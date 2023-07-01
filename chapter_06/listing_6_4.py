import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f"Finished counting to {count_to} in {end - start}")
    return counter

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        numbers = [1, 3, 5, 22, 100_000_000]
        """
        if 100_000_000 will be first in the list
        then `print(result)` will stuck until it completes!

        `.map` gives us iterator with deterministic order
        """
        for result in pool.map(count, numbers):
            print(result)