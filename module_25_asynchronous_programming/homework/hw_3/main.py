import asyncio
from pathlib import Path
import aiohttp
from bs4 import BeautifulSoup, SoupStrainer

URL = 'https://skillbox.ru/media/'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


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


async def get():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(30)) as client:
        return await asyncio.gather(get_site(client))


if __name__ == '__main__':
    asyncio.run(get())
