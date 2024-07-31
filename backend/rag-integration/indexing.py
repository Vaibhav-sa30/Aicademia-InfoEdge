import faiss
import numpy as np

def create_faiss_index(embeddings):
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

async def create_indexes(engineering_embeddings, ethics_embeddings, policy_embeddings):
    engineering_index = create_faiss_index(np.array(engineering_embeddings))
    ethics_index = create_faiss_index(np.array(ethics_embeddings))
    policy_index = create_faiss_index(np.array(policy_embeddings))

    return engineering_index, ethics_index, policy_index


