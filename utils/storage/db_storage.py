"""
PostgreSQL-backed storage implementations.

Delegates all persistence to utils.database.Database, which owns the
connection pool and raw SQL.  These classes simply adapt its methods
to the repository interfaces so the rest of the app stays storage-agnostic.
"""

import logging
from typing import Dict, List, Optional

from utils.database import Database
from .interfaces import UserRepository, TestRepository, VocabularyRepository

logger = logging.getLogger(__name__)


class DbUserRepository(UserRepository):
    def __init__(self, db: Database):
        self._db = db

    def get(self, email: str) -> Dict:
        return self._db.get_user_profile(email)

    def save(self, email: str, profile: Dict) -> None:
        self._db.save_user_profile(email, profile)

    def get_or_create(self, email: str) -> Dict:
        return self._db.get_or_create_user(email)

    def update_role(self, email: str, role: str) -> None:
        self._db.update_user_role(email, role)

    def list_all(self) -> List[str]:
        return self._db.list_all_users()


class DbTestRepository(TestRepository):
    def __init__(self, db: Database):
        self._db = db

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
        self._db.save_test_result(
            user_email, test_num, skill, part_num,
            answers, correct_answers, score, max_score, attempt_id,
        )

    def complete_attempt(self, user_email: str, test_num: int, attempt_id: str) -> None:
        self._db.complete_test_attempt(user_email, test_num, attempt_id)

    def get_history(self, user_email: str, test_num: int) -> Dict:
        return self._db.get_user_test_history(user_email, test_num)

    def get_all_summary(self, user_email: str) -> Dict[int, Dict]:
        return self._db.get_all_tests_summary(user_email)


class DbVocabularyRepository(VocabularyRepository):
    def __init__(self, db: Database):
        self._db = db

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
        return self._db.save_vocabulary_note(
            user_email, test_num, skill, part_num, word, definition, context
        )

    def get(
        self,
        user_email: str,
        test_num: Optional[int] = None,
        skill: Optional[str] = None,
        part_num: Optional[int] = None,
    ) -> List[Dict]:
        return self._db.get_vocabulary_notes(user_email, test_num, skill, part_num)

    def delete(self, user_email: str, note_id: str) -> bool:
        return self._db.delete_vocabulary_note(user_email, note_id)

    def update(
        self,
        user_email: str,
        note_id: str,
        word: Optional[str] = None,
        definition: Optional[str] = None,
        context: Optional[str] = None,
    ) -> bool:
        return self._db.update_vocabulary_note(user_email, note_id, word, definition, context)
