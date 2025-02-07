from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Данные прокси
PROXY_HOST = "45.118.250.2"
PROXY_PORT = "8000"
PROXY_USER = "B01vby"
PROXY_PASS = "GBno0x"

# Формируем строку прокси
PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

# Прокси для HTTP и HTTPS
PROXIES = {
    "http": PROXY_URL,
    "https": PROXY_URL,
}


# CORS Middlware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Заголовки запроса
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-CA,en-US;q=0.9,en;q=0.8",
    "Origin": "http://www.encar.com",
    "Priority": "u=3, i",
    "Referer": "http://www.encar.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
}

ENCAR_API_URL = "https://api.encar.com"


@app.get("/carlist")
async def get_car_list(car_type: str = "korean", page: int = 1, limit: int = 20):
    """Получение списка автомобилей с Encar через FastAPI"""
    try:
        if car_type == "korean":
            api_url = f"{ENCAR_API_URL}/search/car/list/general?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C0%7C20&page={page}&limit={limit}"
        else:
            api_url = f"{ENCAR_API_URL}/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.N.)&sr=%7CModifiedDate%7C0%7C20&page={page}&limit={limit}"

        response = requests.get(api_url, headers=HEADERS, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ProxyError:
        raise HTTPException(
            status_code=500, detail="❌ Ошибка прокси! Возможно, прокси не работает."
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=500,
            detail="❌ Таймаут! Прокси слишком медленный или Encar заблокировал IP.",
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"❌ Ошибка запроса к API Encar: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    import os

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
