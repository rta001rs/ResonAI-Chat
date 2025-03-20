from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable Cross-Origin for browser requests
import ollama

app = Flask(__name__)
CORS(app)  # Allow all origins (modify for security later)

# Memory for session context (temporary storage)
conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.get_json()
    user_message = data.get("message", "")

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Generate AI response
    response = ollama.chat(model='mistral', messages=conversation_history)

# Ensure we extract only the content as a string
if isinstance(response, dict) and 'message' in response and 'content' in response['message']:
    bot_response = response['message']['content']
else:
    bot_response = "⚠️ AI Response Unavailable"

return jsonify({"response": bot_response})
    bot_response = response.get("message", "I couldn't process that.")

    # Add AI response to history
    conversation_history.append({"role": "assistant", "content": bot_response})

    return jsonify({"response": bot_response.get('content', '⚠️ AI Response Unavailable')})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
