import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    try:
        req = request.json
        utterance = req["request"].get("original_utterance", "").strip()

        # Если пользователь ничего не сказал
        if not utterance:
            return make_response("Привет! Я тебя слушаю. Спроси что-нибудь.")

        # Заглушка (ответ без GPT, но работает стабильно)
        reply = f"Ты сказал: {utterance}"
        return make_response(reply)

    except Exception as e:
        print("Ошибка:", e)
        return make_response("Произошла ошибка. Попробуй ещё раз.")

def make_response(text):
    return {
        "response": {
            "text": text[:1024],
            "tts": text[:1024],  # Чтобы Алиса проговаривала голосом
            "end_session": False
        },
        "version": "1.0"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
