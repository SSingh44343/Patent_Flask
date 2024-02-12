# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, World, from Flask!"

#may need to put Werkzeug in requirements.txt

from flask import Flask, request, render_template, jsonify
import requests
import os
from bs4 import BeautifulSoup
import re
import openai
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables and set OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>') 
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['searchTerm']
    res = requests.get(f"https://patents.google.com/xhr/query?url=q%3D{search_term}&exp=")
    main_data = res.json()
    data = main_data['results']['cluster']

    patents = []
    if data:
        for i, item in enumerate(data[0]['result']):
            num = item['patent']['publication_number']
            title = cleanhtml(item['patent']['title'])
            patent_url = "https://patents.google.com/patent/" + num
            patents.append({
                'index': i + 1,
                'title': title,
                'number': num,
                'url': patent_url
            })

    return render_template('results.html', patents=patents)

# Add more routes as needed for other functionalities

if __name__ == '__main__':
    app.run(debug=True)
