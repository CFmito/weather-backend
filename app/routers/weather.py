from fastapi import APIRouter, HTTPException, Depends
from redis.asyncio import Redis
from app.services.weather import get_weather_by_city

router = APIRouter(prefix="/api/v1", tags=["Weather"])

# Простая функция получения Redis клиента
async def get_redis():
    client = Redis(host="redis", port=6379, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()

@router.get("/weather")
async def read_weather(city: str, redis_client: Redis = Depends(get_redis)):
    try:
        return await get_weather_by_city(city, redis_client)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка получения данных о погоде")