from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.embeddings import GPT4AllEmbeddings

DATA_PATH = "data"
DB_PATH = "vectorstores/db/"


def create_vector_db():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    print(f"Processed {len(documents)} pdf files")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embedding = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf")
    vectorstore = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=DB_PATH)
    vectorstore.persist()


create_vector_db()
