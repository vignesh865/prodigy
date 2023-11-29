from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema.embeddings import Embeddings

from source_consumer.service.qdrant_data_store import QdrantDataStore


class VectorOrchestrator:

    def get_embeddings(self) -> (Embeddings, int):
        return SentenceTransformerEmbeddings(), 768

    def get_vector_store(self, embedding_model: Embeddings, vector_size: int):
        return QdrantDataStore(embedding_model, vector_size)
