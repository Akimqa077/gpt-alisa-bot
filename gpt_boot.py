import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handler():
    try:
        req = request.json
        user_utterance = req["request"].get("original_utterance", "").strip()

        if not user_utterance:
            return jsonify(build_response("Привет! Я тебя слушаю. Задай мне любой вопрос."))

        # ВРЕМЕННЫЙ ответ (заглушка без GPT)
        return jsonify(build_response(f"Ты сказал: {user_utterance}"))

    except Exception as e:
        print("Ошибка:", e)
        return jsonify(build_response("Произошла ошибка. Попробуй ещё раз."))


def build_response(text):
    print("Ответ для Алисы:", text)
    return {
        "response": {
            "text": text[:1024],  # Ограничение на длину ответа
            "end_session": False
        },
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
