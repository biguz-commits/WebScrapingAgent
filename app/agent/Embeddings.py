from sentence_transformers import SentenceTransformer
import numpy as np


class Embeddings:
    def __init__(self,
                 model_path: str = "ibm-granite/granite-embedding-278m-multilingual",
                 ):
        self.model_path = model_path

    def get_embedding_model(self):
        return SentenceTransformer(self.model_path)

    @staticmethod
    def vector_resize(array: np.array) -> np.array:
        return array.flatten()

