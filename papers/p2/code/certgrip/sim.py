"""CertGrip simulator: a parallel-jaw gripper holding one rigid object in MuJoCo, replayable at any grip force.

One grasp *instance* = (object geometry, mass, friction, CoM offset, grasp offset, disturbance). `replay(inst, F)` runs
the full grasp protocol with the grip force F and returns whether the object slipped plus the tactile/proprioceptive
features recorded before the force is applied (they do not depend on F). Everything is deterministic given `inst`.

Protocol (07_hypotheses §1.1, simplified for the stage-10 pilot):
  1. the pads close on the object at a constant preload F0 (same for every instance) while the hand holds still;
     gravity acts, the object is supported by the grasp alone (lift phase is a hold in the hand frame);
  2. probe squeeze F0 -> 1.5 F0 -> F0;
  3. ramp to the chosen F and settle;
  4. disturbance window (D1 lift acceleration, D2 shake, D3 lateral pull, D4 added payload).
Slip = tangential displacement of the object in the hand frame > delta_t, or rotation about the grasp axis > rot_t,
or loss of contact with a pad (07_hypotheses §1.1); the normal (x) component is excluded by construction.
"""
from __future__ import annotations

import dataclasses
import math

import mujoco
import numpy as np

G = 9.81
DT = 0.002
T_PRELOAD, T_PROBE, T_RAMP, T_SETTLE, T_DIST = 0.4, 0.3, 0.1, 0.1, 0.6
PAD_HALF = (0.004, 0.02, 0.03)  # pad box half-sizes (x thickness, y width, z height) [m]
T_RD, RD_FLOOR, RD_DISP, RD_ROT = 0.4, 0.02, 0.0003, math.radians(1.0)  # ramp-down probe (pilot candidate)
GRID = 8                        # touch_grid resolution per pad (GRID x GRID)


@dataclasses.dataclass
class Instance:
    family: str          # F1 box, F2 cylinder, F3 capsule, F4 composite, F5 plate
    size: tuple          # geometry parameters [m]
    mass: float          # [kg]
    mu: float            # sliding friction (object; pads use the same so the pair value is mu)
    com: float           # CoM offset along z (jaw-parallel, vertical) [m]
    grasp_dz: float      # grasp offset along z [m]
    dist: str            # D1..D4
    amp: float           # D1 m/s^2, D2 m (amplitude), D3 multiple of m g, D4 multiple of m
    freq: float = 0.0    # D2 Hz


def half_width(inst: Instance) -> float:
    """Half-extent of the object along the jaw (x) axis."""
    if inst.family in ("F1", "F5", "F4"):
        return inst.size[0]
    return inst.size[0]  # cylinder / capsule radius


def build_xml(inst: Instance, delta_pad: float = 0.0) -> str:
    hw = half_width(inst)
    if inst.family in ("F1", "F5"):
        geom = f'<geom name="obj" type="box" size="{inst.size[0]} {inst.size[1]} {inst.size[2]}"'
    elif inst.family == "F2":
        geom = f'<geom name="obj" type="cylinder" size="{inst.size[0]} {inst.size[1]}" euler="0 0 0"'
    elif inst.family == "F3":
        geom = f'<geom name="obj" type="capsule" size="{inst.size[0]} {inst.size[1]}"'
    elif inst.family == "F4":
        geom = (f'<geom name="obj" type="box" size="{inst.size[0]} {inst.size[1]} {inst.size[2]}"'
                f' mass="{0.5 * inst.mass}" friction="{inst.mu} 0.005 0.0001"/>'
                f'<geom name="obj2" type="sphere" size="{0.6 * inst.size[0]}" pos="0 0 {inst.size[2] * 0.8}"'
                f' mass="{0.5 * inst.mass}" contype="0" conaffinity="0"')
    else:
        raise ValueError(inst.family)
    if inst.family != "F4":
        geom += f' mass="{inst.mass}" friction="{inst.mu} 0.005 0.0001"'
    geom += "/>"
    # CoM offset: inertial pos overrides geom-derived CoM (all families incl. F4 via explicit inertial)
    I = inst.mass * (hw ** 2 + 0.03 ** 2) / 5
    inertial = f'<inertial pos="0 0 {inst.com}" mass="{inst.mass}" diaginertia="{I} {I} {I}"/>'
    px, py, pz = PAD_HALF
    gap = hw + px + 0.0005
    return f"""
<mujoco model="certgrip">
  <option timestep="{DT}" cone="elliptic" impratio="10" gravity="0 0 -{G}" integrator="implicitfast"/>
  <default><geom solref="0.004 1" solimp="0.95 0.99 0.001" condim="6"/></default>
  <extension><plugin plugin="mujoco.sensor.touch_grid"/></extension>
  <worldbody>
    <body name="hand" mocap="true" pos="0 0 0.5">
      <body name="padL" pos="{-gap} 0 {-inst.grasp_dz}">
        <joint name="jL" type="slide" axis="1 0 0" damping="20" range="-0.05 0.05"/>
        <geom name="gL" type="box" size="{px} {py} {pz}" mass="0.05" friction="{inst.mu} 0.005 0.0001"/>
        <site name="sL" pos="{-6 * px} 0 0" euler="0 -90 0" size="0.001"/>
      </body>
      <body name="padR" pos="{gap} 0 {-inst.grasp_dz}">
        <joint name="jR" type="slide" axis="1 0 0" damping="20" range="-0.05 0.05"/>
        <geom name="gR" type="box" size="{px} {py} {pz}" mass="0.05" friction="{inst.mu} 0.005 0.0001"/>
        <site name="sR" pos="{6 * px} 0 0" euler="0 90 0" size="0.001"/>
      </body>
    </body>
    <body name="object" pos="0 0 0.5">
      <freejoint name="free"/>
      {inertial}
      {geom}
    </body>
  </worldbody>
  <actuator>
    <motor name="aL" joint="jL" gear="1" ctrlrange="0 200"/>
    <motor name="aR" joint="jR" gear="-1" ctrlrange="0 200"/>
  </actuator>
  <sensor>
    <plugin name="tL" plugin="mujoco.sensor.touch_grid" objtype="site" objname="sL">
      <config key="size" value="{GRID} {GRID}"/><config key="fov" value="80 80"/>
      <config key="gamma" value="0"/><config key="nchannel" value="3"/>
    </plugin>
    <plugin name="tR" plugin="mujoco.sensor.touch_grid" objtype="site" objname="sR">
      <config key="size" value="{GRID} {GRID}"/><config key="fov" value="80 80"/>
      <config key="gamma" value="0"/><config key="nchannel" value="3"/>
    </plugin>
  </sensor>
</mujoco>"""


def tangential_disp(dp) -> float:
    """Displacement projected onto the pad plane (y, z); the normal (x, jaw-axis) component is excluded (UT9)."""
    return float(np.linalg.norm(np.asarray(dp)[1:]))


def preload_force(m_max: float = 1.0, mu_min: float = 0.3) -> float:
    """Constant preload F0 = 2 m_max g / (2 mu_min) (07_hypotheses §1.1) — identical for every instance."""
    return 2 * m_max * G / (2 * mu_min)


class Sim:
    """Compiled model for one instance; `run(F)` replays the protocol from the same initial state."""

    def __init__(self, inst: Instance, F0: float, delta_t: float = 0.002, rot_t_deg: float = 3.0,
                 rampdown: bool = False):
        self.inst, self.F0, self.rampdown = inst, F0, rampdown
        self.delta_t, self.rot_t = delta_t, math.radians(rot_t_deg)
        self.m = mujoco.MjModel.from_xml_string(build_xml(inst))
        self.d = mujoco.MjData(self.m)
        self.obj = self.m.body("object").id
        self.hand_mocap = self.m.body("hand").mocapid[0]
        self.gL, self.gR = self.m.geom("gL").id, self.m.geom("gR").id
        self.obj_geoms = {self.m.geom("obj").id}

    # ------------------------------------------------------------------ helpers
    def _set_force(self, F):
        self.d.ctrl[0] = F
        self.d.ctrl[1] = F

    def _hand_pos(self):
        return self.d.mocap_pos[self.hand_mocap].copy()

    def _rel_pose(self):
        """Object position relative to the hand and object rotation about the grasp (x) axis."""
        p = self.d.xpos[self.obj] - self._hand_pos()
        R = self.d.xmat[self.obj].reshape(3, 3)
        ang = math.atan2(R[2, 1], R[2, 2])  # rotation about x (hand frame = world frame, hand does not rotate)
        return p, ang

    def _pad_contact(self):
        cL = cR = False
        for i in range(self.d.ncon):
            c = self.d.contact[i]
            pair = {c.geom1, c.geom2}
            if pair & self.obj_geoms:
                cL |= self.gL in pair
                cR |= self.gR in pair
        return cL and cR

    def _touch(self):
        return self.d.sensordata.copy()

    def _step(self, n=1):
        mujoco.mj_step(self.m, self.d, nstep=n)

    def _dist_apply(self, t):
        """Disturbance at time t into the window, applied at the object's CoM in the (non-rotating) hand frame.

        D1/D2 are hand motions. A kinematic (mocap) hand cannot drag the object through MuJoCo's velocity-level
        friction, so the hand is kept still and the motion enters as the exact inertial pseudo-force -m a_hand(t)
        on the object (the pads are rigidly attached to the hand along y, z, so in the hand frame only the object
        feels it). D1: lift profile +a for 0.15 s then -a for 0.15 s. D2: hand z = A sin(wt), a = -A w^2 sin(wt).
        D3: lateral (y) pull, D4: added payload (downward), both ramped over 0.1 s.
        """
        inst = self.inst
        self.d.xfrc_applied[self.obj] = 0.0
        if inst.dist == "D1":
            a = inst.amp if t < 0.15 else (-inst.amp if t < 0.30 else 0.0)
            self.d.xfrc_applied[self.obj, 2] = -inst.mass * a
        elif inst.dist == "D2":
            w = 2 * math.pi * inst.freq
            self.d.xfrc_applied[self.obj, 2] = -inst.mass * (-inst.amp * w * w * math.sin(w * t))
        elif inst.dist == "D3":    # lateral (y) pull on the object, ramped over 0.1 s
            self.d.xfrc_applied[self.obj, 1] = inst.amp * inst.mass * G * min(1.0, t / 0.1)
        elif inst.dist == "D4":    # payload: extra downward load, ramped over 0.1 s
            self.d.xfrc_applied[self.obj, 2] = -inst.amp * inst.mass * G * min(1.0, t / 0.1)

    def _rampdown_probe(self, p_ref, a_ref, record):
        """Lower the grip force log-linearly from F0 to RD_FLOOR*F0 over T_RD; stop at the first tangential
        micro-displacement > RD_DISP or rotation > RD_ROT (incipient slip), then return to F0 over 0.1 s and hold
        0.1 s. Returns the onset force and the touch frame at onset (only the robot-observable quantities are used
        as features: commanded force at onset and pad readings; the displacement test stands in for a tactile
        incipient-slip detector)."""
        n = int(T_RD / DT)
        onset, F, touch = None, self.F0 * RD_FLOOR, None
        for k in range(n):
            F = self.F0 * math.exp(math.log(RD_FLOOR) * (k + 1) / n)
            self._set_force(F)
            self._step()
            p, a = self._rel_pose()
            if tangential_disp(p - p_ref) > RD_DISP or abs(a - a_ref) > RD_ROT:
                onset = F
                break
        if record:
            touch = self._touch()
        F_end = F
        n_up = int(0.1 / DT)
        for k in range(n_up):
            self._set_force(F_end + (self.F0 - F_end) * (k + 1) / n_up)
            self._step()
        self._step(int(0.1 / DT))
        return {"onset_force": onset, "found": onset is not None, "end_force": F_end, "touch_onset": touch}

    # ------------------------------------------------------------------ protocol
    def run(self, F: float, record: bool = False):
        """Replay the instance at grip force F. Returns dict(slip, reason, features?)."""
        m, d = self.m, self.d
        mujoco.mj_resetData(m, d)
        mujoco.mj_forward(m, d)
        feats = {}
        # 1. preload hold
        self._set_force(self.F0)
        n_pre = int(T_PRELOAD / DT)
        self._step(n_pre)
        p0, a0 = self._rel_pose()
        if record:
            feats["touch_preload"] = self._touch()
            feats["aperture"] = float(d.qpos[m.joint("jR").qposadr[0]] - d.qpos[m.joint("jL").qposadr[0]])
        pre_slip = False
        # 2. probe squeeze F0 -> 1.5F0 -> F0
        n_probe = int(T_PROBE / DT)
        probe = []
        for k in range(n_probe):
            s = k / n_probe
            self._set_force(self.F0 * (1 + 0.5 * math.sin(math.pi * s)))
            self._step()
            if record and k % 15 == 0:
                probe.append(self._touch())
        if record:
            feats["touch_probe"] = np.array(probe)
            feats["aperture_probe"] = float(d.qpos[m.joint("jR").qposadr[0]] - d.qpos[m.joint("jL").qposadr[0]])
        p1, a1 = self._rel_pose()
        pre_slip = bool(tangential_disp(p1 - p0) > self.delta_t)
        if self.rampdown:   # 2b. incipient-slip ramp-down probe (pilot amendment candidate; off by default)
            rd = self._rampdown_probe(p1, a1, record)
            if record:
                feats["rampdown"] = rd
            p1, a1 = self._rel_pose()   # slip in steps 3-4 is measured from the pose after the probe
        # 3. ramp to F and settle
        n_r = int(T_RAMP / DT)
        Fs = self.F0
        for k in range(n_r):
            self._set_force(Fs + (F - Fs) * (k + 1) / n_r)
            self._step()
        self._step(int(T_SETTLE / DT))
        pr, ar = self._rel_pose()
        # 4. disturbance window; slip measured relative to the pose at the start of the ramp (p1)
        n_d = int(T_DIST / DT)
        slip, reason = False, ""
        ref_p, ref_a = p1, a1
        for k in range(n_d):
            self._dist_apply((k + 1) * DT)
            self._step()
            if k % 5 == 4:
                p, a = self._rel_pose()
                if tangential_disp(p - ref_p) > self.delta_t:
                    slip, reason = True, "translation"
                    break
                if abs(a - ref_a) > self.rot_t:
                    slip, reason = True, "rotation"
                    break
                if not self._pad_contact():
                    slip, reason = True, "contact_lost"
                    break
        if not slip:  # also catch slip during ramp/settle
            if tangential_disp(pr - ref_p) > self.delta_t:
                slip, reason = True, "translation_settle"
        self.d.xfrc_applied[self.obj] = 0.0
        out = {"slip": slip, "reason": reason, "preload_slip": pre_slip}
        if record:
            out["features"] = feats
        return out


def bisect_fstar(sim: Sim, f_min=0.1, f_max=100.0, halvings=10):
    """Log-space bisection for the minimal no-slip force; returns (F_lo, F_hi, n_replays) or (f_max, inf) if F_max slips."""
    n = 1
    if sim.run(f_max)["slip"]:
        return f_max, math.inf, n
    lo, hi = math.log(f_min), math.log(f_max)
    for _ in range(halvings):
        mid = 0.5 * (lo + hi)
        n += 1
        if sim.run(math.exp(mid))["slip"]:
            lo = mid
        else:
            hi = mid
    return math.exp(lo), math.exp(hi), n


def sample_instance(rng: np.random.Generator, family: str, dist: str) -> Instance:
    """Sample one instance from the design ranges (07_hypotheses §1.2)."""
    mu = float(np.exp(rng.uniform(np.log(0.3), np.log(1.0))))
    mass = float(np.exp(rng.uniform(np.log(0.05), np.log(1.0))))
    if family == "F1":
        size = (rng.uniform(0.015, 0.035), rng.uniform(0.015, 0.035), rng.uniform(0.02, 0.05))
    elif family == "F2":
        size = (rng.uniform(0.015, 0.035), rng.uniform(0.02, 0.05))
    elif family == "F3":
        size = (rng.uniform(0.015, 0.03), rng.uniform(0.01, 0.04))
    elif family == "F4":
        size = (rng.uniform(0.015, 0.035), rng.uniform(0.015, 0.035), rng.uniform(0.02, 0.05))
    elif family == "F5":
        size = (rng.uniform(0.002, 0.005), rng.uniform(0.02, 0.04), rng.uniform(0.02, 0.05))
    else:
        raise ValueError(family)
    zext = size[-1]
    com = float(rng.uniform(-1, 1) * (0.6 if family == "F4" else 0.4) * zext)
    grasp_dz = float(rng.uniform(-0.3, 0.3) * zext)
    freq = 0.0
    if dist == "D1":
        amp = rng.uniform(1, 10)
    elif dist == "D2":
        amp, freq = rng.uniform(0.005, 0.02), rng.uniform(2, 5)
    elif dist == "D3":
        amp = rng.uniform(0.5, 2.0)
    else:
        amp = rng.uniform(0.2, 1.0)
    return Instance(family, tuple(float(s) for s in size), mass, mu, com, grasp_dz, dist, float(amp), float(freq))
