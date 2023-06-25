import os

import pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone


def get_pdf_qa_chain_response(query):


    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chatgpt_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')

    prompt_template = """You are a hiring manager for a company. You will be given a job description and resumes. Using 
    these, you will need to answer questions about all the candidates and their suitability for the given job. You will 
    be objective, clearly stating whether a candidate is qualified or not for the job. Do not say that it is difficult to 
    determine. You are to use objective information from the job description and compare it to the resumes to determine 
    their qualifications. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Job Description: 
    Company: Instalily.ai
    Location: Remote (HQ in New York)
    Role: AI Engineer
    Instalily, a cutting-edge AI startup, is seeking a highly skilled and motivated software engineer to join our rapidly growing team. We are revolutionizing the way organizations operate by empowering them to leverage the power of AI, and we need a talented engineer to help us bring our vision to life.
    As an AI Engineer at Instalily, you will be responsible for developing our AI workflow platform and driving technical excellence throughout the organization. You will work closely with the Lead AI Engineer and cross-functional teams to design and implement new features and capabilities. Additionally, you will be responsible for building a culture of continuous learning and improvement as we continue to build the Instalily team. You will benefit from world-class mentorship from highly-regarded executive leaders at Internet Retailer 100 brands.
    Successful candidates will have the flexibility to work remotely and a continuing education stipend to deepen their technical understanding of the AI landscape.

    Requirements:
    Bachelor’s degree in computer science, engineering, or a related field.
    0 to 2 years of experience as a software engineer (prior software engineering internships and experience a significant plus)
    Excellent problem-solving and analytical skills.
    Passion for understanding AI and machine learning technologies.
    Experience with Python, JavaScript, and other programming languages.
    Understanding of cloud computing technologies and experience with AWS, Azure, or GCP.
    Track record of delivering successful products / working in a collaborative, fast-paced environment is a plus.

    Resumes:
    {context}

    Question: {question}
    Answer: As per the job description, """

    qa_prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    embeddings = OpenAIEmbeddings()

    pinecone.init(
        api_key="035dee03-042d-4a6e-bc1b-a9a4a3546f2b",  # find at app.pinecone.io
        environment="northamerica-northeast1-gcp",  # next to api key in console
    )
    index_name = "langchain1"

    vectorstore = Pinecone.from_existing_index(index_name, embeddings)

    pdf_qa = ConversationalRetrievalChain.from_llm(
        chatgpt_model,
        vectorstore.as_retriever(search_kwargs={"k": 50}),
        memory=memory,
        chain_type="stuff",
        combine_docs_chain_kwargs={'prompt': qa_prompt},
    )

    result = pdf_qa.run(question=query)

    return result


