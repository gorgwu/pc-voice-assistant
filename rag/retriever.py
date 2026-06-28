class Retriever:

    def __init__(
        self,
        vector_store
    ):

        self.vector_store = (
            vector_store
        )

    def retrieve(
        self,
        query: str
    ):

        docs = (
            self.vector_store.similarity_search(
                query,
                k=3
            )
        )

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )