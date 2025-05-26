import time

import numpy as np
from bpy.types import Object as BObject


class DisjointSet:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        else:
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1


class HairUVProcessor:
    def __init__(self, b_object: BObject,
                 uv_layer_name: str,
                 spacing: float):
        if b_object.type != 'MESH':
            raise RuntimeError("Select a mesh object containing your hair strands")

        self.b_object = b_object
        self.uv_layer_name = uv_layer_name
        self.spacing = spacing

    def uv_exists(self) -> bool:
        return self.b_object.data.uv_layers.get(self.uv_layer_name) is not None

    def regenerate_uv(self):
        mesh = self.b_object.data

        start = time.time()
        mesh.calc_loop_triangles()
        self._print_timing(start, "mesh.calc_loop_triangles")

        old_layer = mesh.uv_layers.active
        existing = mesh.uv_layers.get(self.uv_layer_name)
        if existing:
            mesh.uv_layers.remove(existing)
        new_layer = mesh.uv_layers.new(name=self.uv_layer_name)
        self._print_timing(start, "UV layer setup")

        loops = mesh.loops
        polys = mesh.polygons
        nl = len(loops)
        num_polys = len(polys)

        # bulk-get old UVs
        uv_old = np.empty((nl * 2,), dtype=np.float32)
        old_layer.data.foreach_get("uv", uv_old)
        uv_old = uv_old.reshape(nl, 2)
        self._print_timing(start, "bulk-get UVs")

        # prepare new UV buffer
        uv_new = uv_old.copy()

        # build loop->poly map
        loop_to_poly = np.empty((nl,), dtype=np.int32)
        for p in polys:
            s, t = p.loop_start, p.loop_total
            loop_to_poly[s:s + t] = p.index
        self._print_timing(start, "build loop_to_poly")

        # sort loops by UV
        structured = np.zeros(nl, dtype=[('u', 'f4'), ('v', 'f4'), ('p', 'i4'), ('i', 'i4')])
        structured['u'], structured['v'] = uv_old[:, 0], uv_old[:, 1]
        structured['p'] = loop_to_poly
        structured['i'] = np.arange(nl, dtype=np.int32)
        structured.sort(order=('u', 'v'))
        self._print_timing(start, "sort UVs")

        # union-find on identical UV
        ds = DisjointSet(num_polys)
        i = 0
        while i < nl:
            j = i + 1
            while j < nl and structured['u'][j] == structured['u'][i] and structured['v'][j] == structured['v'][i]:
                ds.union(structured['p'][i], structured['p'][j])
                j += 1
            i = j
        self._print_timing(start, "union-find UV islands")

        # map loops to island roots
        loops_root = np.vectorize(ds.find)(loop_to_poly)
        self._print_timing(start, "map loops to roots")

        # relabel
        unique, loops_island = np.unique(loops_root, return_inverse=True)
        num_islands = unique.size
        self._print_timing(start, f"relabel islands ({num_islands})")

        # vectorized min/max per island via sorting & reduce at
        u = uv_old[:, 0]
        v = uv_old[:, 1]
        order = np.argsort(loops_island)
        labels = loops_island[order]
        u_s = u[order]
        v_s = v[order]
        # group boundaries
        idx = np.nonzero(np.diff(labels) != 0)[0] + 1
        boundaries = np.concatenate(([0], idx, [nl]))
        starts = boundaries[:-1]
        # reduce
        u_min = np.minimum.reduceat(u_s, starts)
        u_max = np.maximum.reduceat(u_s, starts)
        v_min = np.minimum.reduceat(v_s, starts)
        v_max = np.maximum.reduceat(v_s, starts)
        self._print_timing(start, "vectorized min/max")

        widths = u_max - u_min
        heights = v_max - v_min

        # normalize islands
        u_norm = (u - u_min[loops_island]) / (widths[loops_island] + 1e-8)
        v_norm = (v - v_min[loops_island]) / (heights[loops_island] + 1e-8)

        # compute total width and scale into 0..1
        scaled_widths = widths + self.spacing
        total_width = np.sum(scaled_widths)
        x_offsets = np.zeros(num_islands, dtype=np.float32)
        x_offsets[1:] = np.cumsum(scaled_widths[:-1])
        x_offsets /= total_width  # normalize into 0..1
        scaled_widths /= total_width

        # fit into 0-1 tile
        new_u = u_norm * scaled_widths[loops_island] + x_offsets[loops_island]
        new_v = v_norm

        uv_new[:, 0], uv_new[:, 1] = new_u, new_v
        self._print_timing(start, "normalize & tile")

        # write back
        flat = uv_new.ravel().astype(np.float32)
        new_layer.data.foreach_set("uv", flat.tolist())
        mesh.update()
        self._print_timing(start, f"finished packing {num_islands} islands")

    def _print_timing(self, start: float, step: str):
        print(f"BlendedHairUVProcessor[{self.b_object.name}][{self.uv_layer_name}]: "
              f"Completed {step} at {time.time() - start:.2f}s")
