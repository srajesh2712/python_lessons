import timeit

from dsa.stack.stack import reverse_string_slow, reverse_string_fast

# Benchmark Setup
test_data = "gninraeL nIdekniL htiw tol a nraeL" * 1000 # Make it longer to see the gap

# Running the benchmark 1000 times
slow_time = timeit.timeit(lambda: reverse_string_slow(test_data), number=1000)
fast_time = timeit.timeit(lambda: reverse_string_fast(test_data), number=1000)

print(f"Slow version: {slow_time:.5f} seconds")
print(f"Fast version: {fast_time:.5f} seconds")