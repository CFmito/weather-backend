import json
import httpx
from redis.asyncio import Redis

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

async def get_weather_by_city(city_name: str, redis_client: Redis) -> dict:
    cache_key = f"weather:{city_name.lower().strip()}"
    
    # Проверка Redis
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    async with httpx.AsyncClient() as client:
        # 1. Поиск координат
        geo_res = await client.get(GEOCODING_URL, params={"name": city_name, "count": 1, "language": "ru"})
        geo_data = geo_res.json()
        
        if not geo_data.get("results"):
            raise ValueError(f"Город '{city_name}' не найден")
            
        location = geo_data["results"][0]
        lat, lon, resolved_name = location["latitude"], location["longitude"], location["name"]

        # 2. Погода по координатам
        weather_res = await client.get(
            WEATHER_URL, 
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        )
        weather_data = weather_res.json()
        current = weather_data.get("current_weather", {})

        result = {
            "city": resolved_name,
            "latitude": lat,
            "longitude": lon,
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "weathercode": current.get("weathercode"),
            "time": current.get("time")
        }

        # 3. Запись в Redis (TTL 10 минут)
        await redis_client.set(cache_key, json.dumps(result), ex=600)
        return result