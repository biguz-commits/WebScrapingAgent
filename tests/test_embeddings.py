from sentence_transformers import SentenceTransformer
import numpy as np

from app.agent.Embeddings import Embeddings


def main():
    model_path = "ibm-granite/granite-embedding-278m-multilingual"
    model = SentenceTransformer(model_path)
    input_queries = [
        ' Who made the song My achy breaky heart? ',
        'summit define'
    ]
    input_passages = [
        "Achy Breaky Heart is a country song written by Don Von Tress. Originally titled Don't Tell My Heart and performed by The Marcy Brothers in 1991. ",
        "Definition of summit for English Language Learners. : 1 the highest point of a mountain : the top of a mountain. : 2 the highest level. : 3 a meeting or series of meetings between the leaders of two or more governments."
    ]
    em = Embeddings()
    query_embeddings = model.encode(input_queries)
    passage_embeddings = model.encode(input_passages)
    print(f"before flattened: {np.array(query_embeddings)}")
    print(f"size: {query_embeddings.shape}")
    print(f"after flattened: {em.vector_resize(query_embeddings)}")
    print(f"size: {em.vector_resize(query_embeddings).shape}")



if __name__ == '__main__':
    main()
