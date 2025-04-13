"""Module to search for scriptures using an agent."""

import pandas as pd
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from scripture_search.logger import get_logger
from scripture_search.retrievers.bm25 import BM25RetrieverTool

load_dotenv()

LOGGER = get_logger(__name__)

K_SEARCH_RESULTS = 10


class SimpleSearch:
    """Simple Search."""

    def __init__(self):
        self.dhamma_talks_suttas = self._load_data()
        self.dhamma_talks_suttas = self._preprocess(self.dhamma_talks_suttas)
        self.documents = self.dhamma_talks_suttas.apply(
            self._row_to_doc, axis=1
        ).tolist()
        self.docs_processed = self._split_docs(self.documents)

        self.bm25_retriever_tool = BM25RetrieverTool(self.docs_processed)

    def run(self, query: str) -> list[Document]:
        """Run the simple search."""
        return self.bm25_retriever_tool.search(query, k=K_SEARCH_RESULTS)

    @staticmethod
    def _load_data() -> pd.DataFrame:
        """Load the data."""
        LOGGER.debug("Loading data...")
        dhamma_talks_suttas = pd.read_csv("data/dhamma_talks_suttas.csv", index_col=0)
        dhamma_talks_suttas["id"] = dhamma_talks_suttas.index.to_list()
        LOGGER.debug("Data shape: %s", dhamma_talks_suttas.shape)
        LOGGER.debug("Data head: %s", dhamma_talks_suttas.head())
        return dhamma_talks_suttas

    @staticmethod
    def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the data."""
        LOGGER.debug("Preprocessing data...")

        LOGGER.debug("Data shape before: %s", df.shape)
        df = df.dropna(subset=["clean_text"])
        LOGGER.debug("Data shape after dropping na: %s", df.shape)
        df = df.drop_duplicates(subset=["clean_text"])
        LOGGER.debug("Data shape after dropping duplicates: %s", df.shape)

        return df

    @staticmethod
    def _row_to_doc(row: pd.Series) -> Document:
        """Convert a row to a document."""
        return Document(
            page_content=row["clean_text"],
            metadata=row.to_dict(),
        )

    @staticmethod
    def _split_docs(documents: list[Document]) -> list[Document]:
        """Split the documents into smaller chunks for more efficient search."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        return text_splitter.split_documents(documents)
