import os
import openai
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def webhook():
    try:
        req = request.get_json()

        # Безопасная проверка входа
        if not req or 'request' not in req:
            return jsonify(build_response("Ошибка: пустой запрос."))

        user_utterance = req["request"].get("original_utterance", "").strip()

        if not user_utterance:
            return jsonify(build_response("Привет! Я тебя слушаю. Спроси что-нибудь."))

        # Запрос к OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-4o",  # или gpt-3.5-turbo, если gpt-4o недоступен
            messages=[
                {"role": "system", "content": "Ты голосовой помощник Алисы. Отвечай кратко, дружелюбно и по делу."},
                {"role": "user", "content": user_utterance}
            ]
        )

        answer = completion.choices[0].message.content.strip()

        return jsonify(build_response(answer))

    except Exception:
        # Печатаем ошибку в лог Render
        print("Ошибка GPT:", traceback.format_exc())
        return jsonify(build_response("Произошла ошибка. Попробуй ещё раз."))

def build_response(text):
    return {
        "response": {
            "text": text,
            "tts": text,
            "end_session": False
        },
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
