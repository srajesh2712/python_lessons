from typing import List


class Solution:
    def maximumScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # 1. Prefix Sums
        ps = [[0] * n for _ in range(n + 1)]
        for j in range(n):
            for i in range(n):
                ps[i + 1][j] = ps[i][j] + grid[i][j]

        # States: max score at column j-1 with height h
        # dec: we just came from a taller or equal height (prev >= current)
        # inc: we just came from a shorter height (prev < current)
        dec = [0] * (n + 1)
        inc = [0] * (n + 1)

        for j in range(1, n):
            next_dec = [0] * (n + 1)
            next_inc = [0] * (n + 1)

            # --- PRE-CALCULATIONS ---
            # For next_inc[h]: we need max(dec[h_prev] - ps[h_prev][j-1]) where h_prev < h
            # This handles the "Rise" part of a mountain.
            prefix_inc = -float('inf')

            # For next_dec[h]: we need max(dec[h_prev] + ps[h_prev][j]) where h_prev > h
            # This handles the "Fall" part and the "Valley" scoring.
            suffix_dec = -float('inf')

            # 1. Calculate next_inc (Growing the mountain)
            for h in range(n + 1):
                next_inc[h] = prefix_inc + ps[h][j - 1]
                # Update prefix for the next height: use best of existing mountain or a new valley start
                prefix_inc = max(prefix_inc, dec[h] - ps[h][j - 1], inc[h] - ps[h][j - 1])

            # 2. Calculate next_dec (Falling into the valley)
            for h in range(n, -1, -1):
                next_dec[h] = max(suffix_dec - ps[h][j], (inc[h] if j > 1 else dec[h]))
                # Update suffix: best score from a taller wall to our left
                suffix_dec = max(suffix_dec, dec[h] + ps[h][j], inc[h] + ps[h][j])

            dec, inc = next_dec, next_inc

        return max(max(dec), max(inc))


if __name__ == '__main__':
    s = Solution()
    # This correctly returns 94
    print(s.maximumScore([[10, 9, 0, 0, 15], [7, 1, 0, 8, 0], [5, 20, 0, 11, 0], [0, 0, 0, 1, 2], [8, 12, 1, 10, 3]]))