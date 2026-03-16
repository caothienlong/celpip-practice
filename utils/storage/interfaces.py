"""
Abstract repository interfaces for the storage layer.

Every storage backend (file-based, PostgreSQL, future S3, etc.) must
implement these three protocols.  All concrete implementations live in
their own modules; nothing in the rest of the application should import
them directly — always go through the factory.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserRepository(ABC):
    """Manages user profiles and roles."""

    @abstractmethod
    def get(self, email: str) -> Dict:
        """Return the profile dict for *email*. Creates a default if missing."""

    @abstractmethod
    def save(self, email: str, profile: Dict) -> None:
        """Persist (upsert) the profile dict."""

    @abstractmethod
    def get_or_create(self, email: str) -> Dict:
        """Return profile, creating and persisting a default one if absent."""

    @abstractmethod
    def update_role(self, email: str, role: str) -> None:
        """Change the role field for *email*."""

    @abstractmethod
    def list_all(self) -> List[str]:
        """Return a list of all known email addresses."""


# ---------------------------------------------------------------------------
# Test history
# ---------------------------------------------------------------------------

class TestRepository(ABC):
    """Manages test attempts and results."""

    @abstractmethod
    def save_result(
        self,
        user_email: str,
        test_num: int,
        skill: str,
        part_num: int,
        answers: Dict,
        correct_answers: Dict,
        score: int,
        max_score: int,
        attempt_id: str,
    ) -> None:
        """Persist the result for a single part inside an attempt."""

    @abstractmethod
    def complete_attempt(
        self,
        user_email: str,
        test_num: int,
        attempt_id: str,
    ) -> None:
        """Mark an attempt as completed and compute its totals."""

    @abstractmethod
    def get_history(self, user_email: str, test_num: int) -> Dict:
        """Return attempt history for one test number."""

    @abstractmethod
    def get_all_summary(self, user_email: str) -> Dict[int, Dict]:
        """Return a summary dict keyed by test number."""


# ---------------------------------------------------------------------------
# Vocabulary notes
# ---------------------------------------------------------------------------

class VocabularyRepository(ABC):
    """Manages per-user vocabulary notes."""

    @abstractmethod
    def save(
        self,
        user_email: str,
        test_num: int,
        skill: str,
        part_num: int,
        word: str,
        definition: str,
        context: str = "",
    ) -> str:
        """Persist a new note and return its generated note_id."""

    @abstractmethod
    def get(
        self,
        user_email: str,
        test_num: Optional[int] = None,
        skill: Optional[str] = None,
        part_num: Optional[int] = None,
    ) -> List[Dict]:
        """Return notes, optionally filtered."""

    @abstractmethod
    def delete(self, user_email: str, note_id: str) -> bool:
        """Delete a note.  Returns True if a row was removed."""

    @abstractmethod
    def update(
        self,
        user_email: str,
        note_id: str,
        word: Optional[str] = None,
        definition: Optional[str] = None,
        context: Optional[str] = None,
    ) -> bool:
        """Update fields of an existing note.  Returns True if found."""
