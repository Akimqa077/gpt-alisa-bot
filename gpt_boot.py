import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def handler():
    try:
        req = request.json
        user_utterance = req['request']['original_utterance']

        if not user_utterance:
            return jsonify(build_response("Я вас слушаю."))

        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты умный помощник, отвечай кратко."},
                {"role": "user", "content": user_utterance}
            ]
        )

        answer = completion.choices[0].message.content
        return jsonify(build_response(answer))

    except Exception as e:
        print("Error:", e)
        return jsonify(build_response("Произошла ошибка."))

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
