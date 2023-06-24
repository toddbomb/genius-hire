from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
from src.database.chatHistory import memory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

def getDocChainAnswer(query, chat_history):

    """
    input_path = 'src/database/Crunch.pkl'
    with open(input_path, "rb") as f:
        vectorstore = pickle.load(f) 
    """

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  
    index_store = os.getcwd()+'/src/database/new_index' 
    vectorstore = FAISS.load_local(index_store,embeddings)
    #test_index.similarity_search_with_relevance_scores("metrics for google Ads performance")

    llm = OpenAI(temperature=0)
    retriever = vectorstore.as_retriever()

    template = """You are an AI assistant answering questions about Crunchbase's marketing.
    You are given the following documents on marketing performance across several channels. 
    If provided, use metrics from the documents in your answer.
    Provide a professional answer to the question.
    Question: {question}
    =========
    {context}
    =========
    Answer:"""

    qa_prompt = PromptTemplate(template=template, input_variables=["question", "context"])

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=False,
        max_tokens_limit=2000, # Should limit this dynamically 
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        #memory=chat_history,
        #get_chat_history=lambda h : h,
    )

    response = qa_chain({'question':query,'chat_history':chat_history})["answer"]

    return response
