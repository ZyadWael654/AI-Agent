import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from config import CHROMA_DIR, KNOWLEDGE_FILE, EMBEDDING_MODEL


def get_retriever():
    print("=== Initializing Vector Database (RAG)... ===")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if not os.path.exists(CHROMA_DIR):
        print("=== No existing DB found, building from knowledge.txt... ===")
        loader = TextLoader(KNOWLEDGE_FILE, encoding="utf-8")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=0,
            separators=["\n\n", "\n"]
        )
        docs = text_splitter.split_documents(documents)

        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=CHROMA_DIR
        )
    else:
        print("=== Loading existing Vector Database... ===")
        vector_store = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )

    print("=== Vector Database Ready! ===")
    return vector_store.as_retriever(search_kwargs={"k": 3})