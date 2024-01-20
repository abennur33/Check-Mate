import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def process_text_and_extract_keywords(text_input):
    # Initialize SentenceTransformer
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

# Example text input
text_input = '''This was stated in a recent article in the Chinese state media Global Times (GT). The report came amid Iran and Pakistan trading fire and attacking Baloch separatist groups that hide in each other’s territory and often attack each other’s governments.'''
print(process_text_and_extract_keywords(text_input))
