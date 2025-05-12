import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def handler():
    try:
        req = request.json
        version = req.get("version", "1.0")

        user_utterance = req.get("request", {}).get("original_utterance", "")

        if not user_utterance:
            return jsonify(build_response("Привет! Я тебя слушаю.", version))

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты голосовой помощник Алисы. Отвечай кратко, по делу и дружелюбно."},
                {"role": "user", "content": user_utterance}
            ]
        )

        answer = completion.choices[0].message.content
        return jsonify(build_response(answer, version))

    except Exception as e:
        print("Ошибка:", e)
        return jsonify(build_response("Произошла ошибка. Попробуй ещё раз.", "1.0"))

def build_response(text, version):
    return {
        "response": {
            "text": text,
            "end_session": False
        },
        "version": version
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
