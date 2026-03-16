"""
Database Module for PostgreSQL Storage
Uses PostgreSQL JSON columns to store user data persistently.
Falls back gracefully when DATABASE_URL is not configured.

Tables:
  users          - email, name, provider, role, timestamps
  test_history   - user_email FK, test data as JSONB
  vocabulary_notes - individual notes with indexed columns
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

try:
    import psycopg2
    import psycopg2.extras
    import psycopg2.pool
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


class Database:
    """PostgreSQL database wrapper with connection pooling."""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.pool = None
        self._available = False

        if not self.database_url:
            logger.info("DATABASE_URL not set - using file-based storage")
            return

        if not HAS_PSYCOPG2:
            logger.warning("psycopg2 not installed - using file-based storage")
            return

        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                dsn=self.database_url
            )
            self._init_tables()
            self._available = True
            logger.info("PostgreSQL database connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            self.pool = None

    @property
    def is_available(self) -> bool:
        return self._available and self.pool is not None

    @contextmanager
    def _get_conn(self):
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)

    def _init_tables(self):
        """Create tables if they don't exist."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        email       TEXT PRIMARY KEY,
                        name        TEXT,
                        provider    TEXT,
                        picture     TEXT,
                        role        TEXT NOT NULL DEFAULT 'Basic',
                        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        last_accessed TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );

                    CREATE TABLE IF NOT EXISTS test_history (
                        id          SERIAL PRIMARY KEY,
                        user_email  TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
                        test_num    INTEGER NOT NULL,
                        data        JSONB NOT NULL DEFAULT '{}'::jsonb,
                        updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        UNIQUE(user_email, test_num)
                    );

                    CREATE TABLE IF NOT EXISTS vocabulary_notes (
                        note_id     TEXT PRIMARY KEY,
                        user_email  TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
                        test_num    INTEGER NOT NULL,
                        skill       TEXT NOT NULL,
                        part_num    INTEGER NOT NULL,
                        word        TEXT NOT NULL,
                        definition  TEXT NOT NULL,
                        context     TEXT NOT NULL DEFAULT '',
                        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updated_at  TIMESTAMPTZ
                    );

                    CREATE INDEX IF NOT EXISTS idx_vocab_user
                        ON vocabulary_notes(user_email);
                    CREATE INDEX IF NOT EXISTS idx_vocab_user_test
                        ON vocabulary_notes(user_email, test_num);
                    CREATE INDEX IF NOT EXISTS idx_test_history_user
                        ON test_history(user_email);
                """)

    # ------------------------------------------------------------------ users

    def get_user_profile(self, email: str) -> Dict:
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    return {
                        'email': row['email'],
                        'name': row['name'],
                        'provider': row['provider'],
                        'picture': row['picture'],
                        'role': row['role'],
                        'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                        'last_accessed': row['last_accessed'].isoformat() if row['last_accessed'] else None,
                    }
                return {
                    'email': email,
                    'role': 'Basic',
                    'created_at': datetime.now().isoformat(),
                    'last_accessed': datetime.now().isoformat(),
                }

    def save_user_profile(self, email: str, profile: Dict):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (email, name, provider, picture, role, created_at, last_accessed)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (email) DO UPDATE SET
                        name = COALESCE(EXCLUDED.name, users.name),
                        provider = COALESCE(EXCLUDED.provider, users.provider),
                        picture = COALESCE(EXCLUDED.picture, users.picture),
                        role = COALESCE(EXCLUDED.role, users.role),
                        last_accessed = NOW()
                """, (
                    email,
                    profile.get('name'),
                    profile.get('provider'),
                    profile.get('picture'),
                    profile.get('role', 'Basic'),
                    profile.get('created_at', datetime.now().isoformat()),
                ))

    def get_or_create_user(self, email: str) -> Dict:
        profile = self.get_user_profile(email)
        self.save_user_profile(email, profile)
        return self.get_user_profile(email)

    def update_user_role(self, email: str, role: str):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET role = %s WHERE email = %s",
                    (role, email),
                )

    def list_all_users(self) -> List[str]:
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email FROM users ORDER BY email")
                return [row[0] for row in cur.fetchall()]

    # --------------------------------------------------------- test_history

    def _load_test_history(self, email: str) -> Dict:
        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT test_num, data FROM test_history WHERE user_email = %s",
                    (email,),
                )
                tests = {}
                for row in cur.fetchall():
                    test_key = f"test_{row['test_num']}"
                    tests[test_key] = row['data']
                return {'tests': tests}

    def _save_test_history_for_test(self, email: str, test_num: int, data: Dict):
        """Save history for a single test number."""
        self._ensure_user_exists(email)
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO test_history (user_email, test_num, data, updated_at)
                    VALUES (%s, %s, %s, NOW())
                    ON CONFLICT (user_email, test_num) DO UPDATE SET
                        data = EXCLUDED.data,
                        updated_at = NOW()
                """, (
                    email,
                    test_num,
                    json.dumps(data),
                ))

    def save_test_result(self, user_email, test_num, skill, part_num,
                         answers, correct_answers, score, max_score, attempt_id):
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'

        if test_key not in history['tests']:
            history['tests'][test_key] = {
                'test_number': test_num,
                'attempts': []
            }

        test_data = history['tests'][test_key]

        attempt = None
        for att in test_data['attempts']:
            if att['attempt_id'] == attempt_id:
                attempt = att
                break

        if attempt is None:
            attempt = {
                'attempt_id': attempt_id,
                'started_at': datetime.now().isoformat(),
                'completed_at': None,
                'skills': {}
            }
            test_data['attempts'].append(attempt)

        if skill not in attempt['skills']:
            attempt['skills'][skill] = {
                'skill_name': skill,
                'parts': {},
                'total_score': 0,
                'total_max': 0
            }

        attempt['skills'][skill]['parts'][str(part_num)] = {
            'part_number': part_num,
            'answers': {str(k): v for k, v in answers.items()},
            'correct_answers': {str(k): v for k, v in correct_answers.items()},
            'score': score,
            'max_score': max_score,
            'timestamp': datetime.now().isoformat()
        }

        skill_data = attempt['skills'][skill]
        skill_data['total_score'] = sum(p['score'] for p in skill_data['parts'].values())
        skill_data['total_max'] = sum(p['max_score'] for p in skill_data['parts'].values())

        self._save_test_history_for_test(user_email, test_num, test_data)

        # Touch last_accessed
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET last_accessed = NOW() WHERE email = %s",
                    (user_email,),
                )

    def complete_test_attempt(self, user_email, test_num, attempt_id):
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'

        if test_key in history['tests']:
            test_data = history['tests'][test_key]
            for attempt in test_data['attempts']:
                if attempt['attempt_id'] == attempt_id:
                    attempt['completed_at'] = datetime.now().isoformat()
                    total_score = 0
                    total_max = 0
                    for skill_data in attempt['skills'].values():
                        total_score += skill_data['total_score']
                        total_max += skill_data['total_max']
                    attempt['total_score'] = total_score
                    attempt['total_max'] = total_max
                    attempt['percentage'] = round((total_score / total_max * 100), 1) if total_max > 0 else 0
                    break
            self._save_test_history_for_test(user_email, test_num, test_data)

    def get_user_test_history(self, user_email, test_num) -> Dict:
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'

        if test_key not in history['tests']:
            return {'attempt_count': 0, 'latest_attempt': None, 'all_attempts': []}

        attempts = history['tests'][test_key]['attempts']
        completed = [a for a in attempts if a.get('completed_at')]

        latest = None
        if completed:
            latest = max(completed, key=lambda x: x['completed_at'])

        return {
            'attempt_count': len(completed),
            'latest_attempt': latest,
            'all_attempts': completed
        }

    def get_all_tests_summary(self, user_email) -> Dict[int, Dict]:
        history = self._load_test_history(user_email)
        summary = {}

        for test_key, test_data in history['tests'].items():
            test_num = test_data['test_number']
            completed = [a for a in test_data['attempts'] if a.get('completed_at')]

            if completed:
                latest = max(completed, key=lambda x: x['completed_at'])
                summary[test_num] = {
                    'attempt_count': len(completed),
                    'latest_score': latest.get('total_score', 0),
                    'latest_max': latest.get('total_max', 0),
                    'latest_percentage': latest.get('percentage', 0),
                    'latest_date': latest.get('completed_at', '')
                }

        return summary

    # --------------------------------------------------- vocabulary_notes

    def save_vocabulary_note(self, user_email, test_num, skill, part_num,
                             word, definition, context='') -> str:
        self._ensure_user_exists(user_email)
        note_id = f"{test_num}_{skill}_{part_num}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO vocabulary_notes
                        (note_id, user_email, test_num, skill, part_num, word, definition, context)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    note_id, user_email, test_num, skill, part_num,
                    word.strip(), definition.strip(), context.strip(),
                ))
        return note_id

    def get_vocabulary_notes(self, user_email, test_num=None,
                             skill=None, part_num=None) -> List[Dict]:
        conditions = ["user_email = %s"]
        params: list = [user_email]

        if test_num is not None:
            conditions.append("test_num = %s")
            params.append(test_num)
        if skill is not None:
            conditions.append("skill = %s")
            params.append(skill)
        if part_num is not None:
            conditions.append("part_num = %s")
            params.append(part_num)

        where = " AND ".join(conditions)

        with self._get_conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"SELECT * FROM vocabulary_notes WHERE {where} ORDER BY created_at DESC",
                    params,
                )
                rows = cur.fetchall()
                return [self._row_to_note(r) for r in rows]

    def delete_vocabulary_note(self, user_email, note_id) -> bool:
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM vocabulary_notes WHERE note_id = %s AND user_email = %s",
                    (note_id, user_email),
                )
                return cur.rowcount > 0

    def update_vocabulary_note(self, user_email, note_id,
                               word=None, definition=None, context=None) -> bool:
        sets = []
        params: list = []

        if word is not None:
            sets.append("word = %s")
            params.append(word.strip())
        if definition is not None:
            sets.append("definition = %s")
            params.append(definition.strip())
        if context is not None:
            sets.append("context = %s")
            params.append(context.strip())

        if not sets:
            return False

        sets.append("updated_at = NOW()")
        params.extend([note_id, user_email])

        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE vocabulary_notes SET {', '.join(sets)} WHERE note_id = %s AND user_email = %s",
                    params,
                )
                return cur.rowcount > 0

    # ------------------------------------------------------------ helpers

    def _ensure_user_exists(self, email: str):
        """Insert a minimal user row if it doesn't exist yet."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (email) VALUES (%s)
                    ON CONFLICT (email) DO NOTHING
                """, (email,))

    @staticmethod
    def _row_to_note(row) -> Dict:
        return {
            'note_id': row['note_id'],
            'word': row['word'],
            'definition': row['definition'],
            'context': row['context'],
            'created_at': row['created_at'].isoformat() if row['created_at'] else None,
            'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None,
            'test_num': row['test_num'],
            'skill': row['skill'],
            'part_num': row['part_num'],
        }

    def close(self):
        if self.pool:
            self.pool.closeall()
