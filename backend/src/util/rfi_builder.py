import os

from langchain.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

def rfi_response(query):
    loader = UnstructuredExcelLoader("/Users/tusharaggarwal/Documents/GitHub/genius-hire/backend/src/files/J. Crew RFP Questions - Feb 2023.xlsx")
    docs = loader.load()

    rfi_data = docs[0].page_content

    text_splitter = RecursiveCharacterTextSplitter()

    texts = text_splitter.create_documents([rfi_data])
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(texts, embeddings)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0), 
        vectorstore.as_retriever(), 
        memory=memory
        )

    answer = qa.run(query)
    return answer


query = "What is your approach to utilizing Artificial Intelligence and machine learning in performance marketing?"

# print(rfi_response(query))