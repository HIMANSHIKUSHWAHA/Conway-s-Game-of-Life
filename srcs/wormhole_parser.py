# File: srcs/wormhole_parser.py

import numpy as np
from collections import deque

def parse_wormholes_from_color_map(arr):
    """
    Given an (H, W, 3) RGB array `arr`, identify all non-black pixels by color.
    Use 8-connectivity to group same-colored pixels into connected components.
    For each color:
      - If it has an even number of connected components (2,4,6,…),
        pair them in lexicographic order: (comp0 ⇄ comp1), (comp2 ⇄ comp3), etc.,
        provided each paired component has the same size.
      - Otherwise (odd number of components, or size mismatch), skip this color entirely
        (no portals for any pixels of that color), printing a warning.

    Returns:
      A dict mapping (r, c) → (r', c') for every valid portal pixel.
    """
    h, w, _ = arr.shape
    visited = np.zeros((h, w), dtype=bool)

    # color → list of flood-filled connected components (each a list of (r,c))
    color_to_components = {}

    # 8-direction neighbors
    neighbors8 = [
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),           ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]

    # 1) Flood-fill to find all connected components by color
    for r in range(h):
        for c in range(w):
            if visited[r, c]:
                continue

            color = tuple(arr[r, c])
            if color == (0, 0, 0):
                continue  # dead/black pixel

            # BFS flood-fill this color
            queue = deque()
            queue.append((r, c))
            visited[r, c] = True
            comp = [(r, c)]

            while queue:
                cr, cc = queue.popleft()
                for dr, dc in neighbors8:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                        if tuple(arr[nr, nc]) == color:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
                            comp.append((nr, nc))

            comp.sort()
            color_to_components.setdefault(color, []).append(comp)

    wormhole_map = {}

    # 2) For each color, attempt to pair its components
    for color, comps in color_to_components.items():
        ncomps = len(comps)
        if ncomps == 0:
            continue

        if ncomps % 2 != 0:
            print(f"WARNING: Color {color} has {ncomps} connected components (odd). Skipping this color.")
            continue

        # Sort components by first coordinate, to guarantee lexicographic pairing
        comps.sort(key=lambda comp: comp[0])

        # Validate each pair (comp[i], comp[i+1]) has equal size
        all_pairs_valid = True
        for i in range(0, ncomps, 2):
            if len(comps[i]) != len(comps[i + 1]):
                print(
                    f"WARNING: Color {color} has components of different sizes "
                    f"{len(comps[i])} and {len(comps[i+1])}. Skipping this color."
                )
                all_pairs_valid = False
                break
        if not all_pairs_valid:
            continue

        # Pair each pixel in compA to corresponding pixel in compB
        for i in range(0, ncomps, 2):
            compA = comps[i]
            compB = comps[i + 1]
            sizeA = len(compA)
            # sizeB is equal by earlier check
            for idx in range(sizeA):
                coordA = compA[idx]
                coordB = compB[idx]
                wormhole_map[coordA] = coordB
                wormhole_map[coordB] = coordA

    return wormhole_map
