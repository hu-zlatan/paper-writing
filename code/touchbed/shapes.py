"""Object libraries for TouchBED (docs/08_experiment_plan.yaml, `datasets`).

All shapes are simple planar polygons in millimetres, counter-clockwise, centred at their area centroid and scaled so the
circumradius about the centroid is R = 40 mm. Everything is generated procedurally from fixed seeds; no external data.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box

R_CIRCUM = 40.0  # mm


@dataclass
class Shape:
    name: str
    verts: np.ndarray  # (V, 2) CCW, centroid at origin
    sym: list = field(default_factory=lambda: [0.0])  # rotation symmetry group (radians), always contains 0

    @property
    def poly(self) -> Polygon:
        return Polygon(self.verts)


def _normalize(poly: Polygon, scale_to_r: bool = True) -> np.ndarray:
    """Centre at the area centroid, orient CCW, optionally scale circumradius to R_CIRCUM, drop duplicate closing vertex."""
    poly = poly.buffer(0)  # repair any numerical self-touching
    c = poly.centroid
    poly = affinity.translate(poly, -c.x, -c.y)
    v = np.asarray(poly.exterior.coords)[:-1]
    if scale_to_r:
        v = v * (R_CIRCUM / np.max(np.linalg.norm(v, axis=1)))
    # CCW orientation: positive signed area
    x, y = v[:, 0], v[:, 1]
    if 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y) < 0:
        v = v[::-1]
    # remove near-collinear / duplicate vertices (keeps edge count honest)
    keep = []
    n = len(v)
    for i in range(n):
        a, b, c2 = v[i - 1], v[i], v[(i + 1) % n]
        cross = (b[0] - a[0]) * (c2[1] - b[1]) - (b[1] - a[1]) * (c2[0] - b[0])
        if np.linalg.norm(b - a) > 1e-6 and abs(cross) > 1e-9:
            keep.append(i)
    return np.ascontiguousarray(v[keep], dtype=float)


def rot_iou(verts: np.ndarray, ang: float) -> float:
    p = Polygon(verts)
    q = affinity.rotate(p, ang, origin=(0, 0), use_radians=True)
    return p.intersection(q).area / p.union(q).area


def symmetry_group(verts: np.ndarray, tol: float = 0.999) -> list:
    """Rotations (about the centroid) mapping the shape onto itself, tested on the candidate set 2*pi*j/n."""
    group = {0.0}
    for n in range(2, 13):
        for j in range(1, n):
            ang = 2 * math.pi * j / n
            if rot_iou(verts, ang) >= tol:
                group.add(round(ang, 10))
    return sorted(group)


def self_confusability(verts: np.ndarray, sym: list, step_deg: float = 2.0, min_sep_deg: float = 10.0) -> float:
    """max IoU(shape, R_theta shape) over theta at least min_sep_deg away from every element of the symmetry group."""
    best = 0.0
    for d in np.arange(step_deg, 360.0, step_deg):
        ang = math.radians(d)
        sep = min(abs(math.degrees((ang - g + math.pi) % (2 * math.pi) - math.pi)) for g in sym)
        if sep >= min_sep_deg:
            best = max(best, rot_iou(verts, ang))
    return best


def make_irregular(rng: np.random.Generator, n_min: int = 8, n_max: int = 14, min_edge: float = 6.0) -> np.ndarray:
    """Star-shaped (hence simple) irregular polygon about the origin; rejection-sampled for minimum edge length."""
    while True:
        n = int(rng.integers(n_min, n_max + 1))
        ang = np.sort(rng.uniform(0, 2 * math.pi, n))
        if np.min(np.diff(np.r_[ang, ang[0] + 2 * math.pi])) < math.radians(12):
            continue
        rad = rng.uniform(0.55, 1.0, n)
        v = np.c_[rad * np.cos(ang), rad * np.sin(ang)]
        p = Polygon(v)
        if not p.is_valid:
            continue
        v = _normalize(p)
        e = np.linalg.norm(np.roll(v, -1, axis=0) - v, axis=1)
        if len(v) >= n_min and e.min() >= min_edge:
            return v


def make_set_A(seed: int = 0, K: int = 8, max_self_conf: float = 0.80) -> list:
    """Asymmetric irregular polygons. A4 is the first 4 of A8; A8 the first 8 of A16 (same seed stream)."""
    rng = np.random.default_rng(seed)
    shapes = []
    while len(shapes) < K:
        v = make_irregular(rng)
        sym = symmetry_group(v)
        if len(sym) != 1:
            continue
        if self_confusability(v, sym, step_deg=3.0) > max_self_conf:
            continue
        shapes.append(Shape(f"A{len(shapes)}", v, sym))
    return shapes


def _rounded_triangle(side: float = 60.0, corner_r: float = 6.0) -> Polygon:
    h = side * math.sqrt(3) / 2
    tri = Polygon([(-side / 2, -h / 3), (side / 2, -h / 3), (0, 2 * h / 3)])
    return tri.buffer(-corner_r, join_style="mitre").buffer(corner_r, quad_segs=4)


def _bases() -> dict:
    return {
        "rect": box(-40, -20, 40, 20),
        "rtri": _rounded_triangle(),
        "hex": Polygon([(math.cos(math.pi / 3 * i), math.sin(math.pi / 3 * i)) for i in range(6)]),
        "trap": Polygon([(-40, -18), (40, -18), (22, 18), (-22, 18)]),
    }


def _scaled(poly: Polygon) -> Polygon:
    c = poly.centroid
    poly = affinity.translate(poly, -c.x, -c.y)
    r = max(math.hypot(x, y) for x, y in poly.exterior.coords)
    return affinity.scale(poly, R_CIRCUM / r, R_CIRCUM / r, origin=(0, 0))


def _edge_feature(poly: Polygon, edge_frac: float, kind: str, width: float = 6.0, depth: float = 3.5,
                  edge_index: int = 0) -> Polygon:
    """Cut a notch / add a bump of size width x depth on edge `edge_index` at fraction `edge_frac` along it, or chamfer
    the start vertex of that edge (kind='chamfer')."""
    v = np.asarray(poly.exterior.coords)[:-1]
    if poly.exterior.is_ccw is False:
        v = v[::-1]
    a, b = v[edge_index], v[(edge_index + 1) % len(v)]
    e = (b - a) / np.linalg.norm(b - a)
    nrm = np.array([e[1], -e[0]])  # outward for CCW
    if kind == "chamfer":
        prev = v[edge_index - 1]
        e_prev = (a - prev) / np.linalg.norm(a - prev)
        cut = Polygon([a, a + e * width, a - e_prev * width])
        return poly.difference(cut.buffer(1e-9))
    c = a + edge_frac * (b - a)
    rect = Polygon([c - e * width / 2 - nrm * depth, c + e * width / 2 - nrm * depth,
                    c + e * width / 2 + nrm * depth, c - e * width / 2 + nrm * depth])
    if kind == "notch":
        return poly.difference(rect)
    if kind == "bump":
        return poly.union(rect)
    raise ValueError(kind)


def make_set_S() -> list:
    """Four near-symmetric bases + one symmetry-breaking variant each (K = 8)."""
    bases = {k: _scaled(p) for k, p in _bases().items()}
    variants = {
        "rect": ("notch", 0.30, 0, 3.5),   # long bottom edge, off-centre notch
        "rtri": ("bump", 0.30, 0, 3.5),
        "hex": ("notch", 0.30, 0, 4.0),
        "trap": ("notch", 0.30, 2, 3.5),   # short top edge, off-centre notch
    }
    shapes = []
    for name, p in bases.items():
        v = _normalize(p)
        shapes.append(Shape(f"S_{name}", v, symmetry_group(v)))
    for name, p in bases.items():
        kind, frac, ei, depth = variants[name]
        q = _edge_feature(p, frac, kind, depth=depth, edge_index=ei)
        assert len(np.asarray(q.exterior.coords)) > len(np.asarray(p.exterior.coords)), f"feature not applied to {name}"
        v = _normalize(q)
        shapes.append(Shape(f"S_{name}_{kind}", v, symmetry_group(v)))
    return shapes


def make_positive_control() -> list:
    """H2b-P2: two 2:1 rectangles identical except a notch (6 mm x 4 mm) at 30% along the bottom edge."""
    r = _scaled(box(-40, -20, 40, 20))
    q = _edge_feature(r, 0.30, "notch", depth=4.0, edge_index=0)
    out = []
    for name, p in (("PC_rect", r), ("PC_rect_notch", q)):
        v = _normalize(p)
        out.append(Shape(name, v, symmetry_group(v)))
    return out


def get_set(name: str) -> list:
    if name == "A":
        return make_set_A(0, 8)
    if name == "A4":
        return make_set_A(0, 4)
    if name == "A16":
        return make_set_A(0, 16)
    if name == "S":
        return make_set_S()
    if name == "PC":
        return make_positive_control()
    raise KeyError(name)
