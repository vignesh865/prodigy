from abc import ABC, abstractmethod

from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VectorStore


class DataUpdator(ABC):

    @abstractmethod
    def update_data(self, embedding_model: Embeddings, collection_name: str, chunked_docs: list) -> VectorStore:
        pass
