import asyncio
import logging
import time
from pathlib import Path

import aiofiles
import aiohttp

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        logging.info(response.status)
        result = await response.read()
        await asyncio.to_thread(write_to_disk, result, idx)


def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
         f.write(content)


async def get_all_cats():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    res = asyncio.run(get_all_cats())
    logging.info(len(res))


if __name__ == '__main__':
    start = time.time()
    logging.info(f"START {start}")
    main()
    stop = time.time() - start
    logging.info(f"Time {stop}")