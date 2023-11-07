import requests
import aiohttp

from config import BASE_API_URL


class Request:
    @staticmethod
    def get(url, headers=None):
        response = requests.post(BASE_API_URL + url, headers=headers)
        return response.json()

    @staticmethod
    async def post(url, body=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(BASE_API_URL + url, json=dict(body)) as resp:
                response = await resp.json()
                return response