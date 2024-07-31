from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')

def retrieve_documents(query, index, docs, sentence_model):
    query_embedding = sentence_model.encode([query])
    D, I = index.search(np.array(query_embedding), k=5)
    relevant_docs = [docs[i] for i in I[0]]
    return relevant_docs

def generate_response(query, relevant_docs):
    context = " ".join(relevant_docs)
    inputs = tokenizer.encode(query + " " + context, return_tensors='pt')
    outputs = gpt2_model.generate(inputs, max_length=500, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
