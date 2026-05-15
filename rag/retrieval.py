from rag.embeddings import generar_embedding


def buscar_chunks_similares(
    pregunta,
    collection,
    top_k=5
):

    embedding = generar_embedding(pregunta)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": 100,
                "limit": top_k
            }
        }
    ]

    resultados = list(
        collection.aggregate(pipeline)
    )

    return resultados