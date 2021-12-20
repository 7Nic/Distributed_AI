import tensorflow_hub as hub
# https://github.com/tensorflow/tensorflow/issues/38597
# Precisa importar tensorflow_text mesmo sem usar ele diretamente
import tensorflow as tf
import tensorflow_text
from scipy import spatial
from typing import Iterable, Tuple

from document import Document

model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

class Similarity:
    def __init__(self, first_document: Document, second_document: Document):
        """
        Classe para armazenar informações sobre a similaridade
        entre documentos.

        Args:
            first_document, second_document (Documento): instâncias
            de documentos em que se deve aplicar o cálculo de similaridade 
            semântica no corpo do texto.
        """
        self._first_document = first_document
        self._second_document = second_document
        self._similarity = compute_similarity(first_document.body, second_document.body)
    
    @property
    def similarity(self) -> float:
        return self._similarity
    
    @property
    def documents(self) -> Tuple[Document]:
        return (self._first_document, self._second_document)

    def __str__(self) -> str:
        return f"Similaridade({self._first_document.title}, {self._second_document.title}) = {self._similarity:.2f}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Similarity):
            return self._first_document == other._first_document and self._second_document == other._second_document
        return False

    def same_document(self, other: Iterable[Document]) -> bool:
        """
        Dado um iterável de documentos, verifica se este iterável possui documentos equivalentes
        ao da instância da classe Similarity.

        Args:
            other (Iterable[Document]): iterável contendo documentos.
        
        Returns:
            (bool): True se o iterável possuir o mesmo conjunto de textos que a instância
            da classe Similaridade, False do contrário.
        """
        if len(self.documents) != len(other):
            return False
                
        return set([document.title for document in self.documents]) == set([document.title for document in other]) \
            and set([document.body for document in self.documents]) == set([document.body for document in other])

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