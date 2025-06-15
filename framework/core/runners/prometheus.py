# 使用Prometheus异步客户端
from aioprometheus import Counter
REQS = Counter('http_requests', 'Total requests')

async def monitored_request(url):
    REQS.inc()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp.status