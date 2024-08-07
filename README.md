## Prodigy

Prodigy employs OpenAI for production and quantized Mistral for local development, integrating connected pipelines with Google Drive and Kafka for data ingestion. Leveraging retrieval augmented generation techniques using Large Language Models (LLMs), Prodigy enhances knowledge management with advanced AI capabilities.

**Demo**

In this demo, we are querying 270 pages of unstructured documents loaded directly from Google Drive and ingested into the QdrantDB(Using data pipeline). Then, the context for the queries will be retrieved using a Hybrid search Method(BM25 embeddings for text search and hugging face embeddings for semantic search). After that, the retrieved context will be fed to the LLM and the answers generated will be streamed to the frontend. 

The answers for the given query and relevant context from the pdf are shown side by side in the below video(Clicking will redirect to demo video hosted in Youtube). 

**_V1 Video With Single Document System:_**

[![IMAGE ALT TEXT HERE](https://github.com/vignesh865/prodigy/assets/13492027/85a0d686-86b4-4651-a515-09c7be5b9c67)](https://youtu.be/lSe6nAqhQ1A)

**_V3 Video with Authentication and Multi-Document System:_**

[![Rag Demo V3 Thumbnail](https://github.com/vignesh865/prodigy/assets/13492027/671b2c98-6f93-4cd2-8a53-add25fd5fc90)](https://youtu.be/iYAhVAsJwRs)

---

# Setup Instructions

This is a fullstack application. The steps below will guide you through the initial setup and running the application. Kafka and Redis are part of the application stack but are not necessary for the initial setup. You can comment out `source_consumer/apps.py` and follow the instructions below. Once the initial setup is complete, you can proceed to set up Kafka and Redis.

These instructions are optimized for PyCharm.

## Prerequisites

1. **PyCharm**: Ensure you have PyCharm installed.
2. **Python**: Make sure Python is installed on your machine.
3. **Google Cloud Account**: Required for Google account integration.
4. **Qdrant Account**: Required for Qdrant client integration.

## Initial Setup

1. **Import the Project**: 
   - Open PyCharm and import the project.
   - Create a new Python interpreter. PyCharm will automatically create a `venv` folder.

2. **Restart PyCharm**:
   - Restart the IDE.
   - The terminal should be prefixed with `(venv)`. For example:
     ```
     (venv) vignesh@Vigneshs-MacBook-Pro prodigy %
     ```

3. **Install Requirements**:
   - Open the terminal and run:
     ```bash
     pip install -r requirements.txt
     ```

4. **Database Migrations**:
   - Run the following commands to set up the database:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Seed Initial Data**:
   - Open the Django shell:
     ```bash
     python manage.py shell
     ```
   - In the shell, run the commands from `init_run.shell` one by one.
   - Exit the shell:
     ```python
     exit()
     ```

6. **Start Backend Server**:
   - Run the backend server:
     ```bash
     python manage.py runserver 8080
     ```

7. **Start Frontend Server**:
   - Run the frontend server:
     ```bash
     streamlit run frontend/About.py
     ```
   - It is preferred to run this in a PyCharm configuration because it sets the Python path automatically.
   - <img width="1042" alt="Screenshot 2024-08-06 at 9 55 25 PM" src="https://github.com/user-attachments/assets/9535d78f-3cde-4bab-976c-b87b0dd7f133">

Without the below setup, now you should be able to start, login and logout from the app.

## Additional Setup

1. **Google Account Integration**:
   - Create a Google Cloud project. Create a oauth2 secret in google console and update it in the resources/secrets folder. The file name would be client_secret.json
   - Detailed documentation for this setup will be updated soon.

2. **Qdrant Client Integration**:
   - Create a free Qdrant server.
   - Detailed documentation for this setup will be updated soon.

---

This README provides the necessary steps to get your Prodigy app running. If you have any questions or run into issues, feel free to ask for help.
