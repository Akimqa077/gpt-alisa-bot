import os
from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

@app.route("/", methods=["POST"])
def handler():
    try:
        req = request.json
        utterance = req.get("request", {}).get("original_utterance", "")

        # Если пользователь ничего не сказал
        if not utterance.strip():
            return jsonify(build_response("Привет! Я тебя слушаю. Задай мне любой вопрос."))

        # GPT-4o запрос
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты голосовой помощник Алисы. Отвечай коротко и понятно."},
                {"role": "user", "content": utterance}
            ]
        )
        answer = completion.choices[0].message.content.strip()
if not answer:
    answer = "Я не смог ничего ответить. Попробуй переформулировать вопрос."


        return jsonify(build_response(answer))

    except Exception as e:
        print("Ошибка:", e)
        return jsonify(build_response("Произошла ошибка. Попробуй ещё раз."))

def build_response(text):
    return {
        "response": {
            "text": text,
            "end_session": False
        },
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
