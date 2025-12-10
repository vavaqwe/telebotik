from google import genai
import config 

client = genai.Client(api_key=config.GEMINI_API_KEY)

SYSTEM_INSTRUCTION = (
    "Ти — доброзичливий та професійний бот підтримки клієнтів з фото-послуг. "
    "Твоя мета — надавати чіткі, корисні та лаконічні відповіді. "
    "Відповідай завжди українською мовою."
)

def ai_response(history): 
    
    generation_config = genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION 
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=history,
            config=generation_config 
        )
        return response.text
    except Exception as e:
        print(f"Помилка при генерації відповіді: {e}")
        return "Вибачте, сталася помилка при обробці запиту."