from bs4 import BeautifulSoup
import requests
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

import sys
import re
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag    
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fact_checking import FactChecker


def contains_no_words(main_string, words_to_check):
    # Split the main string into words
    main_words = set(main_string.split())

    # Check if any word from words_to_check is in main_words
    for word in words_to_check.split():
        if word in main_words:
            return False

    # If no matching words are found
    return True

def condense_strings(input_strings):
    combined_strings = []
    current_chunk = ""
    max_words = 750
    
    for string in input_strings:
        # Tokenize the current string into words
        words = word_tokenize(string)
        
        # Check if adding the words exceeds the maximum limit
        if len(words) + len(word_tokenize(current_chunk)) <= max_words:
            # Combine the words into the current chunk
            current_chunk += " ".join(words) + " "
        else:
            # Start a new chunk if adding the words would exceed the limit
            combined_strings.append(current_chunk.strip())
            current_chunk = " ".join(words) + " "
    
    # Add the last chunk to the result
    if current_chunk:
        combined_strings.append(current_chunk.strip())
    
    return combined_strings


def process_text_and_extract_keywords(text_input):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    def preprocess_text(text):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        return text.lower()

    def extract_keywords(text, max_keywords=5):
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        keywords = [word for word in tokens if word not in stop_words and len(word) > 3]
        tagged = pos_tag(keywords)
        keywords = [word for word, tag in tagged if tag.startswith('NN')]
        return keywords[:max_keywords]

    def cluster_sentences(sentences):
        processed_texts = [preprocess_text(sentence) for sentence in sentences]
        embeddings = model.encode(processed_texts)
        cosine_sim = cosine_similarity(embeddings)
        num_clusters = min(5, len(sentences))
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(cosine_sim)
        return kmeans.labels_

    sentences = sent_tokenize(text_input)
    all_keywords = []

    if len(sentences) == 1:
        all_keywords.extend(extract_keywords(sentences[0]))
    else:
        clusters = cluster_sentences(sentences)
        for cluster in range(max(clusters) + 1):
            cluster_keywords = []
            for i, sentence in enumerate(sentences):
                if clusters[i] == cluster:
                    cluster_keywords.extend(extract_keywords(sentence))
            unique_keywords = list(set(cluster_keywords))
            all_keywords.extend(unique_keywords)

    return ' '.join(all_keywords)

def get_confidence(context, claim):
    # print(f"fact checking!")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    # print('tokenized')
    fact_checking_model = GPT2LMHeadModel.from_pretrained('fractalego/fact-checking')
    # print('fact_checking_model')
    fact_checker = FactChecker(fact_checking_model, tokenizer)
    # print('fact_checker')
    is_claim_true = fact_checker.validate_with_replicas(context, claim)
    # print('with replicas')
    return is_claim_true.get('Y', 0.0) * 100

def gschol_search(query):
    newq = query.replace(" ", "+")
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C15&q=" + newq + "&btnG="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    h3_elements = soup.find_all('h3', class_='gs_rt')

    href_values = []
    for h3_element in h3_elements:
        a_element = h3_element.find('a')
        if a_element:
            href_value = a_element.get('href')
            href_values.append(href_value)

    maxp = 0
    maxurl = ""
    minp = 100
    minurl = ""
    i = 0

    for href in href_values:
        if i > 1:
            break
        i += 1
        url = href
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        p_objects = soup.find_all('p')

        # # Use map to apply .get_text(strip=True) to each p object
        # p_texts = list(map(lambda p: p.get_text(strip=True), p_objects))
        # p_texts = condense_strings(p_texts)
        


        maxc = 0
        cnt = 1
        size = len(p_objects)
        for p in p_objects:
            print(f"{cnt}/{size}")
            cnt += 1
            if contains_no_words(p.get_text(strip=True), query):
                print("skipped")
                continue
            conf = get_confidence(p.get_text(strip=True), query)
            if conf > maxc:
                maxc = conf
        # p_text = get_p_text(soup)

        # if p_text == "":
        #     continue
        
        if maxc > maxp:
            maxp = maxc
            maxurl = url
        if maxc < minp:
            minp = maxc
            minurl = url

    if maxp < 50:
        return {"url": minurl, "confidence": minp}
    
    return {"url": maxurl, "confidence": maxp}
    

def snopes_search(query):
    newq = query.replace(" ", "%20")
    url = "https://www.snopes.com/search/" + newq + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_elements = soup.find_all('div', class_='article_wrapper')

    href_values = []
    for div in div_elements:
        input_element = div.find('input')
        if input_element:
            href_value = input_element.get('value')
            href_values.append(href_value)

    
    maxp = -1
    maxurl = ""
    minp = 100
    minurl = ""

    i = 0

    for href in href_values:
        if i > 1:
            break
        i += 1
        url = href
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        p_objects = soup.find_all('p')

        # # Use map to apply .get_text(strip=True) to each p object
        # p_texts = list(map(lambda p: p.get_text(strip=True), p_objects))
        # p_texts = condense_strings(p_texts)

        maxc = 0
        cnt = 1
        size = len(p_objects)
        for p in p_objects:
            print(f"{cnt}/{size}")
            cnt += 1
            if contains_no_words(p.get_text(strip=True), query):
                print("skipped")
                continue
            conf = get_confidence(p.get_text(strip=True), query)
            if conf > maxc:
                maxc = conf
        # p_text = get_p_text(soup)

        # if p_text == "":
        #     continue
        
        if maxc > maxp:
            maxp = maxc
            maxurl = url
        if maxc < minp:
            minp = maxc
            minurl = url

    if maxp == -1:
        return {"url": "No urls found", "confidence": -1}
    elif maxp < 50:
        return {"url": minurl, "confidence": minp}
    
    return {"url": maxurl, "confidence": maxp}

def full_test(query, source):
    query = process_text_and_extract_keywords(query)

    if source == "snopes":
        print(snopes_search(query))
    elif source == "gschol":
        print(gschol_search(query))
    else:
        return {"url": "https://www.google.com/search?q=" + query, "confidence": 0}
    

full_test("Global temperatures are rising", "snopes")