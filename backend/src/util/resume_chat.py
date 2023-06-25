import os

from langchain import PromptTemplate, LLMChain
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

os.environ['OPENAI_API_KEY'] = "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"  # replace with your own API Key

# Load PDF, currently done locally but will have to change for final version.
loader = PyMuPDFLoader('backend/src/data/resume_test_pages.pdf')
pages = loader.load()

llm = OpenAI(temperature=0, model_name='text-davinci-003')  # Maybe we can use an open source model for summarization.
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

query = "Have any candidates built React apps?"  # This comes from the user, in my testing I've provided an example.

# Prompt conversion chain. Purpose: to convert user query that asks about all the resumes to a query that asks about
# a single candidate. This is so that I can pass this new query into the retrieval chain for each resume page. 

conversion_prompt_template = """Given the following query, respond a query that is directed to a singular entity 
rather than a group. Examples: Plural question: Did any candidate have a job as a software engineer? Singular 
question: Did this candidate have a job as a software engineer?

Plural question: {original_question}
Singular question: """

conversion_prompt = PromptTemplate(
    input_variables=['original_question'],
    template=conversion_prompt_template
)

conversion_chain = LLMChain(llm=llm, prompt=conversion_prompt)
new_query = conversion_chain.run(query).strip()
print(new_query)

text_splitter = RecursiveCharacterTextSplitter()
embeddings = OpenAIEmbeddings()

# Can be commented out
num_docs = len(pages)
print(f"There are {num_docs} total resumes.\n")

# Running the new query on each resume page. 
for resume_page in pages:
    resume_chunks = text_splitter.create_documents([resume_page.page_content])
    vectorstore = FAISS.from_documents(resume_chunks, embeddings)  # Using FAISS temporarily to test QA, Pinecone later

    # To do: add custom prompt so that response is formatted with candidate name. And sources?
    resume_qa = ConversationalRetrievalChain.from_llm(
        llm,
        vectorstore.as_retriever(),
        memory=memory,
        chain_type="map_reduce"
    )

    num_tokens = llm.get_num_tokens(resume_page.page_content)
    page_num = resume_page.metadata['page'] + 1

    print(f"Resume #{page_num} has {num_tokens} tokens")

    answer = resume_qa.run(question=new_query)
    print(f"Response to '{new_query}' from resume #{page_num}:\n{answer}")

# Findings: by querying the resumes page by page instead of passing the full file into the embedding model, we can get an
# accurate response from each candidate's resume without factual errors. In the current state, the response doesn't
# explicitly specify the candidate's name or give sources/examples, and when encountering a resume that didn't include
# anything about the query, it responds with "I don't know", which is correct, but should be different for our use case.
# I wanted to do this so that we could compile all the formatted answers from this code, and then construct a final 
# response that combines them, that then goes back to the frontend. Also to explore: if a user asks "List 10 candidates 
# that have experience with react apps", this will probably require more parsing of the original prompt to get a stop 
# value and then maybe an additional step in the chain to determine if the response was positive or negative and keep 
# track of the count...



