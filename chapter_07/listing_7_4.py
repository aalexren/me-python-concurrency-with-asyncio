import time
import requests
from concurrent.futures import ThreadPoolExecutor


def get_status_code(url: str) -> int:
    respnonse = requests.get(url)
    return respnonse.status_code

start = time.time()

with ThreadPoolExecutor() as pool:
    urls = ["https://example.com" for i in range(1000)]
    results = pool.map(get_status_code, urls)
    for result in results:
        print(result)

end = time.time()

print(f"Finished requests in {end - start:.4f} second(s)")