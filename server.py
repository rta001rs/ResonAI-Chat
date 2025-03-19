from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    response = ollama.chat(model='mistral', messages=[{"role": "user", "content": user_message}])
    bot_response = response["message"] if "message" in response else "I couldn't process that."
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
