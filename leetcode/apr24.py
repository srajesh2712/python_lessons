import itertools
from collections import Counter


class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        char_map = Counter(moves)
        result = abs(char_map['L']-char_map['R'])
        return result +char_map['_']


if __name__ == '__main__':
    s = Solution()
    print(s.furthestDistanceFromOrigin("L_RL__R"))