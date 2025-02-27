from aiohttp import ClientSession
from config import settings


async def get_weather_data(city: str = "Moscow"):
    async with ClientSession() as session:
        async with session.get(url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.OPENWEATHER_KEY}') as resp:
            if resp.status != 200:
                return False
            return (await resp.json())['main']
