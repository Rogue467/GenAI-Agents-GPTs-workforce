# chatbot.py

import os
from flask import Flask, request, jsonify, render_template
import openai



app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = 'sk-wlV9xkHlk6PUHTwewZjGdNy2lYf-6hXqQWXVf_G8cFT3BlbkFJAwmIxaGoBYtwx6pqZLWV5eMCC3bS4XG407lyq2jB8A'

def get_openai_response(user_input):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # You can choose other models like "gpt-3.5-turbo"
            prompt=user_input,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'response': 'Please provide a valid input.'})
    
    bot_response = get_openai_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
