import os

import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA



def get_pdf_qa_chain_response(query, job_description, filename):

    chatgpt_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')


    prompt_template = f"""Use the following pieces of context to answer the question at the end. If you don't know the 
    answer, just say that you don't know, don't try to make up an answer.

    Job Description:
    {job_description}

    ```{{context}}```

    Question: {{question}}
    Helpful Answer: """


    qa_prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    embeddings = OpenAIEmbeddings()

    pinecone.init(
        api_key="035dee03-042d-4a6e-bc1b-a9a4a3546f2b",  # find at app.pinecone.io
        environment="northamerica-northeast1-gcp",  # next to api key in console
    )
    index_name = "langchain1"

    vectorstore = Pinecone.from_existing_index(index_name, embeddings, namespace=filename)

    chain_type_kwargs = {"prompt": qa_prompt}

    pdf_qa = RetrievalQA.from_chain_type(
        llm=chatgpt_model,
        chain_type="map_reduce",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs=chain_type_kwargs
    )

    result = pdf_qa.run(question=query)

    return result


