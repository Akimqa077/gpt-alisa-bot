from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def webhook():
    req = request.json

    user_message = req['request']['original_utterance']

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    answer = response['choices'][0]['message']['content']

    return jsonify({
        "version": req['version'],
        "session": req['session'],
        "response": {
            "text": answer,
            "end_session": False
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
