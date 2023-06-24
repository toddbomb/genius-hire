from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import (PyPDFLoader,DataFrameLoader)
#from langchain.document_loaders import GitLoader
import pandas as pd
import nbformat
from nbconvert import PythonExporter
import textract
import os
import re
import glob


def get_text_splits(text_file):
    """
    Text Files
    """
    with open(text_file,'r') as txt:
        data = txt.read()

    textSplit = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=15, length_function=len)
    doc_list = textSplit.split_text(data)

    return doc_list

def files_other(file_path):
    '''
    file type not listed, get text from file using textract package
    '''
    data = str(textract.process(file_path))

    textSplit = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=15, length_function=len)
    doc_list = textSplit.split_text(data)

    return doc_list

def get_excel_splits(excel_file): #target_col,sheet_name
    """
    Excel splits, functionally loads so that headings are preserved with every embedding
    """
    trialDF = pd.read_excel(io=excel_file,engine='openpyxl')#,sheet_name=sheet_name)
    df_loader = DataFrameLoader(trialDF,page_content_column= trialDF.columns[0])
    excel_docs = df_loader.load()

    return excel_docs

def get_csv_splits(csv_file):
    """
    Csv
    """
    csvLoader = CSVLoader(csv_file)
    csvdocs = csvLoader.load()

    return csvdocs

def get_ipynb_splits(notebook):
    """
    Read ipynb as python script, then splits script data directly
    """

    with open(notebook) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

    exporter = PythonExporter()
    source, meta = exporter.from_notebook_node(nb)

    #Python file data is in the source variable
    textSplit = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=15, length_function=len)
    doc_list = textSplit.split_text(source)

    return doc_list  
     
def get_git_files(repo_link, folder_path, file_ext):
    """
    Get github from repo link
    """

    # eg. loading only python files
    git_loader = GitLoader(clone_url=repo_link, repo_path=folder_path, 
        file_filter=lambda file_path: file_path.endswith(file_ext))

    # Will take each file individual document
    git_docs = git_loader.load()
    textSplit = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=15, length_function=len)
    doc_list = []

    # Pages will be list of pages, so need to modify the loop
    for code in git_docs:
        code_splits = textSplit.split_text(code.page_content)
        doc_list.extend(code_splits)

    return doc_list

def embed_index(doc_list, embed_fn, index_store):
    """
    Function takes in existing vector_store, new doc_list, and embedding function that is 
    initialized on appropriate model (local or online)
    * New embedding is merged with the existing index. 
    * If no index given a new one is created.
    """

    #check whether the doc_list is documents, or text
    try:
        faiss_db = FAISS.from_documents(doc_list, embed_fn)  
    except Exception as e:
        faiss_db = FAISS.from_texts(doc_list,embed_fn)
    
    if os.path.exists(index_store):
        local_db = FAISS.load_local(index_store,embed_fn)
        #merging the new embedding with the existing index store
        local_db.merge_from(faiss_db)
        print("Merge completed")
        local_db.save_local(index_store)
        print("Updated index saved")
    else:
        faiss_db.save_local(folder_path=index_store)
        print("New store created...")
    
def get_docs_length(index_path, embed_fn):

    test_index = FAISS.load_local(index_path, embeddings=embed_fn)
    test_dict = test_index.docstore._dict
    return len(test_dict.values())  

def get_filename(text):
    '''
    Get the file name from path
    '''
    match = re.search(r'[^/]+$', text)
    if match:
        return match.group(0)
    else:
        return None

def get_filetype(text):
    '''
    Get the file type from path
    '''
    match = re.search(r'[^.]+$', text)
    if match:
        return match.group(0)
    else:
        return None

def run_embeddings(file_path):
    '''
    call ingest functions based on file type
    '''
    #file_name = get_filename(file_path)
    file_type = get_filetype(file_path)

    # get doc list for any file type using mapper
    try:
        doc_list = file_type_map[file_type](file_path)
    except:
        doc_list = files_other(file_path)

    # get embeddings 
    index_store = os.getcwd()+'/backend/src/database/new_index'
    embed_index(doc_list=doc_list, embed_fn=embeddings, index_store=index_store)

file_type_map = {'txt': get_text_splits,
    'xls': get_excel_splits,
    'xlsx': get_excel_splits,
    'csv': get_csv_splits,
    'ipynb': get_ipynb_splits,
    'github link': get_git_files} # (repo_link, folder_path, file_ext)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def call_embeddings():

    file_paths =  glob.glob("/Users/cristinconnerney/Desktop/Crunchlabs/*")

    for file in file_paths:
        run_embeddings(file)


#print("docs length: ",get_docs_length(index_path='new_index',embed_fn=embeddings))

#test_index = FAISS.load_local("new_index",embeddings)

#print(test_index.similarity_search_with_relevance_scores("metrics for google Ads performance"))