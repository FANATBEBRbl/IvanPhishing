from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as api_app

# Создаем основное приложение
app = FastAPI(title="Phishing Detection System", version="1.0.0")

# Настройка CORS для работы с клиентом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API приложение
app.mount("/", api_app)

# Эндпоинт для проверки здоровья
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Phishing Detection System is running",
        "models": {
            "shield": "loaded",
            "ivan": "loaded"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
