from collections import deque
from typing import List
class Solution:
    offset = {
        "right": (0, 1),
        "left": (0, -1),
        "down": (1, 0),
        "up": (-1, 0),
    }
    def containsCycle(self, grid: List[List[str]]) -> bool:
        rows,cols = len(grid), len(grid[0])
        visited = set()
        for r in range(rows):
            for c in range(cols):
                if (r,c) not in visited:
                    char = grid[r][c]
                    queue = deque([(r, c, -1, -1)])
                    visited.add((r, c))
                    while queue:
                        curr_r,curr_c,pr,pc= queue.popleft()
                        for dr,dc in self.offset.values():
                            nr,nc = curr_r+dr,curr_c+dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == char:
                                if (nr,nc) == (pr,pc):
                                    continue

                                if (nr, nc) in visited:
                                    return True

                                visited.add((nr, nc))
                                queue.append((nr, nc, curr_r, curr_c))
        return False





if __name__ == '__main__':
    s = Solution()
    print(s.containsCycle([["a","a","a","a"],["a","b","b","a"],["a","b","b","a"],["a","a","a","a"]]))