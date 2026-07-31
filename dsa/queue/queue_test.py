import timeit
from collections import deque


def benchmark_queue():
    test_data = ["Spark-Job-ID-"] * 1000

    # Simulate the same workload as Go
    q = deque()
    for item in test_data:
        q.append(item)
    while q:
        q.popleft()


# Run it 84,282 times to match your Go "b.N" result
iterations = 84282
total_time = timeit.timeit(benchmark_queue, number=iterations)
print(f"Python average: {(total_time / iterations) * 1e9:.0f} ns/op")