# Content of utils.py
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.pdf import PyPDFLoader
import datetime

def load_db(file, chain_type, k):
    loader = PyPDFLoader(file)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs1 = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = DocArrayInMemorySearch.from_documents(docs1, embeddings)

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo" if datetime.datetime.now().date() >= datetime.date(2023, 9, 2) else "gpt-3.5-turbo-0301", temperature=0),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )

    return qa
