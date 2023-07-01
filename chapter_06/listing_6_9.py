import asyncio
import concurrent.futures
import functools
import time
from chapter_06.listing_6_8 import partition, merged_dictionaries, map_frequencies


async def reduce(loop, pool, counters, chunk_size) -> dict[str, int]:
    chunks: list[list[dict]] = list(partition(counters, chunk_size))
    reducers = []
    while len(chunks[0]) > 1: # while not single dictionary
        for chunk in chunks:
            reducer = functools.partial(functools.reduce, merged_dictionaries, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunks: list[dict] = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]

async def main(partition_size: int):
    with open("chapter_06/googlebooks-eng-all-1gram-20120701-a", encoding="utf-8") as f:
        contents = f.readlines()

        loop = asyncio.get_event_loop()
        tasks = []
        with concurrent.futures.ProcessPoolExecutor() as pool:
            start = time.time()
            
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)
                    )
                )
            
            intermediate_results: list[dict] = await asyncio.gather(*tasks)
            final_result = await reduce(loop, pool, intermediate_results, 500)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")

            end = time.time()
            print(f"MapReduce took: {end - start:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
