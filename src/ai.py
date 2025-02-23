from openai import OpenAI
from settings import OPEN_API
from redis_util import get_context, update_context
import html
import logging

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPEN_API,
)


async def ai_request(user_input: str, user_id: int | str) -> str:

    context = await get_context(user_id=user_id)
    # создание промпта и отправка контекста нейросети
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-pro-exp-02-05:free",
            messages=[
                {"role": "system", "content": "Ты умный помощник, отвечай вежливо. Общайся со мной на том языке, на котором тебе придет сообщение. Если ты не знаешь ответа - так и скажи, не оставляй ответ пустым. Прими во внимание контекст"},
                {'role': 'system', 'content': f'Контекст диалога: {context}'}, 
                {"role": "user", "content": user_input}
            ]
        )
        
        #openrouter может вернуть путой ответ
        if not completion or not hasattr(completion, "choices") or not completion.choices:
            logging.error(f"AI response is empty or malformed: {completion}")
            return "Произошла ошибка. Попробуй снова."

        ai_response = completion.choices[0].message.content

        #нейронка так же может не дать ответа
        if ai_response is None:
            logging.error("AI response is None.")
            return "Я не смог сгенерировать ответ. Попробуй задать другой вопрос."

        ai_response = html.escape(completion.choices[0].message.content) # некоторые модели отправляют html контект, телеграм их не распознает
        print(ai_response)
        await update_context(user_id=user_id, user_content=user_input, ai_content=ai_response)
        return ai_response
    
    except Exception as e:
        logging.error(f'an error with AI response: {e}')
        return None 
