from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Optimize memory usage
MAX_HISTORY = 5
conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Please provide a valid message."})

    # Maintain only the last 5 messages to prevent slow processing
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history = conversation_history[-MAX_HISTORY:]

    try:
        # AI Response Optimization
        response = ollama.chat(
            model="mistral",
            messages=conversation_history,
            options={"num_predict": 64, "keep_alive": True}  # Reduce response size for faster processing
        )

        # Extract response safely
        bot_response = response.get("message", {}).get("content", "⚠️ AI Response Unavailable")

        # Store response & trim history
        conversation_history.append({"role": "assistant", "content": bot_response})
        conversation_history = conversation_history[-MAX_HISTORY:]

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', threaded=True)
