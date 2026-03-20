from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
def process_pdf(file_path):
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings()

    
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore


def get_answer(vectorstore, query):
    docs = vectorstore.similarity_search(query)
    context = " ".join([doc.page_content for doc in docs])

    return context
