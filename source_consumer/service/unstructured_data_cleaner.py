from unstructured.cleaners.core import clean, group_broken_paragraphs

from source_consumer.models.ingest_message import IngestMessage
from source_consumer.service.data_cleaner import DataCleaner


class UnstructuredDataCleaner(DataCleaner):

    def clean_document_pre_chunking(self, ingest_message: IngestMessage, elements):
        for element in elements:
            element.text = clean(element.text, extra_whitespace=True, dashes=True)
            element.text = group_broken_paragraphs(element.text)
        return elements

    def clean_document_post_chunking(self, ingest_message: IngestMessage, chunked_elements):
        for chunked_element in chunked_elements:
            chunked_element.text = clean(chunked_element.text, extra_whitespace=True, dashes=True)
            chunked_element.text = group_broken_paragraphs(chunked_element.text)
        return chunked_elements
