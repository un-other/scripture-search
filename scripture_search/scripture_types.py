import re
from typing import Optional

from pydantic import BaseModel
from unidecode import unidecode


class SuttaText(BaseModel):
    """Class to hold relevant data for a sutta."""

    collection: str
    title: str
    original_text: str
    url_source: str
    clean_text: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = self._decode_text(self.title)
        self.original_text = self._decode_text(self.original_text)
        self.clean_text = self._clean_text(self.original_text)

    @staticmethod
    def _decode_text(text: str) -> str:
        """
        Attempts to fix common text encoding issues in Buddhist scriptures.

        This function handles cases where text might have been incorrectly encoded,
        particularly with special characters and diacritics common in Pali and Sanskrit
        (e.g., ā, ī, ū, ṃ, etc.).

        The function tries multiple decoding strategies in order:
        1. Latin-1 to UTF-8: Handles cases where UTF-8 text was incorrectly stored as Latin-1
        2. Latin-1 to Latin-1: Handles cases where text is actually in Latin-1 encoding
        3. Returns original: If all decoding attempts fail, returns the original text

        Args:
            text: The text string that may have encoding issues

        Returns:
            The decoded text if successful, or the original text if decoding fails
        """
        try:
            return text.encode("latin1").decode("utf-8")
        except UnicodeDecodeError:
            pass

        try:
            return text.encode("latin1").decode("latin1")
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass

        return text

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Computed field that returns the cleaned version of the text.
        The cleaning process:
        1. Removes diacritics using unidecode
        2. Normalizes whitespace
        3. Strips leading/trailing whitespace
        """
        text = unidecode(text)  # Remove diacritics
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace
        text = text.strip()  # Remove leading and trailing whitespace
        return text
