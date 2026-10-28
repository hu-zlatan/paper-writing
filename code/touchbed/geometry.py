"""Vectorized ray-polygon intersection for the geometric probe model.

A probe action a = (phi, psi) starts at P0 = RHO * (cos phi, sin phi) and moves along direction phi + pi + psi for at most
STROKE mm (guarded move). For a state s = (k, x, y, theta) the object is polygon k rotated by theta and translated to
(x, y). `cast` returns, for every (state, action) pair in a broadcast batch, whether the probe hits, the world-frame
contact point and the outward surface normal angle at the contact.
"""
from __future__ import annotations

import numpy as np

RHO = 100.0      # mm, probe start radius
STROKE = 200.0   # mm, guarded-move length
PSI_MAX = np.deg2rad(40.0)


class Library:
    """Polygons padded to a common edge count so batches can be gathered by identity index."""

    def __init__(self, shapes):
        self.shapes = shapes
        self.K = len(shapes)
        self.V = max(len(s.verts) for s in shapes)
        p0 = np.zeros((self.K, self.V, 2))
        p1 = np.zeros((self.K, self.V, 2))
        mask = np.zeros((self.K, self.V), dtype=bool)
        for k, s in enumerate(shapes):
            v = s.verts
            n = len(v)
            p0[k, :n] = v
            p1[k, :n] = np.roll(v, -1, axis=0)
            mask[k, :n] = True
        self.p0, self.p1, self.mask = p0, p1, mask
        e = p1 - p0
        ln = np.linalg.norm(e, axis=-1)
        ln[~mask] = 1.0
        # outward normal of a CCW polygon edge e = (ex, ey) is (ey, -ex) / |e|
        self.normal_ang = np.arctan2(-e[..., 0] / ln, e[..., 1] / ln)
        self.sym = [np.asarray(s.sym) for s in shapes]


def probe_ray(phi, psi):
    """World-frame ray origin and unit direction for actions (phi, psi) (arrays broadcast)."""
    phi = np.asarray(phi, dtype=float)
    psi = np.asarray(psi, dtype=float)
    ox, oy = RHO * np.cos(phi), RHO * np.sin(phi)
    d = phi + np.pi + psi
    return ox, oy, np.cos(d), np.sin(d)


def cast(lib: Library, k, x, y, th, phi, psi):
    """Ray-cast probes against posed polygons.

    All of k, x, y, th, phi, psi are broadcast to a common shape S. Returns (hit [S] bool, px [S], py [S], n_ang [S]);
    px, py, n_ang are NaN-free (0) where hit is False. Cost O(prod(S) * V).
    """
    k, x, y, th, phi, psi = np.broadcast_arrays(np.asarray(k), x, y, th, phi, psi)
    shape = k.shape
    ox, oy, dx, dy = probe_ray(phi, psi)
    c, s = np.cos(th), np.sin(th)
    # ray in the object frame: R(-th) (o - t), R(-th) d
    rx, ry = ox - x, oy - y
    lox, loy = c * rx + s * ry, -s * rx + c * ry
    ldx, ldy = c * dx + s * dy, -s * dx + c * dy
    p0 = lib.p0[k]            # S + (V, 2)
    e = lib.p1[k] - p0
    m = lib.mask[k]
    wx, wy = p0[..., 0] - lox[..., None], p0[..., 1] - loy[..., None]
    ex, ey = e[..., 0], e[..., 1]
    ddx, ddy = ldx[..., None], ldy[..., None]
    denom = ddx * ey - ddy * ex                       # cross(d, e)
    ok = m & (np.abs(denom) > 1e-12)
    safe = np.where(ok, denom, 1.0)
    t = (wx * ey - wy * ex) / safe                    # cross(w, e) / cross(d, e)
    u = (wx * ddy - wy * ddx) / safe                  # cross(w, d) / cross(d, e)
    valid = ok & (t > 1e-9) & (t <= STROKE) & (u >= 0.0) & (u <= 1.0)
    t = np.where(valid, t, np.inf)
    j = np.argmin(t, axis=-1)
    tmin = np.take_along_axis(t, j[..., None], axis=-1)[..., 0]
    hit = np.isfinite(tmin)
    tt = np.where(hit, tmin, 0.0)
    px = np.where(hit, ox + tt * dx, 0.0)
    py = np.where(hit, oy + tt * dy, 0.0)
    nloc = lib.normal_ang[k, j]
    n_ang = np.where(hit, np.angle(np.exp(1j * (nloc + th))), 0.0)
    return hit.reshape(shape), px.reshape(shape), py.reshape(shape), n_ang.reshape(shape)
