import asyncio
import logging
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup, SoupStrainer

URL = 'https://skillbox.ru/media/'
DEPTH = 5
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


async def get_link(client: aiohttp.ClientSession, url: str = URL, depth: int = DEPTH) -> None:
    async with client.get(url) as response:
        try:
            result = await response.text()
            soup = BeautifulSoup(result, 'html.parser')

            for link in soup.find_all('a'):
                link_str = link.get('href')
                logger.info(f'depth-{depth}, link-{link_str}')
                if link_str is not None and link_str.startswith("http"):
                    await write_to_disk_2(link_str)
                    if depth > 0:
                        await get_link(client, link_str, depth - 1)
        except UnicodeDecodeError as err:
            logger.error(err)


async def get_site(client: aiohttp.ClientSession) -> bytes:
    async with client.get(URL) as response:
        response_result = await response.read()
        result_list = set()
        for link in BeautifulSoup(response_result, parse_only=SoupStrainer('a'), features="html.parser"):
            a: str = link.get('href')
            if a and a.startswith('http'):
                result_list.add(link['href'])
        await asyncio.to_thread(write_to_disk, list(result_list))


def write_to_disk(content):
    file_path = "{}/{}.txt".format(OUT_PATH, 'crawler')
    with open(file_path, mode='wb') as file:
        for row in content:
            file.write(' '.join([row, '\n']).encode('utf-8'))


async def write_to_disk_2(content):
    file_path = "{}/{}.txt".format(OUT_PATH, 'crawler')
    with open(file_path, mode='a') as file:
        file.write(''.join([content, '\n']))


async def get():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as client:
        return await asyncio.gather(get_link(client, depth=0))
        #return await asyncio.gather(get_site(client))

if __name__ == '__main__':
    asyncio.run(get())
