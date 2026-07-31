def longest(a1, a2):
    charset = set()

    [charset.add(char) for char in a1]
    [charset.add(char) for char in a2]

    return "".join(sorted(charset))

a = "xyaabbbccccdefww"
b = "xxxxyyyyabklmopq"
#longest(a, b) -> "abcdefklmopqwxy"
print(longest(a, b))