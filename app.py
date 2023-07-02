from flask import Flask, render_template, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['search_term']
    results = get_search_results(term)
    save_results_to_txt(results)
    return jsonify(results)

def get_search_results(term):
    search_results = {}

    search_engines = {
        'Google': f"https://www.google.com/search?q={term}",
        'Bing': f"https://www.bing.com/search?q={term}",
        'Yahoo': f"https://br.search.yahoo.com/search?p={term}",
        'DuckDuckGo': f"https://duckduckgo.com/?q={term}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    links_list = []
    for engine, url in search_engines.items():
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links_count = 0
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href is not None and href.startswith("http"):
                    links_list.append(href)
                    links_count += 1
                    if links_count == 5:
                        break
            webbrowser.open_new_tab(url)
        except:
            search_results[engine] = []

    search_results['Search Results'] = links_list

    return search_results

def save_results_to_txt(results):
    with open('search_results.txt', 'w') as file:
        for engine, links in results.items():
            file.write(f"{engine}:\n")
            for link in links:
                file.write(f"{link}\n")
            file.write("\n")

@app.route('/download')
def download():
    file_path = 'search_results.txt'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
