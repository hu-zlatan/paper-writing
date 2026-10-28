"""MuJoCo contact evaluation for H4 (docs/07_hypotheses.md, docs/08_experiment_plan.yaml `mujoco_scenes`).

Each polygon is built as a set of thin box "walls" (one per edge, 1.5 mm thick, placed inside the boundary, 30 mm tall)
so non-convex outlines (notches) are represented exactly — MuJoCo would convexify a single mesh. Objects are mocap bodies;
the spherical fingertip of radius r is positioned through two slide joints. A probe is executed as a guarded move: the fingertip centre advances
along the probe line in 0.5 mm steps, MuJoCo collision detection (mj_forward) is run at each step, and at the first
step with a finger–object contact the position is refined by bisection to 0.01 mm. The observation is MuJoCo's contact
point and contact normal (pointing from the object to the finger), with the same sensor noise model as the geometric
probe model. This is a kinematic sweep with MuJoCo's collision geometry (finite fingertip radius, contact margins),
not a compliant dynamic contact simulation.
"""
from __future__ import annotations

import math

import numpy as np

try:
    import mujoco
except ImportError:  # pragma: no cover
    mujoco = None

from .geometry import RHO, STROKE, probe_ray
from .likelihood import ObsModel, wrap

WALL = 1.5   # mm
HEIGHT = 30.0  # mm
PARK = 10_000.0  # mm, where inactive objects are parked


def _mjcf(shapes, r_finger: float) -> str:
    bodies = []
    for k, s in enumerate(shapes):
        geoms = []
        v = s.verts
        for i in range(len(v)):
            a, b = v[i], v[(i + 1) % len(v)]
            e = b - a
            ln = float(np.hypot(*e))
            nrm = np.array([e[1], -e[0]]) / ln          # outward normal (CCW)
            c = (a + b) / 2 - nrm * WALL / 2            # wall lies inside the boundary
            ang = math.atan2(e[1], e[0])
            geoms.append(f'<geom type="box" size="{ln / 2 + WALL / 2:.4f} {WALL / 2:.4f} {HEIGHT / 2:.4f}" '
                         f'pos="{c[0]:.4f} {c[1]:.4f} {HEIGHT / 2:.4f}" euler="0 0 {ang:.6f}" contype="1" conaffinity="2"/>')
        bodies.append(f'<body name="obj{k}" mocap="true" pos="{PARK} {PARK * (k + 1)} 0">{"".join(geoms)}</body>')
    # the finger is a jointed (non-static) body: MuJoCo does not test collisions between two static/mocap bodies
    finger = (f'<body name="finger" pos="0 0 {HEIGHT / 2}"><joint name="fx" type="slide" axis="1 0 0"/>'
              f'<joint name="fy" type="slide" axis="0 1 0"/>'
              f'<geom type="sphere" size="{r_finger}" contype="2" conaffinity="1" mass="0.01"/></body>')
    return (f'<mujoco><compiler angle="radian"/><option timestep="0.001"/><worldbody>{"".join(bodies)}{finger}'
            f'</worldbody></mujoco>')


class MujocoProbe:
    def __init__(self, shapes, r_finger: float = 4.0, step: float = 0.5):
        if mujoco is None:
            raise ImportError("mujoco is required for MuJoCo evaluation")
        self.shapes, self.r, self.step = shapes, r_finger, step
        self.model = mujoco.MjModel.from_xml_string(_mjcf(shapes, r_finger))
        self.data = mujoco.MjData(self.model)
        self.qx = self.model.joint("fx").qposadr[0]
        self.qy = self.model.joint("fy").qposadr[0]
        self.obj_mocap = [self.model.body(f"obj{k}").mocapid[0] for k in range(len(shapes))]
        self.finger_geom = self.model.body("finger").geomadr[0]

    def set_object(self, k, x, y, th):
        d = self.data
        for j, m in enumerate(self.obj_mocap):
            d.mocap_pos[m] = [PARK, PARK * (j + 1), 0.0]
            d.mocap_quat[m] = [1, 0, 0, 0]
        m = self.obj_mocap[k]
        d.mocap_pos[m] = [x, y, 0.0]
        d.mocap_quat[m] = [math.cos(th / 2), 0, 0, math.sin(th / 2)]

    def _contact_at(self, px, py):
        d = self.data
        d.qpos[self.qx], d.qpos[self.qy] = px, py
        mujoco.mj_forward(self.model, d)
        best = None
        for i in range(d.ncon):
            c = d.contact[i]
            if self.finger_geom in (c.geom1, c.geom2) and c.dist <= 0:
                n = np.array(c.frame[:3])
                if c.geom1 == self.finger_geom:   # MuJoCo normal points from geom1 to geom2; we want object -> finger
                    n = -n
                if best is None or c.dist < best[0]:
                    best = (c.dist, np.array(c.pos[:2]), n)
        return best

    def probe(self, phi, psi):
        """Guarded move along the probe line; returns (hit, contact_x, contact_y, normal_angle) or a miss."""
        ox, oy, dx, dy = probe_ray(phi, psi)
        s_prev = 0.0
        s = 0.0
        if self._contact_at(ox, oy) is not None:  # starting in contact cannot happen for the prior box; guard anyway
            raise RuntimeError("finger starts in contact")
        while s < STROKE:
            s = min(s + self.step, STROKE)
            if self._contact_at(ox + s * dx, oy + s * dy) is not None:
                lo, hi = s_prev, s
                while hi - lo > 0.01:
                    mid = (lo + hi) / 2
                    if self._contact_at(ox + mid * dx, oy + mid * dy) is None:
                        lo = mid
                    else:
                        hi = mid
                c = self._contact_at(ox + hi * dx, oy + hi * dy)
                return True, float(c[1][0]), float(c[1][1]), float(math.atan2(c[2][1], c[2][0]))
            s_prev = s
        return False, 0.0, 0.0, 0.0

    def sample_obs(self, om: ObsModel, rng: np.random.Generator, s0, phi, psi):
        """Same ε-mixture and sensor noise as likelihood.sample_obs, but the geometric outcome comes from MuJoCo."""
        k, x, y, th = s0
        self.set_object(k, x, y, th)
        hit, qx, qy, qn = self.probe(phi, psi)
        if rng.random() < om.eps:
            if rng.random() < 0.5:
                r = RHO * math.sqrt(rng.random())
                a = rng.uniform(-math.pi, math.pi)
                return True, r * math.cos(a), r * math.sin(a), rng.uniform(-math.pi, math.pi)
            return False, 0.0, 0.0, 0.0
        if not hit:
            return False, 0.0, 0.0, 0.0
        return (True, qx + om.sigma_p * rng.standard_normal(), qy + om.sigma_p * rng.standard_normal(),
                float(wrap(qn + om.sigma_n * rng.standard_normal())))
