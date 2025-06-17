from multiprocessing import Pool
import asyncio
import aiohttp

async def async_worker(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

def process_worker(url):
    asyncio.run(async_worker(url))

if __name__ == '__main__':
    with Pool(4) as p:
        p.map(process_worker, ["http://api.example.com"]*1000)