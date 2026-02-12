import threading
import time

def task_worker(name, delay):
    print(f"Thread {name}: Starting...")
    time.sleep(delay)
    print(f"Thread {name}: Finished after {delay}s")

def threads_python():
    # 1. Create the Thread objects
    # target = the function to run, args = the inputs for that function
    t1 = threading.Thread(target=task_worker, args=("Browser-Scan", 2))
    t2 = threading.Thread(target=task_worker, args=("HDFS-Upload", 4))

    # 2. Start the threads
    t1.start()
    t2.start()

    # 3. Wait for them to finish (Optional, but recommended)
    t1.join()
    t2.join()

    print("All threads are done!")


# We set a very small interval to force the interpreter
# to switch threads frequently (default is 0.005 seconds)
import sys
sys.setswitchinterval(0.005)


def heavy_math(name, iterations):
    print(f"Thread {name}: Starting heavy calculation...")
    counter = 0
    for i in range(iterations):
        # This is pure CPU work. No sleeping!
        counter += 1
        # Every 25 million iterations, let us know we are still alive
        if i % 25_000_000 == 0:
            print(f"Thread {name}: Reached {i}...")

    print(f"Thread {name}: FINISHED with counter at {counter}")

def preemptive_multitasking():
    # 1. Create threads for heavy math
    # These threads will "fight" for the GIL
    t1 = threading.Thread(target=heavy_math, args=("Math-A", 100_000_000))
    t2 = threading.Thread(target=heavy_math, args=("Math-B", 100_000_000))

    start_time = threading.Timer(0, lambda: None)  # Just for timing reference

    # 2. Start the threads
    t1.start()
    t2.start()

    # 3. Wait for finish
    t1.join()
    t2.join()

    print("All CPU-bound threads are done!")

if __name__ == '__main__':
    preemptive_multitasking()