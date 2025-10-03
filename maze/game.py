class Maze:
    def __init__(self, rows=20, cols=30, density=0.25):
        self.rows, self.cols, self.density = rows, cols, density
        # Grid values: 0=unwalkable (black), 1=weight 1 (white), 5=weight 5 (blue)
        self.grid = [[1]*cols for _ in range(rows)]  # Start with all walkable (weight 1)
        self.start = (0,0); self.goal = (rows-1, cols-1)

    def generate_random(self):
        import random
        # Generate weighted maze: 0=unwalkable, 1=weight 1, 5=weight 5
        self.grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                rand = random.random()
                if rand < self.density:
                    row.append(0)  # Unwalkable (black)
                elif rand < self.density + 0.1:  # 10% chance for weighted blocks
                    row.append(5)  # Weight 5 (blue)
                else:
                    row.append(1)  # Weight 1 (white)
            self.grid.append(row)

        # Ensure start/goal are walkable
        self.start=(0,0); self.goal=(self.rows-1,self.cols-1)
        sr, sc = self.start
        gr, gc = self.goal
        self.grid[sr][sc] = 1
        self.grid[gr][gc] = 1

        # If not already solvable (respecting weights), carve a path
        if not self._is_reachable_with_dijkstra():
            path = self._randomized_bfs_on_empty_grid()  # path of cells from start->goal
            for r, c in path:
                self.grid[r][c] = 1  # carve to walkable weight 1

    def neighbors(self, r, c):
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<self.rows and 0<=nc<self.cols and self.grid[nr][nc] > 0:
                yield nr,nc

    def get_weight(self, r, c):
        """Get the weight/cost of moving to cell (r,c)"""
        return self.grid[r][c] if self.grid[r][c] > 0 else float('inf')

    # === Helpers ===

    def _is_reachable_with_dijkstra(self):
        """Return True if goal reachable from start given current walls/weights."""
        import heapq
        sr, sc = self.start
        gr, gc = self.goal
        if self.grid[sr][sc] == 0 or self.grid[gr][gc] == 0:
            return False

        dist = [[float('inf')]*self.cols for _ in range(self.rows)]
        dist[sr][sc] = 0
        pq = [(0, sr, sc)]
        while pq:
            d, r, c = heapq.heappop(pq)
            if (r, c) == (gr, gc):
                return True
            if d != dist[r][c]:
                continue
            for nr, nc in self.neighbors(r, c):
                nd = d + self.get_weight(nr, nc)
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
        return False

    def _randomized_bfs_on_empty_grid(self):
        """
        Find a (random-tie) shortest path from start to goal on an EMPTY grid
        (i.e., ignoring current walls/weights). This guarantees a route exists.
        """
        from collections import deque
        import random

        sr, sc = self.start
        gr, gc = self.goal
        q = deque([(sr, sc)])
        parent = { (sr, sc): None }

        while q:
            r, c = q.popleft()
            if (r, c) == (gr, gc):
                break
            # Shuffle 4-neighborhood to induce variety in carved paths
            nbrs = [(-1,0),(1,0),(0,-1),(0,1)]
            random.shuffle(nbrs)
            for dr, dc in nbrs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in parent:
                    parent[(nr, nc)] = (r, c)
                    q.append((nr, nc))

        # Reconstruct path (guaranteed because empty grid is connected)
        path = []
        cur = (gr, gc)
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path.reverse()
        return path
