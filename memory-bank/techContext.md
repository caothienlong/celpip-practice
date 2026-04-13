# Technology Context: CELPIP Practice Platform

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.9+ (3.11 on Render) |
| Web Framework | Flask | 3.0.0 |
| Templates | Jinja2 | (bundled with Flask) |
| Auth | Authlib | 1.3.0 |
| Session | Flask-Login | 0.6.3 |
| HTTP | Werkzeug | 3.0.0 |
| Database | PostgreSQL | via psycopg2-binary >=2.9.9 |
| WSGI Server | Gunicorn | 21.2.0 |
| Config | python-dotenv | 1.0.0 |
| HTTP Client | requests | 2.31.0 |
| Frontend | HTML5, CSS3, JS (ES6+) | No SPA framework |
| Media Hosting | Cloudinary | .m4a audio, .mp4 video |
| Deployment | Render.com | Blueprint via render.yaml |
| Mobile (planned) | Capacitor | Core + iOS (package-lock.json only) |

## Dependencies (requirements.txt)

```
Flask==3.0.0
authlib==1.3.0
flask-login==0.6.3
python-dotenv==1.0.0
requests==2.31.0
Werkzeug==3.0.0
gunicorn==21.2.0
psycopg2-binary>=2.9.9
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes (prod) | Flask session secret (auto-generated on Render) |
| `DATABASE_URL` | No | PostgreSQL connection string (falls back to file storage) |
| `GOOGLE_CLIENT_ID` | No | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | Google OAuth client secret |
| `FACEBOOK_CLIENT_ID` | No | Facebook OAuth app ID |
| `FACEBOOK_CLIENT_SECRET` | No | Facebook OAuth app secret |
| `APP_URL` | No | Public URL for OAuth redirects |
| `REDIRECT_URI_BASE` | No | Base URL for OAuth callbacks |
| `ENABLE_PASSWORD_AUTH` | No | Enable email/password login |
| `CLOUDINARY_CLOUD_NAME` | No | For upload scripts only (app uses public URLs) |
| `CLOUDINARY_API_KEY` | No | For upload scripts only |
| `CLOUDINARY_API_SECRET` | No | For upload scripts only |

## Database Schema

```sql
users (email TEXT PK, name, provider, picture, role, created_at, last_accessed)
test_history (id SERIAL PK, user_email FK, test_num, data JSONB, updated_at, UNIQUE(user_email, test_num))
vocabulary_notes (note_id TEXT PK, user_email FK, test_num, skill, part_num, word, definition, context, created_at, updated_at)
```

Tables auto-created on first startup — no manual migrations.

## Development Setup

```bash
git clone https://github.com/caothienlong/celpip-practice.git
cd celpip-practice
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py  # http://127.0.0.1:5000
```

Local dev uses JSON file storage (no database needed).

## Production Deployment (Render.com)

- `render.yaml` Blueprint provisions web service + PostgreSQL automatically
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Health check: `GET /`
- Free tier: spins down after 15 min inactivity (~30s cold start)
- Database: free tier expires after 90 days

## Testing

- **No automated test suite** in the repository
- Manual QA documented in `TEST_STATUS.md`
- JSON validation: `python -m json.tool data/test_X/skill/partY.json`
- No CI/CD pipeline configured

## Key Files for Development

| File | What to Know |
|------|-------------|
| `app.py` | All routes — this is the main application (~single large file) |
| `config.json` | Timer settings, UI config, test metadata |
| `utils/data_loader.py` | How test data is loaded and processed |
| `utils/storage/interfaces.py` | Repository contracts — read before modifying storage |
| `utils/results_tracker.py` | The public API for all user data operations |
| `utils/database.py` | PostgreSQL schema and queries |
| `templates/listening_section.html` | Complex JS state machine for listening |
