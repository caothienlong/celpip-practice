# Documentation

## Guides

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deploy to Render.com with PostgreSQL & OAuth |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, storage layer, data flow |
| [ADDING_TESTS.md](ADDING_TESTS.md) | Adding Reading test content |
| [ADDING_LISTENING_TESTS.md](ADDING_LISTENING_TESTS.md) | Adding Listening test content (PDF → JSON workflow) |
| [CONFIG_GUIDE.md](CONFIG_GUIDE.md) | Timer, UI settings, `config.json` options |
| [USER_DATA_STRUCTURE.md](USER_DATA_STRUCTURE.md) | PostgreSQL schema & file-based fallback |
| [VOCABULARY_NOTES.md](VOCABULARY_NOTES.md) | Vocabulary notes feature & API |

## Infrastructure

| Service | Purpose |
|---------|---------|
| **Render.com** | Web hosting (Python + gunicorn) & PostgreSQL |
| **Cloudinary** | Audio/video hosting for Listening tests (URL-only, no SDK) |
| **Google/Facebook OAuth** | User authentication |

## Quick Links

| I want to... | Read this |
|--------------|-----------|
| Deploy the app | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Add a new Reading test | [ADDING_TESTS.md](ADDING_TESTS.md) |
| Add a new Listening test | [ADDING_LISTENING_TESTS.md](ADDING_LISTENING_TESTS.md) |
| Change timer settings | [CONFIG_GUIDE.md](CONFIG_GUIDE.md) |
| Understand the storage layer | [USER_DATA_STRUCTURE.md](USER_DATA_STRUCTURE.md) |
| Understand system architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
