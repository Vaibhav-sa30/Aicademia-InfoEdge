# data_processing.py
import pymongo
import re
from sentence_transformers import SentenceTransformer
import logging

MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "researchPapers"
client = pymongo.MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]


def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_papers_from_collection(collection_name):
    papers = db[collection_name].find()
    documents = []
    for paper in papers:
        content = paper.get('content', '')
        if content:
            cleaned_content = clean_text(content)
            documents.append(cleaned_content)
        else:
            logging.warning(f'Found paper with no content: {paper.get("_id")}')
    return documents

def generate_embeddings():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    engineering_docs = get_papers_from_collection('engineering_papers')
    ethics_docs = get_papers_from_collection('ethics_papers')
    policy_docs = get_papers_from_collection('policy_papers')

    engineering_embeddings = model.encode(engineering_docs)
    ethics_embeddings = model.encode(ethics_docs)
    policy_embeddings = model.encode(policy_docs)

    return engineering_docs, ethics_docs, policy_docs, engineering_embeddings, ethics_embeddings, policy_embeddings






