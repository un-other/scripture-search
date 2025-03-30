"""
This module contains the ScriptureSearchTool class, which is a tool that uses
semantic search to retrieve relevant scriptures for a given query.
"""

from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool


class ScriptureSearchTool(Tool):
    name = "scripture_search_tool"
    description = (
        "Uses semantic search to retrieve relevant scriptures for a given query."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "A user query. Find the most relevant scriptures for this query.",
        }
    }
    output_type = "string"

    def __init__(self, docs: list[Document], top_k: int = 10, **kwargs):
        """
        Initialize the ScriptureSearchTool.

        Args:
            docs (list[Document]): The list of documents to search from.
            top_k (int): The number of results to retrieve.
        """
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(docs, k=top_k)

    def forward(self, query: str) -> str:
        """
        Use semantic search to retrieve the top k most relevant scriptures for a given query.

        Args:
            query (str): The query to search on.

        Returns:
            str: A string containing the top k most relevant pieces of scripture.
        """
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(query)
        output = "\n The following scriptures may be helpful:\n"
        for doc in docs:
            output += (
                f"\n\n===== {self._get_metadata_str(doc)} =====\n" + doc.page_content
            )
        return output

    def _get_metadata_str(self, doc: Document):
        """
        Get a string representation of the metadata for a given document.
        """
        return (
            f"Scripture: {doc.metadata['title']} | source: {doc.metadata['url_source']}"
        )
