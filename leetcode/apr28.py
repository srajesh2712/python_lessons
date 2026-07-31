from typing import List
import itertools
class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        result =  sorted(itertools.chain.from_iterable(grid))
        n = len(result)
        median = result[n // 2]
        first_rem = result[0] % x
        count = 0
        for val in result:
            if val % x != first_rem: return -1
            count +=abs(val - median) // x
        return count
if __name__ == '__main__':
    s = Solution()
    print(s.minOperations(grid=[[1,2,3],[4,5,6],[7,8,9]],x=2))
    print(s.minOperations(grid=[[2, 4], [6, 8]], x=2))