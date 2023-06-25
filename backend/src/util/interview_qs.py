import os

from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyMuPDFLoader
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter



os.environ['OPENAI_API_KEY'] = "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"  # replace with your own API Key

# Load PDF, currently done locally but will have to change for final version.
loader = PyMuPDFLoader('backend/src/data/resume_test_pages.pdf')
pages = loader.load()

llm = OpenAI(temperature=0, model_name='text-davinci-003')  # Maybe we can use an open source model for summarization.
# Should we have a separate LLM for the question generation? Maybe one with higher temperature...

# Potentially create custom summarization prompt here?
summary_prompt_template = """
"""

# Initializing summarization chain and text splitter
text_splitter = RecursiveCharacterTextSplitter()
# If done, summary prompt is passed in as a param here - prompt=summary_prompt
summarization_chain = load_summarize_chain(llm, chain_type='map_reduce')
# What chain type is best for this?

interview_prompt_template = '''I want you to act as a skilled hiring manager. You come up with interview questions to ask 
candidates who are applying for a job at your company. Take the following job description and resume summary to 
generate a numbered list of ten interview questions specific to the candidate and job description.



JOB DESCRIPTION:
Company: Instalily.ai
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



RESUME SUMMARY:
{resume_summary}


INTERVIEW QUESTIONS:
'''

interview_prompt = PromptTemplate(
    input_variables=["resume_summary"],
    template=interview_prompt_template
)

interview_question_chain = LLMChain(llm=llm, prompt=interview_prompt)

num_docs = len(pages)
print(f"There are {num_docs} total resumes.\n")

# Generating summaries for each resume.
for resume_page in pages:
    resume_chunks = text_splitter.create_documents([resume_page.page_content])

    num_tokens = llm.get_num_tokens(resume_page.page_content)
    page_num = resume_page.metadata['page'] + 1

    print(f"Resume #{page_num} has {num_tokens} tokens")

    resume_summary = summarization_chain.run(resume_chunks).strip()
    print(resume_summary)

    interview_questions = interview_question_chain.run(resume_summary)
    print(f"{interview_questions}\n")
