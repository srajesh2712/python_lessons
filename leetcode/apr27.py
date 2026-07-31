from collections import deque
from typing import List

conf = {#1 R -1 L 3 TOP 4 BOTTOM
    1:{(0,1):[1,3,5],   (0,-1):[1,4,6]},
    2:{(-1,0):[2,3,4],     (1,0):[2,5,6]},
    3:{(0,-1):[1,4,6],  (1,0):[2,5,6]},
    4:{(0,1):[1,3,5],       (1,0):[2,5,6]},
    5:{(0,-1):[1,4,6],  (-1,0):[2,3,4]},
    6:{(-1,0):[2,3,4],   (0,1):[1,3,5]}
}

class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        deq = deque([(0, 0)])
        row, col = len(grid), len(grid[0])
        visited = set([(0,0)])

        while deq:
            r,c = deq.popleft()
            if r == row - 1 and c == col - 1: return True
            curr_cell_val = grid[r][c]
            visited.add((r,c))

            for key,val in  conf[curr_cell_val].items():
                nr= r+key[0]
                nc= c+key[1]
                if 0 <= nr < row and 0 <= nc < col:
                    if grid[nr][nc] in val and (nr,nc)  not in visited:
                        deq.append((nr,nc))
                        visited.add((nr,nc))

        return False

if __name__ == '__main__':
    print(Solution().hasValidPath(grid=[[4,1],[6,1]]))

