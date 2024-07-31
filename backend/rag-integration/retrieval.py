import numpy as np


def retrieve_documents(query, index, docs, model, k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    return [docs[i] for i in I[0]]
