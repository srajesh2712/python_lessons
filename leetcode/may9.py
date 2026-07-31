from typing import List
class Solution:
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        left=0
        top = 0
        print(len(grid))
        right = len(grid)-1
        bottom = len(grid[0])-1
        print(grid,k)
        current = left
        while current <= right:
            print(grid[top][current])
            current= current+1

if __name__ == '__main__':
    solution = Solution()
    grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    k = 2
    solution.rotateGrid(grid, k)

# Explanation: The figures above represent the grid at every state.to the many company


