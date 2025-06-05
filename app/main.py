from fastapi import FastAPI
from .models import is_phishing, will_click
from .schemas import MessageRequest

app = FastAPI()

@app.post("/check-message/")
async def check_message(request: MessageRequest):
    # Теперь анализируем всё сообщение целиком
    full_text = request.message
    
    # Получаем детальные результаты
    shield_result = is_phishing(full_text)
    ivan_result = will_click(full_text)
    success = not shield_result["это_фишинг"] and ivan_result["будет_кликать"]
    
    return {
        "message": request.message,
        "success": success,
        "shield": {
            "status": "DANGER" if shield_result["это_фишинг"] else "SAFE",
            "details": shield_result
        },
        "ivan": {
            "status": "CLICK" if ivan_result["будет_кликать"] else "IGNORE",
            "details": ivan_result
        }
    }