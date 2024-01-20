from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

from fact_checking import FactChecker

import sys

app = Flask(__name__)

def get_confidence(context, claim):
    print("fact checking!")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    fact_checker = FactChecker(fact_checking_model, tokenizer)
    is_claim_true = fact_checker.validate_with_replicas(context, claim)
    return is_claim_true['Y'] * 100

def gschol_search(query):
    newq = query.replace(" ", "+")
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C15&q=" + newq + "&btnG="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 elements with class "gs_rt"
    h3_elements = soup.find_all('h3', class_='gs_rt')

    # Extract href attributes within <a> elements under each h3
    href_values = []
    for h3_element in h3_elements:
        a_element = h3_element.find('a')
        if a_element:
            href_value = a_element.get('href')
            href_values.append(href_value)

    maxp = 0
    maxurl = ""

    for href in href_values:
        url = href
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        p_text = lambda soup: ''.join([p.get_text() for p in soup.find_all('p')])
        
        conf = get_confidence(p_text, query)
        if conf > maxp:
            maxp = conf
            maxurl = url
    
    return {"url": maxurl, "confidence": maxp}
    

def snopes_search(query):
    newq = query.replace(" ", "%20")
    url = "https://www.snopes.com/search/" + newq + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with class "article_wrapper"
    div_elements = soup.find_all('div', class_='article_wrapper')

    # Extract href attributes within <a> elements under each div
    href_values = []
    for div in div_elements:
        input_element = div.find('input')
        if input_element:
            href_value = input_element.get('value')
            href_values.append(href_value)

    
    maxp = 0
    maxurl = ""

    for href in href_values:
        url = href
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        p_elements = soup.find_all('p')
        for p in p_elements:
            p_text = p.get_text()
            conf = get_confidence(p_text, query)
            if conf > maxp:
                maxp = conf
                maxurl = url
    
    return {"url": maxurl, "confidence": maxp}

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        source = data.get('source', '')
        query = data.get('query', '')

        if source == 'gschol':
            result = gschol_search(query)
        elif source == 'snopes':
            result = snopes_search(query)
        else:
            return jsonify({'error': 'Invalid source. Please provide either "gschol" or "snopes".'}), 400

        return jsonify({'percent': result.confidence, 'url': result.url})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
