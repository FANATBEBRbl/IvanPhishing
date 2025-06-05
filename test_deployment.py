#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования API локально перед развертыванием
"""
import requests
import json

def test_api_locally():
    """Тестирует API локально"""
    base_url = "http://localhost:8000"
    
    print("🧪 ТЕСТИРОВАНИЕ API ЛОКАЛЬНО")
    print("=" * 50)
    
    # Тест 1: Корневой эндпоинт
    print("1. Тестируем корневой эндпоинт...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.json()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 2: Health check
    print("\n2. Тестируем health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.json()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # Тест 3: Проверка сообщения
    print("\n3. Тестируем проверку сообщения...")
    test_message = {
        "message": "Привет! Получите бесплатный приз: https://example.com/prize"
    }
    
    try:
        response = requests.post(
            f"{base_url}/check-message/",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Статус: {response.status_code}")
        result = response.json()
        print(f"   Результат атаки: {result.get('attack_result', 'N/A')}")
        print(f"   Щит: {result.get('shield', {}).get('decision', 'N/A')}")
        print(f"   Иван: {result.get('ivan', {}).get('decision', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")

def test_api_on_render(render_url):
    """Тестирует API на Render"""
    print(f"🌐 ТЕСТИРОВАНИЕ API НА RENDER: {render_url}")
    print("=" * 50)
    
    # Тест корневого эндпоинта
    try:
        response = requests.get(f"{render_url}/")
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("Выберите режим тестирования:")
    print("1. Локальное тестирование (localhost:8000)")
    print("2. Тестирование на Render")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "1":
        test_api_locally()
    elif choice == "2":
        url = input("Введите URL вашего приложения на Render: ").strip()
        test_api_on_render(url)
    else:
        print("Неверный выбор!")
