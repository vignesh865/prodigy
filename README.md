## Prodigy

Prodigy employs OpenAI for production and quantized Mistral for local development, integrating connected pipelines with Google Drive and Kafka for data ingestion. Leveraging retrieval augmented generation techniques using Large Language Models (LLMs), Prodigy enhances knowledge management with advanced AI capabilities.

**Demo**

In this demo, we are querying 270 pages of unstructured documents loaded directly from Google Drive and ingested into the QdrantDB(Using data pipeline). Then, the context for the queries will be retrieved using a Hybrid search Method(BM25 embeddings for text search and hugging face embeddings for semantic search). After that, the retrieved context will be fed to the LLM and the answers generated will be streamed to the frontend. 

The answers for the given query and relevant context from the pdf are shown side by side in the below video(Clicking will redirect to demo video hosted in Youtube). 

**_V1 Video With Single Document System:_**

[![IMAGE ALT TEXT HERE](https://github.com/vignesh865/prodigy/assets/13492027/85a0d686-86b4-4651-a515-09c7be5b9c67)](https://youtu.be/lSe6nAqhQ1A)

**_V3 Video with Authentication and Multi-Document System:_**

[![Rag Demo V3 Thumbnail](https://github.com/vignesh865/prodigy/assets/13492027/671b2c98-6f93-4cd2-8a53-add25fd5fc90)](https://youtu.be/iYAhVAsJwRs)
