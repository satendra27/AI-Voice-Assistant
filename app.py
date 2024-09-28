import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher

app = Flask(__name__)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBg6-xTEEppzlgJEE17IjkTpR6TbV2zsrw"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

conversation_history = []
def voice_assistant(user_input):
    prompt = f"""
        You are an AI assistant in an engaging conversation with a user. The user just asked the following question:
        '{user_input}'
        Provide a direct and informative answer, focusing on the exact details the user is asking for. Avoid unnecessary elaboration or asking follow-up questions unless essential to the user’s inquiry. Keep the response clear, concise, and to the point. If the topic is complex, briefly summarize the key aspects.
        """
    response = model.generate_content(prompt).text


 # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response


# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle voice input and return model response with conversation history
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistant(user_input)

    # Return the updated conversation history
    return jsonify({'response': response, 'conversation_history': conversation_history})


if __name__ == '__main__':
    app.run(debug=True)