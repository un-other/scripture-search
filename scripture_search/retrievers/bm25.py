"""BM25 retriever tool."""

from typing import Optional

from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever

DEFAULT_K = 10


class BM25RetrieverTool:
    """
    Uses semantic search to retrieve relevant scriptures for a given query.
    """

    def __init__(self, docs: list[Document], default_k: int = DEFAULT_K):
        """
        Initialize the BM25RetrieverTool.

        Args:
            docs (list[Document]): The list of documents to search from.
            default_k (int): The default number of results to retrieve.
        """
        self.retriever = BM25Retriever.from_documents(docs, k=default_k)

    def search(self, query: str, k: Optional[int] = None) -> list[Document]:
        """
        Use semantic search to retrieve the top k most relevant scriptures for a given query.

        Args:
            query (str): The query to search on.
            k (Optional[int]): The number of results to retrieve. Defaults to 10.

        Returns:
            list[Document]: A list of the top k most relevant scriptures.
        """
        assert isinstance(query, str), "Your search query must be a string"
        if k is None:
            return self.retriever.invoke(query)

        self.retriever.k = k  # Update the retriever's k value
        docs = self.retriever.invoke(query)
        self.retriever.k = DEFAULT_K  # Reset the retriever's k value
        return docs
