import json
import gensim.downloader as api
from gensim.models import Word2Vec, KeyedVectors

import os
import operator


def load_descriptors_from_json(json_path):
    try:

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, json_path)
        with open(file_path) as f:
            descriptors = json.load(f)
        if not isinstance(descriptors, list):
            raise ValueError("JSON input should be a list.")
        return descriptors
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Error processing JSON: {e}")

def get_similar_words(descriptors_path, words):
    descriptors = load_descriptors_from_json(descriptors_path)
    
    # Convert descriptors to a set for faster lookups
    descriptor_set = set(descriptors)
    
    word_vectors = load_word_vectors()

    # Get the most similar words
    result = word_vectors.most_similar(
        positive=words,  # Example input; adjust as needed
        topn=len(word_vectors.key_to_index)
    )
    # Filter results based on the descriptors
    matches = [res for res in result if res[0] in descriptor_set]
    
    return list(map(operator.itemgetter(0), matches[:10])) # change later to better fit the model

def load_word_vectors():
    # Load the model from disk
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, os.getenv("MODEL_PATH"))
    return KeyedVectors.load(file_path)