from django.conf import settings
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VectorStore
from langchain.vectorstores.qdrant import Qdrant

from source_consumer.service.data_updator import DataUpdator


class QdrantDataUpdator(DataUpdator):

    def update_data(self, embedding_model: Embeddings, collection_name: str, chunked_docs: list) -> VectorStore:
        db_config = settings.QDRANT_DB_CONFIG

        return Qdrant.from_documents(chunked_docs, embedding_model,
                                     collection_name=collection_name,
                                     host=db_config["host"],
                                     port=db_config["port"],
                                     api_key=db_config["api_key"])
