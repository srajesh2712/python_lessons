import numpy as np
import time
from mathwonder import fast_threshold

# 1. Create a large "SAR image" (10 million pixels)
size = 10_000_000
data_python = np.random.rand(size).astype(np.float32)
data_c = data_python.copy()

print(f"Benchmarking with {size:,} pixels...\n")

# --- Test 1: Pure Python Loop ---
start = time.time()
for i in range(len(data_python)):
    if data_python[i] > 0.5:
        data_python[i] = 255.0
    else:
        data_python[i] = 0.0
python_time = time.time() - start
print(f"Pure Python Loop: {python_time:.4f} seconds")

# --- Test 2: Your C-Extension ---
start = time.time()
fast_threshold(data_c, 0.5)
c_time = time.time() - start
print(f"Your C-Extension: {c_time:.4f} seconds")

# --- Result ---
speedup = python_time / c_time
print(f"\nResult: Your C-code is {speedup:.1f}x faster than Python!")