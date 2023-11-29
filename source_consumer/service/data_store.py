from abc import ABC, abstractmethod
from typing import List

from langchain.schema import Document


class DataStore(ABC):

    @abstractmethod
    def update_data(self, collection_name: str, chunked_docs: List[Document]):
        pass
