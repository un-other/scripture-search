"""
This module contains the ScriptureSearchTool class, which is a tool that uses
semantic search to retrieve relevant scriptures for a given query.
"""

from typing import Optional

from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool

DEFAULT_K = 10

class ScriptureSearchTool(Tool):
    name = "scripture_search_tool"
    description = (
        "Uses semantic search to retrieve relevant scriptures for a given query."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "A user query. Find the most relevant scriptures for this query.",
        },
        "k": {
            "type": "integer",
            "description": "The number of results to retrieve. Defaults to 10.",
            "nullable": True,
        },
    }
    output_type = "string"

    def __init__(self, docs: list[Document], default_k: int = DEFAULT_K, **kwargs):
        """
        Initialize the ScriptureSearchTool.

        Args:
            docs (list[Document]): The list of documents to search from.
        """
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(docs, k=default_k)

    def forward(self, query: str, k: Optional[int] = None) -> str:
        """
        Use semantic search to retrieve the top k most relevant scriptures for a given query.

        Args:
            query (str): The query to search on.
            k (Optional[int]): The number of results to retrieve. Defaults to 10.

        Returns:
            str: A string containing the top k most relevant pieces of scripture.
        """
        docs = self.search(query, k)
        output = "\n The following scriptures may be helpful:\n"
        for doc in docs:
            output += (
                f"\n\n===== {self._get_metadata_str(doc)} =====\n"
                + doc.metadata["full_text"]
            )
        return output

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

    def _get_metadata_str(self, doc: Document):
        """
        Get a string representation of the metadata for a given document.
        """
        return (
            f"ID: {doc.metadata['id']} | Scripture: {doc.metadata['title']} "
            f"| source: {doc.metadata['url_source']}"
        )
