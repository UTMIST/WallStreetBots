import pandas as pd
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    df = pd.read_csv('dataset.csv')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    sentences = [
        'This framework generates embeddings for each input sentence',
        'Sentences are passed as a list of string.',
        'The quick brown fox jumps over the lazy dog.']
    sentence_embeddings = model.encode(sentences)
    for (sentence, embedding) in zip(sentences, sentence_embeddings):
        print(sentence)
        print(embedding)
        print()

