from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Keep only the latest N messages to prevent lag
MAX_HISTORY = 5
conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "⚠️ Please provide a valid message."})

    # Add user message to conversation history (limit history size)
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history = conversation_history[-MAX_HISTORY:]  # Trim history

    try:
        # Generate AI response with optimized settings
        response = ollama.chat(
            model="mistral",
            messages=conversation_history,
            options={"num_predict": 128}  # Limit response size for speed
        )

        # Extract content safely
        bot_response = response.get("message", {}).get("content", "⚠️ AI Response Unavailable")

        # Add AI response to history and trim again
        conversation_history.append({"role": "assistant", "content": bot_response})
        conversation_history = conversation_history[-MAX_HISTORY:]

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    # Use threaded mode for better performance
    app.run(debug=True, host='0.0.0.0', threaded=True)
