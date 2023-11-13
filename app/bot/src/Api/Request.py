import aiohttp

from config import BASE_API_URL


class Request:
    @staticmethod
    async def get(url, params: dict=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_API_URL + url, params=params) as resp:
                response = await resp.json()
                return response

    @staticmethod
    async def post(url, body=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_API_URL + url, json=dict(body)) as resp:
                response = await resp.json()
                return response
    
    @staticmethod
    async def put(url, body=None):
        async with aiohttp.ClientSession() as session:
            async with session.put(BASE_API_URL + url, json=dict(body)) as resp:
                response = await resp.json()
                return response
