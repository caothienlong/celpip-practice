"""
Storage layer — repository interfaces and factory.

Usage:
    from utils.storage import make_repositories, UserRepository, TestRepository, VocabularyRepository
"""

from .interfaces import UserRepository, TestRepository, VocabularyRepository
from .factory import make_repositories

__all__ = [
    "UserRepository",
    "TestRepository",
    "VocabularyRepository",
    "make_repositories",
]
