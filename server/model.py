import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text
from scipy import spatial

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

def calc_similarity(s1, s2):
    # embeddings = embed([
    # "The quick brown fox jumps over the lazy dog.",
    # "I am a sentence for which I would like to get its embedding"])

    embeddings = embed([s1,s2])
    dist = 1-spatial.distance.cosine(embeddings[0], embeddings[1])
    print(dist)
    return dist