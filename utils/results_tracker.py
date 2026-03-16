"""
ResultsTracker — application-level facade over the storage layer.

Keeps a single, stable public API so the rest of the app (app.py, auth.py,
etc.) never needs to know which storage backend is active.

Storage selection is handled by utils.storage.make_repositories:
  • PostgreSQL  — when DATABASE_URL is set and reachable
  • File-based  — fallback for local development

Domain responsibilities are split into three focused repositories:
  • UserRepository       — profiles and roles
  • TestRepository       — test attempts and results
  • VocabularyRepository — vocabulary notes
"""

import os
from typing import Dict, List, Optional

from utils.storage import make_repositories, UserRepository, TestRepository, VocabularyRepository


class ResultsTracker:
    """Thin facade that delegates to the appropriate storage repositories."""

    def __init__(self, users_dir: str = "users", database_url: str | None = None):
        self._users: UserRepository
        self._tests: TestRepository
        self._vocab: VocabularyRepository

        self._users, self._tests, self._vocab = make_repositories(
            users_dir=users_dir,
            database_url=database_url,
        )

    # ------------------------------------------------------------------
    # User profile
    # ------------------------------------------------------------------

    def get_user_profile(self, user_email: str) -> Dict:
        return self._users.get(user_email)

    def save_user_profile(self, user_email: str, profile: Dict) -> None:
        self._users.save(user_email, profile)

    def get_or_create_user(self, user_email: str) -> Dict:
        return self._users.get_or_create(user_email)

    def update_user_role(self, user_email: str, role: str) -> None:
        self._users.update_role(user_email, role)

    def list_all_users(self) -> List[str]:
        return self._users.list_all()

    # ------------------------------------------------------------------
    # Test history
    # ------------------------------------------------------------------

    def save_test_result(
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
        self._tests.save_result(
            user_email, test_num, skill, part_num,
            answers, correct_answers, score, max_score, attempt_id,
        )

    def complete_test_attempt(self, user_email: str, test_num: int, attempt_id: str) -> None:
        self._tests.complete_attempt(user_email, test_num, attempt_id)

    def get_user_test_history(self, user_email: str, test_num: int) -> Dict:
        return self._tests.get_history(user_email, test_num)

    def get_all_tests_summary(self, user_email: str) -> Dict[int, Dict]:
        return self._tests.get_all_summary(user_email)

    # ------------------------------------------------------------------
    # Vocabulary notes
    # ------------------------------------------------------------------

    def save_vocabulary_note(
        self,
        user_email: str,
        test_num: int,
        skill: str,
        part_num: int,
        word: str,
        definition: str,
        context: str = "",
    ) -> str:
        return self._vocab.save(user_email, test_num, skill, part_num, word, definition, context)

    def get_vocabulary_notes(
        self,
        user_email: str,
        test_num: Optional[int] = None,
        skill: Optional[str] = None,
        part_num: Optional[int] = None,
    ) -> List[Dict]:
        return self._vocab.get(user_email, test_num, skill, part_num)

    def delete_vocabulary_note(self, user_email: str, note_id: str) -> bool:
        return self._vocab.delete(user_email, note_id)

    def update_vocabulary_note(
        self,
        user_email: str,
        note_id: str,
        word: Optional[str] = None,
        definition: Optional[str] = None,
        context: Optional[str] = None,
    ) -> bool:
        return self._vocab.update(user_email, note_id, word, definition, context)
