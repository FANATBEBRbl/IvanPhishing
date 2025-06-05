#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный файл для запуска FastAPI приложения на Render
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import is_phishing, will_click
from app.schemas import MessageRequest
import os

# Создаем FastAPI приложение
app = FastAPI(
    title="AI/ML Phishing Detection System",
    description="Система обхода AI/ML моделей для фишинг-атак",
    version="1.0.0"
)

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API"""
    return {
        "message": "🛡️ AI/ML Phishing Detection System is running!",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "check_message": "/check-message/",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {
        "status": "healthy",
        "service": "phishing-detector",
        "timestamp": "2025-06-05"
    }

@app.post("/check-message/")
async def check_message(request: MessageRequest):
    """
    Проверка сообщения на фишинг
    
    Анализирует сообщение двумя моделями:
    - Щит: определяет, является ли сообщение фишингом
    - Иван: определяет, кликнет ли пользователь на ссылку
    """
    try:
        # Анализируем всё сообщение целиком
        full_text = request.message
        
        # Получаем детальные результаты
        shield_result = is_phishing(full_text)
        ivan_result = will_click(full_text)
        
        # Определяем успех атаки
        success = not shield_result["это_фишинг"] and ivan_result["будет_кликать"]
        
        return {
            "message": request.message,
            "success": success,
            "attack_result": "🚀 УСПЕХ!" if success else "💥 ПРОВАЛ",
            "shield": {
                "status": "DANGER" if shield_result["это_фишинг"] else "SAFE",
                "decision": "❌ БЛОКИРУЕТ" if shield_result["это_фишинг"] else "✅ ПРОПУСКАЕТ",
                "details": shield_result
            },
            "ivan": {
                "status": "CLICK" if ivan_result["будет_кликать"] else "IGNORE", 
                "decision": "✅ КЛИКНЕТ" if ivan_result["будет_кликать"] else "❌ НЕ КЛИКНЕТ",
                "details": ivan_result
            },
            "api_version": "1.0.0"
        }
    except Exception as e:
        return {
            "error": f"Ошибка обработки: {str(e)}",
            "success": False,
            "message": request.message
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port,
        reload=False  # В продакшене отключаем reload
    )
