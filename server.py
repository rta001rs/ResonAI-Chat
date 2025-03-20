from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
run_with_ngrok(app)  # Enables external access

MAX_HISTORY = 5
conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Please provide a valid message."})

    # Maintain conversation history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history = conversation_history[-MAX_HISTORY:]

    try:
        response = ollama.chat(
            model="mistral",
            messages=conversation_history,
            options={"num_predict": 64}
        )
        bot_response = response.get("message", {}).get("content", "⚠️ AI Response Unavailable")
        conversation_history.append({"role": "assistant", "content": bot_response})
        conversation_history = conversation_history[-MAX_HISTORY:]

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    app.run()
