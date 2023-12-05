
from django.views import View
from django.http import HttpResponse
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from datetime import datetime
from dotenv import load_dotenv


class ChatView(View):
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        super().__init__()
        self.collection_name = 'sap_security'
        self.embeddings = SentenceTransformerEmbeddings()
        self.llm = ChatOpenAI()
        self.vectorstore = self.get_vectorstore()
        self.conversation = self.get_conversation_chain()

    def get_vectorstore(self):
        client = QdrantClient(url="https://87b489ea-0d6d-47f4-bd4f-f14d5a3a28fa.us-east4-0.gcp.cloud.qdrant.io:6333",
                              api_key="c_jnem-7h7hP4RNQACx0IhU_yCXaKGejhGHsuhk1Vp0bhfBNF2wsfw", prefer_grpc=False)
        vec_store = Qdrant(client, collection_name=self.collection_name, embeddings=self.embeddings)
        return vec_store

    def get_conversation_chain(self):
        memory = ConversationBufferWindowMemory(memory_key='chat_history', k=4, return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=memory,
        )
        print(datetime.now(), ' : memory created')
        return conversation_chain

    def get(self, request, *args, **kwargs):
        # Get the question parameter from the request, defaulting to "What is SAP?" if not provided
        question = request.GET.get('question', 'What is SAP?')
        response = self.conversation({'question': question})
        output = ""
        for i, msg in enumerate(response):
            if i % 2 == 0:
                output += f"user: {msg}\n"
            else:
                output += f"AI : {msg}\n"
        return HttpResponse(output)
