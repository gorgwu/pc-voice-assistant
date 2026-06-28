from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


class VectorStore:

    DB_PATH = "faiss_index"

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    def build_index(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=150
        )

        chunks = splitter.split_documents(documents)

        print(f"Chunk count: {len(chunks)}")

        vector_store = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        vector_store.save_local(self.DB_PATH)

    def load_index(self):

        if not os.path.exists(self.DB_PATH):
            raise Exception("FAISS index not found.")

        return FAISS.load_local(
            self.DB_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )