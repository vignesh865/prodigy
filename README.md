## Prodigy

Prodigy employs OpenAI for production and quantized Mistral for local development, integrating connected pipelines with Google Drive and Kafka for data ingestion. Leveraging retrieval augmented generation techniques using Large Language Models (LLMs), Prodigy enhances knowledge management with advanced AI capabilities.

**Demo**

In this demo, we are querying 270 pages of unstructured documents loaded directly from Google Drive and ingested into the QdrantDB(Using data pipeline). Then, the context for the queries will be retrieved using a Hybrid search Method(BM25 embeddings for text search and hugging face embeddings for semantic search). After that, the retrieved context will be fed to the LLM and the answers generated will be streamed to the frontend. 

The answers for the given query and relevant context from the pdf are shown side by side in the below video. 

[![IMAGE ALT TEXT HERE](https://i.ytimg.com/vi/lSe6nAqhQ1A/maxresdefault.jpg)](https://youtu.be/lSe6nAqhQ1A)
