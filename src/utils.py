from aiohttp import ClientSession
# from src.config import settings


async def get_geodata(city: str = "Moscow"):
    async with ClientSession() as session:
        async with session.get(url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=745bd42cd3530c339c5663ba349fa1c8') as resp:
            if resp.status != 200:
                return False
            return await resp.json()
