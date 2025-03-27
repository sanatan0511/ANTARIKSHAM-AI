from flask import Flask, render_template, request, jsonify
import requests
import random
from datetime import datetime

app = Flask(__name__)

API_KEY = 'Ggkf0FPevYAaEPF5bWCerSDtXs8fhkMJiGVxC0qd'

# User state
history = []

@app.route('/')
def index():
    apod = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}').json()
    return render_template('index.html', apod=apod)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    # Directly pass user question to NASA's Natural Language API (simulated)
    # Since NASA does not have a real Q&A API, we'll fallback to APOD search example
    # You will replace this with any future real NASA Q&A API if available

    # For this example, treat question as a keyword for APOD search
    search_url = f'https://images-api.nasa.gov/search?q={question}'
    response = requests.get(search_url)

    if response.status_code == 200:
        results = response.json().get('collection', {}).get('items', [])
        if results:
            item = results[0]
            title = item.get('data', [{}])[0].get('title', 'No title')
            description = item.get('data', [{}])[0].get('description', 'No description')
            image_url = item.get('links', [{}])[0].get('href', '')
            answer = f"Title: {title}\nDescription: {description}\nImage: {image_url}"
        else:
            answer = "No relevant data found from NASA API."
    else:
        answer = "NASA API error or invalid question."

    history.append({'question': question, 'answer': answer})
    return jsonify({'answer': answer, 'history': history})

if __name__ == "__main__":
    app.run(debug=True)