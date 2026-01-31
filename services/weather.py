from .base import BaseService, classproperty
import python_weather
import asyncio


class Weather(BaseService):

    async def get_weather(self, city):
        # Создаем клиент (imperial=False для градусов Цельсия)
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)
            
            output = {
                "temperature": f"{weather.temperature}°C",
                "description": f"{weather.description}"
            }
            return output
        
    def handle(self, city_name="Kyiv"):
        result = asyncio.run(self.get_weather(city_name))
        return result
    
    @classproperty
    def info(cls):
        return """
            This module get weather info
            not requare key argument:
            city_name - name have to be in english
        """