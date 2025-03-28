from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'Ggkf0FPevYAaEPF5bWCerSDtXs8fhkMJiGVxC0qd'

# User state
history = []

def fetch_wikipedia_summary(question):
    """Fetches Wikipedia summary with improved search capability"""
    search_query = question.replace('What is ', '').replace('?', '').strip()

    # Step 1: Get a list of relevant Wikipedia pages
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_query}&format=json"
    search_response = requests.get(search_url).json()
    
    if 'query' in search_response and 'search' in search_response['query']:
        search_results = search_response['query']['search']
        if search_results:
            best_match_title = search_results[0]['title']  # Take the first matching title
            
            # Step 2: Fetch the summary of the best match
            wiki_api_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_match_title.replace(' ', '_')}"
            summary_response = requests.get(wiki_api_url).json()
            
            return f"**{summary_response.get('title', '')}**\n{summary_response.get('extract', 'No information available.')}"
    
    return "I couldn't find an answer. Try rephrasing your question."

@app.route('/')
def index():
    apod = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}').json()
    return render_template('index.html', apod=apod)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    # Step 1: Check if the question is a general space-related query
    if "what is" in question.lower() or "tell me about" in question.lower():
        answer = fetch_wikipedia_summary(question)
    else:
        # Step 2: Search NASA API if it's not a Wikipedia-type question
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
