import os
import hashlib

from rag.pdf_loader import (
    PDFLoader
)

from rag.vector_store import (
    VectorStore
)


class IndexManager:

    HASH_FILE = (
        "faiss_index/pdf_hash.txt"
    )

    def get_file_hash(
        self,
        file_path: str
    ):

        with open(
            file_path,
            "rb"
        ) as f:

            file_bytes = f.read()

        return hashlib.md5(
            file_bytes
        ).hexdigest()

    def needs_rebuild(
        self,
        pdf_path: str
    ):

        if not os.path.exists(
            self.HASH_FILE
        ):

            return True

        current_hash = (
            self.get_file_hash(
                pdf_path
            )
        )

        with open(
            self.HASH_FILE,
            "r"
        ) as f:

            saved_hash = (
                f.read()
            )

        return (
            current_hash
            != saved_hash
        )

    def build_index(
        self,
        pdf_path: str
    ):

        print(
            "\nBuilding FAISS index..."
        )

        loader = PDFLoader()

        documents = (
            loader.load_pdf(
                pdf_path
            )
        )

        vector_store = (
            VectorStore()
        )

        vector_store.build_index(
            documents
        )

        current_hash = (
            self.get_file_hash(
                pdf_path
            )
        )

        os.makedirs(
            "faiss_index",
            exist_ok=True
        )

        with open(
            self.HASH_FILE,
            "w"
        ) as f:

            f.write(
                current_hash
            )

        print(
            "\nIndex build complete."
        )