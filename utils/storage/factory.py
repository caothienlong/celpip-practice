"""
Storage factory.

Decides which backend to use based on DATABASE_URL and returns the three
repository instances the application needs.
"""

import logging
import os
from typing import Optional, Tuple

from .interfaces import UserRepository, TestRepository, VocabularyRepository

logger = logging.getLogger(__name__)


def make_repositories(
    users_dir: str = "users",
    database_url: Optional[str] = None,
) -> Tuple[UserRepository, TestRepository, VocabularyRepository]:
    """
    Return (user_repo, test_repo, vocab_repo).

    Uses PostgreSQL when *database_url* (or the DATABASE_URL env var) is
    available and psycopg2 connects successfully; falls back to file storage.
    """
    url = database_url or os.getenv("DATABASE_URL")

    if url:
        try:
            from utils.database import Database
            from .db_storage import DbUserRepository, DbTestRepository, DbVocabularyRepository

            db = Database(url)
            if db.is_available:
                logger.info("Storage backend: PostgreSQL")
                return (
                    DbUserRepository(db),
                    DbTestRepository(db),
                    DbVocabularyRepository(db),
                )
            logger.warning("DATABASE_URL set but connection failed — falling back to file storage")
        except Exception as exc:
            logger.warning("Could not initialise DB storage (%s) — falling back to file storage", exc)

    from .file_storage import FileUserRepository, FileTestRepository, FileVocabularyRepository

    logger.info("Storage backend: file-based (%s)", users_dir)
    return (
        FileUserRepository(users_dir),
        FileTestRepository(users_dir),
        FileVocabularyRepository(users_dir),
    )
