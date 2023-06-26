import os

import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

os.environ['OPENAI_API_KEY'] = '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'


def get_pdf_qa_chain_response(query, job_description, filename):

    chatgpt_model = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')

    embeddings = OpenAIEmbeddings()

    pinecone.init(
        api_key="035dee03-042d-4a6e-bc1b-a9a4a3546f2b",  # find at app.pinecone.io
        environment="northamerica-northeast1-gcp",  # next to api key in console
    )
    index_name = "langchain1"

    vectorstore = Pinecone.from_existing_index(index_name, embeddings, namespace=filename)


    prompt_template = f"""You are an experienced hiring manager for a company. You will be given a job description and the resumes of candidates 
    to answer the user's question. Answer questions objectively, using the content from the job description to back up your answers.
      If the topic requested isn't in a candidate's resume, you can assume the candidate has no experience with the topic. 
      If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Job Description:
    {job_description}

    Resumes:
    ```{{context}}```

    Question: {{question}}
    Helpful Answer: """


    qa_prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain_type_kwargs = {"prompt": qa_prompt}

    pdf_qa = ConversationalRetrievalChain.from_llm(
        llm=chatgpt_model,
        retriever=vectorstore.as_retriever(search_kwargs={'k': 50}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )

    result = pdf_qa.run(query)

    return result

job_description = """Company: Instalily.ai
Location: Remote (HQ in New York)
Role: AI Engineer
Instalily, a cutting-edge AI startup, is seeking a highly skilled and motivated software engineer to join our rapidly growing team. We are revolutionizing the way organizations operate by empowering them to leverage the power of AI, and we need a talented engineer to help us bring our vision to life.
As an AI Engineer at Instalily, you will be responsible for developing our AI workflow platform and driving technical excellence throughout the organization. You will work closely with the Lead AI Engineer and cross-functional teams to design and implement new features and capabilities. Additionally, you will be responsible for building a culture of continuous learning and improvement as we continue to build the Instalily team. You will benefit from world-class mentorship from highly-regarded executive leaders at Internet Retailer 100 brands.
Successful candidates will have the flexibility to work remotely and a continuing education stipend to deepen their technical understanding of the AI landscape.

Responsibilities:
Develop Instalily’s AI workflow platform and drive technical excellence throughout the organization.
Work closely with cross-functional teams (product, UI/UX, business development) to design and implement new features and capabilities.
Rapidly learn into the expected quality and reliability of the platform through comprehensive testing and continuous integration/continuous delivery (CI/CD) practices.
Build a rapport with the Lead AI Engineer and Head of Product while fostering a culture of continuous learning and improvement.
Collaborate with the product and design teams to deliver high-quality products that meet customer needs.
Stay up-to-date with the latest AI and software engineering trends and technologies.

Requirements:
Bachelor’s degree in computer science, engineering, or a related field.
0 to 2 years of experience as a software engineer (prior software engineering internships and experience a significant plus)
Excellent problem-solving and analytical skills.
Passion for understanding AI and machine learning technologies.
Experience with Python, JavaScript, and other programming languages.
Understanding of cloud computing technologies and experience with AWS, Azure, or GCP.
Track record of delivering successful products / working in a collaborative, fast-paced environment is a plus.

Join the AI revolution with Instalily! As an AI Engineer, you will have the opportunity to make a significant impact on the future of AI and work with a talented and passionate team of experts. If you’re ready to take your software engineering skills to the next level, we want to hear from you!
"""

filename = "exresumes.pdf"

query = "Rank order the top 5 candidates that are best fit for this job and assign a numerical grade out of 100 to each. "

print(get_pdf_qa_chain_response(query, job_description, filename))