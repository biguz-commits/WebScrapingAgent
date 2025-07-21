from typing import List, Type

from pydantic import BaseModel
from requests import Session
from sentence_transformers import SentenceTransformer
import numpy as np

from app.db.models.UnicattLatestNews import UnicattLatestNews



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

    def vectorialize(self, data: str):
        model = self.get_embedding_model()
        embeddings = np.array(model.encode(data), dtype=np.float32)
        return self.vector_resize(embeddings)

    def lookup(
            self, db: Session, query: str,
            top_k: int = 5,
            model: BaseModel = UnicattLatestNews
    ) -> List[Type[BaseModel]]:
        query = self.vectorialize(query)
        q = db.query(model)
        return (q.order_by(model.embedding.l2_distance(query))
                .limit(top_k)
                .all())



