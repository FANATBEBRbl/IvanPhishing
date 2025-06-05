from transformers import pipeline
import re
import random

# === УМНЫЙ ШИТ ===
shield_phishing_model = pipeline("text-classification", model="martin-ha/toxic-comment-model")
shield_sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def is_phishing(text: str) -> dict:
    """Продвинутый анализ на фишинг с несколькими слоями защиты"""
    
    # 1. ЖЕСТКИЕ ТРИГГЕРЫ (всегда блокируют)
    hard_triggers = ["пароль", "аккаунт", "http://", "логин", "данные карты"]
    found_hard = [t for t in hard_triggers if re.search(rf'\b{t}\b', text.lower())]
    
    # 2. МЯГКИЕ ТРИГГЕРЫ (повышают подозрительность)
    soft_triggers = ["срочно", "немедленно", "истекает", "заблокирован", "подтвердите"]
    found_soft = [t for t in soft_triggers if re.search(rf'\b{t}\b', text.lower())]
    
    # 3. АНАЛИЗ ТОНАЛЬНОСТИ (подозрительно негативные сообщения)
    try:
        sentiment = shield_sentiment_model(text)[0]
        is_threatening = (sentiment["label"] == "LABEL_0" and sentiment["score"] > 0.7)  # NEGATIVE
    except:
        threatening_words = ["потеряете", "заблокируем", "удалим", "прекратим"]
        is_threatening = any(word in text.lower() for word in threatening_words)
    
    # 4. АНАЛИЗ ТОКСИЧНОСТИ
    try:
        toxicity = shield_phishing_model(text)[0]
        is_toxic = toxicity["label"] == "TOXIC" and toxicity["score"] > 0.5
    except:
        is_toxic = False
    
    # 5. ПРОВЕРКА URL ПАТТЕРНОВ
    suspicious_domains = ["bit.ly", "tinyurl", "goo.gl", "t.co"]
    has_suspicious_url = any(domain in text.lower() for domain in suspicious_domains)
    
    # 6. АНАЛИЗ ГРАММАТИКИ (фишинг часто с ошибками)
    grammar_errors = len(re.findall(r'\b[а-я]+[A-Z][а-я]*\b', text))  # смешанный регистр
    poor_grammar = grammar_errors > 2
    
    # ИТОГОВОЕ РЕШЕНИЕ С ВЕСАМИ
    suspicion_score = 0
    reasons = []
    
    if found_hard:
        suspicion_score += 100  # Автоблок
        reasons.append("hard_triggers")
    
    if found_soft:
        suspicion_score += len(found_soft) * 15
        reasons.append("soft_triggers")
    
    if is_threatening:
        suspicion_score += 25
        reasons.append("threatening_tone")
    
    if is_toxic:
        suspicion_score += 30
        reasons.append("toxic_content")
    
    if has_suspicious_url:
        suspicion_score += 20
        reasons.append("suspicious_url")
    
    if poor_grammar:
        suspicion_score += 10
        reasons.append("poor_grammar")
    
    # Добавляем случайность (человеческий фактор)
    suspicion_score += random.randint(-5, 5)
    
    is_phishing_result = suspicion_score >= 50
    return {
        "это_фишинг": is_phishing_result,
        "балл_подозрительности": min(suspicion_score, 100),
        "найденные_жесткие_триггеры": found_hard,
        "найденные_мягкие_триггеры": found_soft,
        "угрожающий_тон": is_threatening,
        "токсичный": is_toxic,
        "подозрительный_урл": has_suspicious_url,
        "плохая_грамматика": poor_grammar,
        "причины": reasons,
        "уверенность_модели": min(suspicion_score / 100, 1.0)
    }

# === УМНЫЙ ИВАН С ФИКСОМ ЭМОЦИЙ ===
ivan_sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def analyze_emotions_russian(text: str) -> dict:
    """Анализ эмоций для русского текста на основе ключевых слов"""
    
    # Словари эмоций на русском
    joy_words = ["поздравляем", "выиграли", "радость", "счастье", "отлично", "супер", "замечательно", "приз"]
    surprise_words = ["удивительно", "невероятно", "сюрприз", "неожиданно", "сенсация", "шок"]
    fear_words = ["опасность", "угроза", "заблокирован", "потеряете", "удалим", "прекратим", "внимание"]
    anger_words = ["возмущены", "недовольны", "жалоба", "нарушение", "штраф"]
    
    text_lower = text.lower()
    
    # Подсчет совпадений
    joy_score = sum(1 for word in joy_words if word in text_lower)
    surprise_score = sum(1 for word in surprise_words if word in text_lower)
    fear_score = sum(1 for word in fear_words if word in text_lower)
    anger_score = sum(1 for word in anger_words if word in text_lower)
    
    # Определяем доминирующую эмоцию
    scores = {
        "joy": joy_score,
        "surprise": surprise_score, 
        "fear": fear_score,
        "anger": anger_score
    }
    
    dominant_emotion = max(scores, key=scores.get)
    max_score = scores[dominant_emotion]
    
    # Если нет явных эмоций - нейтрально
    if max_score == 0:
        dominant_emotion = "neutral"
        confidence = 0.5
    else:
        confidence = min(max_score * 0.3 + 0.4, 1.0)  # Масштабируем 0.4-1.0
    
    return {
        "emotion": dominant_emotion,
        "confidence": confidence,
        "scores": scores
    }

def will_click(text: str) -> dict:
    """Продвинутый анализ вероятности клика с исправленным анализом эмоций"""
    
    # 1. ЭМОЦИОНАЛЬНЫЙ АНАЛИЗ (исправлен для русского языка)
    emotion_analysis = analyze_emotions_russian(text)
    emotions = {
        "joy": emotion_analysis["emotion"] == "joy" and emotion_analysis["confidence"] > 0.6,
        "surprise": emotion_analysis["emotion"] == "surprise" and emotion_analysis["confidence"] > 0.5,
        "fear": emotion_analysis["emotion"] == "fear" and emotion_analysis["confidence"] > 0.5
    }
    
    # 2. ПСИХОЛОГИЧЕСКИЕ ТРИГГЕРЫ
    curiosity_words = ["секрет", "тайна", "эксклюзив", "только для вас", "узнайте"]
    has_curiosity = any(word in text.lower() for word in curiosity_words)
    
    urgency_words = ["сегодня", "сейчас", "скоро истекает", "последний шанс", "только до"]
    has_urgency = any(word in text.lower() for word in urgency_words)
    
    social_proof = ["тысячи людей", "все уже", "присоединяйтесь", "популярно"]
    has_social_proof = any(word in text.lower() for word in social_proof)
    
    authority_words = ["банк", "официально", "государство", "министерство"]
    has_authority = any(word in text.lower() for word in authority_words)
    
    # 3. ВЫГОДА И ПРЕДЛОЖЕНИЯ
    financial_benefit = ["бесплатно", "скидка", "выигрыш", "деньги", "приз", "кэшбек"]
    has_financial_benefit = any(word in text.lower() for word in financial_benefit)
    
    # 4. ПЕРСОНАЛИЗАЦИЯ
    personal_words = ["ваш", "для вас", "персонально", "именно вам"]
    is_personalized = any(word in text.lower() for word in personal_words)
    
    # 5. ПРИЗЫВЫ К ДЕЙСТВИЮ
    action_phrases = {
        "click": ["нажмите", "кликните", "перейдите", "тапните"],
        "check": ["проверьте", "посмотрите", "узнайте", "откройте"],
        "claim": ["получите", "заберите", "активируйте", "воспользуйтесь"],
        "verify": ["подтвердите", "верифицируйте", "обновите"]
    }
    
    found_actions = {}
    for category, phrases in action_phrases.items():
        found_actions[category] = [p for p in phrases if p in text.lower()]
    
    has_any_action = any(found_actions.values())
    
    # 6. АНТИ-ПАТТЕРНЫ
    boring_words = ["уведомление", "рассылка", "техническая", "регламент", "политика"]
    spam_words = ["реклама", "предложение", "акция", "распродажа"]
    
    is_boring = any(word in text.lower() for word in boring_words)
    looks_like_spam = any(word in text.lower() for word in spam_words)
    
    # 7. РАСЧЕТ ВЕРОЯТНОСТИ КЛИКА
    click_score = 0
    factors = {}
    
    # Позитивные факторы
    if emotions["joy"]: 
        click_score += 25
        factors["joy_emotion"] = True
    if emotions["surprise"]: 
        click_score += 20
        factors["surprise_element"] = True
    if has_curiosity: 
        click_score += 30
        factors["curiosity_trigger"] = True
    if has_urgency: 
        click_score += 25
        factors["urgency_trigger"] = True
    if has_financial_benefit: 
        click_score += 35
        factors["financial_benefit"] = True
    if has_social_proof: 
        click_score += 15
        factors["social_proof"] = True
    if has_authority: 
        click_score += 20
        factors["authority"] = True
    if is_personalized: 
        click_score += 15
        factors["personalized"] = True
    if has_any_action: 
        click_score += 20
        factors["clear_action"] = True
    
    # Негативные факторы
    if is_boring: 
        click_score -= 40
        factors["boring_content"] = True
    if looks_like_spam: 
        click_score -= 25
        factors["spam_like"] = True
    if emotions["fear"]: 
        click_score -= 15
        factors["fear_emotion"] = True
    
    # Человеческий фактор
    mood_modifier = random.randint(-10, 10)
    click_score += mood_modifier
      # Финальное решение
    will_click_result = click_score >= 50
    
    return {
        "будет_кликать": will_click_result,
        "вероятность_клика": min(max(click_score, 0), 100),
        "обнаруженная_эмоция": emotion_analysis["emotion"],
        "уверенность_эмоции": round(emotion_analysis["confidence"], 3),
        "баллы_эмоций": emotion_analysis["scores"],
        "психологические_триггеры": {
            "любопытство": has_curiosity,
            "срочность": has_urgency,
            "социальное_доказательство": has_social_proof,
            "авторитет": has_authority,
            "финансовая_выгода": has_financial_benefit,
            "персонализация": is_personalized
        },
        "призывы_к_действию": found_actions,
        "негативные_факторы": {
            "скучное": is_boring,
            "похоже_на_спам": looks_like_spam,
            "вызывает_страх": emotions["fear"]
        },
        "факторы_решения": factors,
        "модификатор_настроения": mood_modifier
    }