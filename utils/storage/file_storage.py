"""
File-based storage implementations.

Used automatically when DATABASE_URL is not set (local development).
Data is persisted as JSON files under users/{sanitized_email}/*.json.
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from .interfaces import UserRepository, TestRepository, VocabularyRepository

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared file-system helpers
# ---------------------------------------------------------------------------

def _sanitize_email(email: str) -> str:
    email = email.lower().strip()
    safe = email.replace("@", "_")
    safe = re.sub(r"\.(com|net|org|edu|gov|io|co|uk|ca|au)$", "", safe)
    safe = re.sub(r"[^\w\-]", "_", safe)
    return safe


def _user_folder(users_dir: str, email: str) -> str:
    return os.path.join(users_dir, _sanitize_email(email))


def _read_json(path: str, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
    except Exception as exc:
        logger.error("Error reading %s: %s", path, exc)
    return default


def _write_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
    except Exception as exc:
        logger.error("Error writing %s: %s", path, exc)


# ---------------------------------------------------------------------------
# UserRepository
# ---------------------------------------------------------------------------

class FileUserRepository(UserRepository):
    def __init__(self, users_dir: str = "users"):
        self._dir = users_dir
        os.makedirs(users_dir, exist_ok=True)

    def _profile_path(self, email: str) -> str:
        return os.path.join(_user_folder(self._dir, email), "profile.json")

    def get(self, email: str) -> Dict:
        return _read_json(
            self._profile_path(email),
            default={
                "email": email,
                "role": "Basic",
                "created_at": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
            },
        )

    def save(self, email: str, profile: Dict) -> None:
        _write_json(self._profile_path(email), profile)

    def get_or_create(self, email: str) -> Dict:
        folder = _user_folder(self._dir, email)
        os.makedirs(folder, exist_ok=True)
        profile = self.get(email)
        profile["last_accessed"] = datetime.now().isoformat()
        self.save(email, profile)
        return profile

    def update_role(self, email: str, role: str) -> None:
        profile = self.get(email)
        profile["role"] = role
        self.save(email, profile)

    def list_all(self) -> List[str]:
        users = []
        if not os.path.exists(self._dir):
            return users
        for folder_name in os.listdir(self._dir):
            folder_path = os.path.join(self._dir, folder_name)
            profile_path = os.path.join(folder_path, "profile.json")
            if os.path.isdir(folder_path) and os.path.exists(profile_path):
                data = _read_json(profile_path, {})
                if "email" in data:
                    users.append(data["email"])
        return users


# ---------------------------------------------------------------------------
# TestRepository
# ---------------------------------------------------------------------------

class FileTestRepository(TestRepository):
    def __init__(self, users_dir: str = "users"):
        self._dir = users_dir

    def _history_path(self, email: str) -> str:
        return os.path.join(_user_folder(self._dir, email), "test_history.json")

    def _load(self, email: str) -> Dict:
        return _read_json(self._history_path(email), default={"tests": {}})

    def _persist(self, email: str, history: Dict) -> None:
        _write_json(self._history_path(email), history)

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
        history = self._load(user_email)
        test_key = f"test_{test_num}"

        history["tests"].setdefault(
            test_key,
            {"test_number": test_num, "attempts": []},
        )

        attempts = history["tests"][test_key]["attempts"]
        attempt = next((a for a in attempts if a["attempt_id"] == attempt_id), None)
        if attempt is None:
            attempt = {
                "attempt_id": attempt_id,
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "skills": {},
            }
            attempts.append(attempt)

        attempt["skills"].setdefault(
            skill,
            {"skill_name": skill, "parts": {}, "total_score": 0, "total_max": 0},
        )
        attempt["skills"][skill]["parts"][str(part_num)] = {
            "part_number": part_num,
            "answers": answers,
            "correct_answers": correct_answers,
            "score": score,
            "max_score": max_score,
            "timestamp": datetime.now().isoformat(),
        }

        skill_data = attempt["skills"][skill]
        skill_data["total_score"] = sum(p["score"] for p in skill_data["parts"].values())
        skill_data["total_max"] = sum(p["max_score"] for p in skill_data["parts"].values())

        self._persist(user_email, history)

    def complete_attempt(self, user_email: str, test_num: int, attempt_id: str) -> None:
        history = self._load(user_email)
        test_key = f"test_{test_num}"

        if test_key not in history["tests"]:
            return

        for attempt in history["tests"][test_key]["attempts"]:
            if attempt["attempt_id"] == attempt_id:
                attempt["completed_at"] = datetime.now().isoformat()
                total_score = sum(s["total_score"] for s in attempt["skills"].values())
                total_max = sum(s["total_max"] for s in attempt["skills"].values())
                attempt["total_score"] = total_score
                attempt["total_max"] = total_max
                attempt["percentage"] = (
                    round(total_score / total_max * 100, 1) if total_max > 0 else 0
                )
                break

        self._persist(user_email, history)

    def get_history(self, user_email: str, test_num: int) -> Dict:
        history = self._load(user_email)
        test_key = f"test_{test_num}"

        if test_key not in history["tests"]:
            return {"attempt_count": 0, "latest_attempt": None, "all_attempts": []}

        completed = [
            a for a in history["tests"][test_key]["attempts"] if a.get("completed_at")
        ]
        latest = max(completed, key=lambda x: x["completed_at"]) if completed else None
        return {
            "attempt_count": len(completed),
            "latest_attempt": latest,
            "all_attempts": completed,
        }

    def get_all_summary(self, user_email: str) -> Dict[int, Dict]:
        history = self._load(user_email)
        summary: Dict[int, Dict] = {}

        for test_data in history["tests"].values():
            test_num = test_data["test_number"]
            completed = [a for a in test_data["attempts"] if a.get("completed_at")]
            if completed:
                latest = max(completed, key=lambda x: x["completed_at"])
                summary[test_num] = {
                    "attempt_count": len(completed),
                    "latest_score": latest.get("total_score", 0),
                    "latest_max": latest.get("total_max", 0),
                    "latest_percentage": latest.get("percentage", 0),
                    "latest_date": latest.get("completed_at", ""),
                }

        return summary


# ---------------------------------------------------------------------------
# VocabularyRepository
# ---------------------------------------------------------------------------

class FileVocabularyRepository(VocabularyRepository):
    def __init__(self, users_dir: str = "users"):
        self._dir = users_dir

    def _notes_path(self, email: str) -> str:
        return os.path.join(_user_folder(self._dir, email), "vocabulary_notes.json")

    def _load(self, email: str) -> Dict:
        return _read_json(self._notes_path(email), default={"tests": {}})

    def _persist(self, email: str, notes: Dict) -> None:
        _write_json(self._notes_path(email), notes)

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
        notes = self._load(user_email)
        test_key = f"test_{test_num}"
        skill_key = f"{skill}_part_{part_num}"

        notes["tests"].setdefault(test_key, {})
        notes["tests"][test_key].setdefault(skill_key, [])

        note_id = f"{test_num}_{skill}_{part_num}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        notes["tests"][test_key][skill_key].append(
            {
                "note_id": note_id,
                "word": word.strip(),
                "definition": definition.strip(),
                "context": context.strip(),
                "created_at": datetime.now().isoformat(),
                "test_num": test_num,
                "skill": skill,
                "part_num": part_num,
            }
        )

        self._persist(user_email, notes)
        return note_id

    def get(
        self,
        user_email: str,
        test_num: Optional[int] = None,
        skill: Optional[str] = None,
        part_num: Optional[int] = None,
    ) -> List[Dict]:
        notes = self._load(user_email)
        all_notes: List[Dict] = []
        for test_data in notes.get("tests", {}).values():
            for note_list in test_data.values():
                all_notes.extend(note_list)

        if test_num is not None:
            all_notes = [n for n in all_notes if n.get("test_num") == test_num]
        if skill is not None:
            all_notes = [n for n in all_notes if n.get("skill") == skill]
        if part_num is not None:
            all_notes = [n for n in all_notes if n.get("part_num") == part_num]

        all_notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return all_notes

    def delete(self, user_email: str, note_id: str) -> bool:
        notes = self._load(user_email)
        for test_data in notes.get("tests", {}).values():
            for skill_key, note_list in test_data.items():
                for i, note in enumerate(note_list):
                    if note.get("note_id") == note_id:
                        del note_list[i]
                        self._persist(user_email, notes)
                        return True
        return False

    def update(
        self,
        user_email: str,
        note_id: str,
        word: Optional[str] = None,
        definition: Optional[str] = None,
        context: Optional[str] = None,
    ) -> bool:
        notes = self._load(user_email)
        for test_data in notes.get("tests", {}).values():
            for note_list in test_data.values():
                for note in note_list:
                    if note.get("note_id") == note_id:
                        if word is not None:
                            note["word"] = word.strip()
                        if definition is not None:
                            note["definition"] = definition.strip()
                        if context is not None:
                            note["context"] = context.strip()
                        note["updated_at"] = datetime.now().isoformat()
                        self._persist(user_email, notes)
                        return True
        return False
