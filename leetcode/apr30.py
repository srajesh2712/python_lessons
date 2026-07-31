
from typing import List
class Solution1:
    def debug_grid(self,dp):
        for r in range(len(dp)):
            for c in range(len(dp[0])):
                print(f"Cell ({r},{c}): Buckets {dp[r][c]}")
            print("-" * 20)


    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        r,c = len(grid), len(grid[0])
        #print(r,c)
        dp=[[[-1 for _ in range(k+1)] for _ in range( c)] for _ in range(r)]
        #self.debug_grid(dp)
        for i in range(r):
            for j in range(c):
                toll = 1 if (grid[i][j] > 0) else 0
                val = grid[i][j]

                if i==0 and j==0:
                    if toll <=k:
                        dp [0][0][toll]=val
                    continue
                for cost in range(k+1):
                    score_above = dp[i-1][j][cost] if i >0 else -1
                    score_left = dp[i][j-1][cost] if j >0 else -1
                    best_prev_score = max(score_above, score_left)

                    if best_prev_score != -1:
                        new_cost = cost + toll
                        if new_cost <= k:
                            dp[i][j][new_cost] = max(dp[i][j][new_cost], best_prev_score + grid[i][j])


        #self.debug_grid(dp)
        ans =  max(dp[r-1][c-1])
        return ans if ans != -1 else -1












class Solution:
    def maxPathScore(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        # dp[col][cost] = max_score
        # Initialize with -1 to signify unreachable states
        dp = [[-1] * (k + 1) for _ in range(n)]

        # Base Case: Starting cell (0,0)
        start_cost = 1 if grid[0][0] > 0 else 0
        if start_cost <= k:
            dp[0][start_cost] = grid[0][0]

        for r in range(m):
            for c in range(n):
                if r == 0 and c == 0:
                    continue

                cell_cost = 1 if grid[r][c] > 0 else 0
                cell_score = grid[r][c]

                # New row state to avoid overwriting current row data prematurely
                # If using 1D/2D optimization, we usually update in place or use a temp row
                # Let's keep it simple: we update dp[c][v] using dp[c][v-cost] (from above)
                # and dp[c-1][v-cost] (from left)

                for v in range(k, -1, -1):
                    # Path from above (r-1, c) -> already in dp[c]
                    res_above = -1
                    if r > 0 and v >= cell_cost:
                        res_above = dp[c][v - cell_cost]

                    # Path from left (r, c-1) -> already in dp[c-1]
                    res_left = -1
                    if c > 0 and v >= cell_cost:
                        res_left = dp[c - 1][v - cell_cost]

                    best_prev = max(res_above, res_left)

                    if best_prev != -1:
                        dp[c][v] = best_prev + cell_score
                    else:
                        # If this cell isn't reachable from top or left with this cost
                        # and it's not the start, we must reset it for the new row
                        # Only reset if we didn't just calculate it from the left
                        if r > 0:
                            dp[c][v] = -1 if res_left == -1 else dp[c][v]

        ans = max(dp[n - 1])
        return ans if ans != -1 else -1

if __name__ == '__main__':
    s = Solution()
    print(s.maxPathScore( [[0, 1],[2, 0]], k = 1))
    print(s.maxPathScore( [[0, 1],[1, 2]], k = 1))
    s = Solution1()
    print(s.maxPathScore([[0, 1], [2, 0]], k=1))
    print(s.maxPathScore([[0, 1], [1, 2]], k=1))
