import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def handler():
    try:
        data = request.json
        user_input = data["request"].get("original_utterance", "")

        # Если пользователь ничего не сказал — приветствие
        if not user_input.strip():
            return jsonify(build_response("Привет! Я тебя слушаю. Спроси что-нибудь."))

        # Запрос к ChatGPT
        chat_response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты умный голосовой помощник Алисы. Отвечай кратко, по делу и дружелюбно."},
                {"role": "user", "content": user_input}
            ]
        )

        answer = chat_response.choices[0].message.content.strip()
        return jsonify(build_response(answer))

    except Exception as e:
        print("Ошибка:", e)
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
