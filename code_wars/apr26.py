def two_sum(numbers, target):
    seen = {}
    for i, n in enumerate(numbers):
        complement = target - n
        if complement in seen:
            # Returns the indices as a single tuple
            return (seen[complement], i)
        seen[n] = i

print(two_sum([1, 2, 3, 4], 4)) # Output: (0, 2)
