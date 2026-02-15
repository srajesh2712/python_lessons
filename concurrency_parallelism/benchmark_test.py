import time
from concurrent.futures.process import ProcessPoolExecutor


def heavy_math(n):
    return sum( i*i for i in range(n) )

def run_sequential(n):
    start = time.perf_counter()
    for i in range(n):
        heavy_math(10_000_000)
    end = time.perf_counter()
    return end - start
def run_parallel(n):
    start = time.perf_counter()
    tasks = [10_000_000]*n
    with ProcessPoolExecutor(max_workers=4) as executor:
            results = executor.map(heavy_math,tasks)

    try:
        for r in results:
            print(r)
    except Exception as e:
        print(f"One of the processes failed with: {e}")
    end = time.perf_counter()
    return end - start
if __name__ == '__main__':
    print(run_sequential(4))
    print(run_parallel(4))
