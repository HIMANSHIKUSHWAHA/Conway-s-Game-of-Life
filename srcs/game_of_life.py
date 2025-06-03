# File: srcs/game_of_life.py

import numpy as np

class GameOfLifeWormhole:
    """
    Conway's Game of Life, but when looking for neighbors, a cell can "teleport"
    through wormholes. We use the precedence rule: Top > Right > Bottom > Left when
    multiple wormholes could apply to a given directional step.
    """

    def __init__(self, grid, h_wormholes=None, v_wormholes=None):
        """
        grid:       2D boolean numpy array (True = alive, False = dead)
        h_wormholes: dict mapping (r, c) → (r2, c2) for horizontal tunnels
        v_wormholes: dict mapping (r, c) → (r2, c2) for vertical tunnels
        """
        self.grid = grid.copy()
        self.rows, self.cols = grid.shape
        self.holes_h = h_wormholes or {}
        self.holes_v = v_wormholes or {}

    def in_bounds(self, r, c):
        """Return True if (r, c) is within the grid."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def teleport(self, r, c, dr, dc):
        """
        Given a source cell (r, c) and a step (dr, dc), return the final neighbor
        (nr, nc) after applying any applicable wormhole rules. The precedence is:
          - If dr == -1 (moving Up or Up-diagonal), vertical wormholes first.
          - If dr == 0 and dc == +1 (moving Right), horizontal wormholes first.
          - If dr == +1 and dc == +1 (moving Down-Right), horizontal first, then vertical.
          - If dr == +1 and dc == 0 (moving Down), vertical first.
          - If dr == +1 and dc == -1 (moving Down-Left), vertical first, then horizontal.
          - If dr == 0 and dc == -1 (moving Left), horizontal wormholes first.
        After any teleport, still apply the same (dr, dc) offset.
        """
        raw_r, raw_c = r + dr, c + dc

        # 1) Moving Up (dr = -1, dc = -1/0/+1)
        if dr == -1:
            # a) vertical wormhole at source
            if (r, c) in self.holes_v:
                pr, pc = self.holes_v[(r, c)]
                return pr + dr, pc + dc
            # b) vertical wormhole at raw neighbor
            if (raw_r, raw_c) in self.holes_v:
                pr, pc = self.holes_v[(raw_r, raw_c)]
                return pr, pc
            # c) otherwise raw neighbor
            return raw_r, raw_c

        # 2) Moving Right (dr = 0, dc = +1)
        if dr == 0 and dc == 1:
            if (r, c) in self.holes_h:
                pr, pc = self.holes_h[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_h:
                pr, pc = self.holes_h[(raw_r, raw_c)]
                return pr, pc
            return raw_r, raw_c

        # 3) Moving Down-Right (dr = +1, dc = +1) → Right first, then Bottom
        if dr == 1 and dc == 1:
            # horizontal (Right) first
            if (r, c) in self.holes_h:
                pr, pc = self.holes_h[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_h:
                pr, pc = self.holes_h[(raw_r, raw_c)]
                return pr, pc
            # then vertical (Bottom)
            if (r, c) in self.holes_v:
                pr, pc = self.holes_v[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_v:
                pr, pc = self.holes_v[(raw_r, raw_c)]
                return pr, pc
            return raw_r, raw_c

        # 4) Moving Down (dr = +1, dc = 0)
        if dr == 1 and dc == 0:
            if (r, c) in self.holes_v:
                pr, pc = self.holes_v[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_v:
                pr, pc = self.holes_v[(raw_r, raw_c)]
                return pr, pc
            return raw_r, raw_c

        # 5) Moving Down-Left (dr = +1, dc = -1) → Bottom first, then Left
        if dr == 1 and dc == -1:
            if (r, c) in self.holes_v:
                pr, pc = self.holes_v[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_v:
                pr, pc = self.holes_v[(raw_r, raw_c)]
                return pr, pc
            if (r, c) in self.holes_h:
                pr, pc = self.holes_h[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_h:
                pr, pc = self.holes_h[(raw_r, raw_c)]
                return pr, pc
            return raw_r, raw_c

        # 6) Moving Left (dr = 0, dc = -1)
        if dr == 0 and dc == -1:
            if (r, c) in self.holes_h:
                pr, pc = self.holes_h[(r, c)]
                return pr + dr, pc + dc
            if (raw_r, raw_c) in self.holes_h:
                pr, pc = self.holes_h[(raw_r, raw_c)]
                return pr, pc
            return raw_r, raw_c

        # (Up-Left dr=-1,dc=-1) is covered by dr=-1 branch
        return raw_r, raw_c

    def get_neighbor_positions(self, r, c):
        """
        Return a list of valid neighbor coordinates for cell (r, c), after teleporting.
        Only in-bounds positions are returned.
        """
        positions = []
        directions = [
            (-1,  0),  # top
            (-1,  1),  # top-right
            ( 0,  1),  # right
            ( 1,  1),  # bottom-right
            ( 1,  0),  # bottom
            ( 1, -1),  # bottom-left
            ( 0, -1),  # left
            (-1, -1),  # top-left
        ]
        for dr, dc in directions:
            nr, nc = self.teleport(r, c, dr, dc)
            if self.in_bounds(nr, nc):
                positions.append((nr, nc))
        return positions

    def step(self):
        """
        Execute one generation of Game of Life with wormholes.
        """
        new_grid = np.zeros_like(self.grid)
        for r in range(self.rows):
            for c in range(self.cols):
                live_neighbors = 0
                for (nr, nc) in self.get_neighbor_positions(r, c):
                    if self.grid[nr, nc]:
                        live_neighbors += 1

                if self.grid[r, c]:
                    # Survives if 2 or 3 neighbors
                    new_grid[r, c] = (live_neighbors == 2 or live_neighbors == 3)
                else:
                    # Birth if exactly 3 neighbors
                    new_grid[r, c] = (live_neighbors == 3)

        self.grid = new_grid

    def simulate(self, iterations):
        """
        Run `iterations` steps consecutively. Returns the final grid.
        """
        for _ in range(iterations):
            self.step()
        return self.grid.copy()
