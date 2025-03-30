from pathlib import Path

import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from smolagents import Agent
from smolagents.memory import ConversationMemory
from smolagents.tools import Tool


class SuttaSearchTool(Tool):
    def __init__(self, vector_store):
        super().__init__(
            name="scripture_search_tool",
            description="Search through Buddhist suttas to find relevant passages",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant suttas",
                }
            },
        )
        self.vector_store = vector_store

    def run(self, query: str) -> str:
        # Search for relevant documents
        docs = self.vector_store.similarity_search(query, k=3)

        # Format the results
        results = []
        for doc in docs:
            results.append(
                f"Title: {doc.metadata['title']}\nText: {doc.page_content}\n"
            )

        return "\n".join(results)


def load_and_process_data(csv_path: str) -> pd.DataFrame:
    """Load and process the CSV data."""
    df = pd.read_csv(csv_path)
    return df


def create_vector_store(df: pd.DataFrame) -> FAISS:
    """Create a FAISS vector store from the DataFrame."""
    # Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create documents for the vector store
    documents = []
    for _, row in df.iterrows():
        doc = {
            "page_content": row["text"],
            "metadata": {
                "title": row["title"],
                "collection": row["collection"],
                "url_source": row["url_source"],
                "religion": row["religion"],
                "subgroup": row["subgroup"],
                "source": row["source"],
                "translation_source": row["translation_source"],
            },
        }
        documents.append(doc)

    # Create and return the vector store
    return FAISS.from_documents(documents, embeddings)


def create_agent(vector_store: FAISS) -> Agent:
    """Create an agent with RAG capabilities."""
    # Create the search tool
    search_tool = SuttaSearchTool(vector_store)

    # Create the agent with the search tool
    agent = Agent(
        tools=[search_tool],
        memory=ConversationMemory(),
        system_prompt="""You are a helpful assistant specializing in Buddhist texts and teachings.
        When a user asks a question, use the search_suttas tool to find relevant passages from the suttas.
        Then, provide a thoughtful response based on the found passages.
        Always cite the sources you use in your response.""",
    )

    return agent


def main():
    # Load the data
    data_path = Path("data/dhama_talks_suttas.csv")
    df = load_and_process_data(str(data_path))

    # Create the vector store
    vector_store = create_vector_store(df)

    # Create the agent
    agent = create_agent(vector_store)

    # Example usage
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == "quit":
            break

        response = agent.run(query)
        print("\nResponse:", response)


if __name__ == "__main__":
    main()
