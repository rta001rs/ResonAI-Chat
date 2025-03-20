from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set your OpenAI API Key
openai.api_key = os.getenv("openai.api_key = os.getenv("OPENAI_API_KEY") # Replace with actual API key

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

    # Maintain conversation history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history = conversation_history[-MAX_HISTORY:]

    try:
        # Generate AI Response using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can upgrade to GPT-4 if needed
            messages=conversation_history
        )

        bot_response = response['choices'][0]['message']['content']

        # Store response & trim history
        conversation_history.append({"role": "assistant", "content": bot_response})
        conversation_history = conversation_history[-MAX_HISTORY:]

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
