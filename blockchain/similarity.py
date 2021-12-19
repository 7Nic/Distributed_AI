import tensorflow_hub as hub
# https://github.com/tensorflow/tensorflow/issues/38597
# Precisa importar tensorflow_text mesmo sem usar ele diretamente
import tensorflow as tf
import tensorflow_text
from scipy import spatial
from typing import Tuple

model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

class Similarity:
    def __init__(self, first_string: str, second_string: str):
        """
        Classe para armazenar informações sobre a similaridade
        entre textos.

        Args:
            first_string, second_string (str): textos em que se 
            deve aplicar o cálculo de similaridade semântica.
        """
        self._first_string = first_string
        self._second_string = second_string
        self._similarity = compute_similarity(first_string, second_string)
    
    @property
    def similarity(self) -> float:
        return self._similarity
    
    @property
    def texts(self) -> Tuple[str]:
        return (self._first_string, self._second_string)

    def __str__(self) -> str:
        return f"Similaridade({self._first_string}, {self._second_string}) = {self._similarity:.2f}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Similarity):
            return self._first_string == other._first_string and self._second_string == other._second_string
        return False

def compute_similarity(first_string: str, second_string: str) -> float:
    """
    Calcula a similaridade semântica entre dois textos fornecidos.

    Args:
        first_string, second_string (str): textos em que se 
        deve aplicar o cálculo de similaridade semântica.
    
    Returns:
        similarity (float): similaridade entre os dois textos fornecidos.
    """
    text_embeddings = model([first_string, second_string])
    similarity = 1 - spatial.distance.cosine(*text_embeddings)
    return similarity