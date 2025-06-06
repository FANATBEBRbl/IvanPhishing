import streamlit as st
import requests
import re

st.title("Фишинг-атака: Проверка письма")

# Одно поле для сообщения с ссылкой
message = st.text_area("Сообщение (должно содержать ссылку):", height=200)

def contains_link(text):
    """Проверяет наличие ссылки в тексте"""
    url_pattern = r'https?://[^\s]+'
    return bool(re.search(url_pattern, text))

if st.button("🚀 Отправить сообщение"):
    if message:
        if contains_link(message):
            try:
                response = requests.post(
                    "http://localhost:8000/check-message/",
                    json={"message": message}
                )
                result = response.json()
                
                # Отображение результатов с деталями
                if result["success"]:
                    st.success("✅ Успех! Сообщение прошло проверку!")
                else:
                    st.error("❌ Сообщение заблокировано")
                
                # Детали щита
                st.subheader("🛡️ Умный Щит")
                shield_details = result["shield"]["details"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Статус", result["shield"]["status"])
                    st.metric("Подозрительность", f"{shield_details['suspicion_score']}/100")
                with col2:
                    if shield_details["found_hard_triggers"]:
                        st.error(f"🚨 Жесткие триггеры: {', '.join(shield_details['found_hard_triggers'])}")
                    if shield_details["found_soft_triggers"]:
                        st.warning(f"⚠️ Мягкие триггеры: {', '.join(shield_details['found_soft_triggers'])}")
                with col3:
                    st.write(f"**Угрожающий тон:** {'⚠️' if shield_details['is_threatening'] else '✅'}")
                    st.write(f"**Токсичность:** {'⚠️' if shield_details['is_toxic'] else '✅'}")
                    st.write(f"**Подозрительный URL:** {'⚠️' if shield_details['has_suspicious_url'] else '✅'}")
                
                # Детали Умного Ивана
                st.subheader("🧠 Умный Иван")
                ivan_details = result["ivan"]["details"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Решение", result["ivan"]["status"])
                    st.metric("Вероятность клика", f"{ivan_details['click_probability']}%")
                    st.metric("Эмоция", ivan_details["emotion_detected"])
                
                with col2:
                    st.write("**Психологические триггеры:**")
                    triggers = ivan_details["psychological_triggers"]
                    for trigger, active in triggers.items():
                        st.write(f"• {trigger}: {'✅' if active else '❌'}")
                
                with col3:
                    st.write("**Негативные факторы:**")
                    negatives = ivan_details["negative_factors"]
                    for factor, active in negatives.items():
                        st.write(f"• {factor}: {'❌' if active else '✅'}")
                
                # Найденные призывы к действию
                actions = ivan_details["action_calls"]
                if any(actions.values()):
                    st.info("**Найдены призывы к действию:**")
                    for category, phrases in actions.items():
                        if phrases:
                            st.write(f"• {category}: {', '.join(phrases)}")
                
                # JSON для разработчика
                with st.expander("🔍 Полный JSON ответ"):
                    st.json(result)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Не удается подключиться к серверу. Убедитесь, что FastAPI запущен на localhost:8000")
            except Exception as e:
                st.error(f"❌ Ошибка: {str(e)}")
        else:
            st.warning("⚠️ Сообщение должно содержать ссылку (http:// или https://)")
    else:
        st.warning("⚠️ Введите сообщение")