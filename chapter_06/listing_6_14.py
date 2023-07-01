import asyncio
import functools
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor
from chapter_06.listing_6_8 import partition, merged_dictionaries

map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies(chunk: list[str]) -> dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split("\t")
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f"Finished {map_progress.value} / {total_partitions} map operations")
        await asyncio.sleep(1)


async def main(partition_size: int):
    global map_progress

    with open("chapter_06/googlebooks-eng-all-1gram-20120701-a", encoding="utf-8") as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value("i", 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress,)) as pool:
            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)
                    )
                )

            counters = await asyncio.gather(*tasks)

            await reporter

            final_result = functools.reduce(merged_dictionaries, counters)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
