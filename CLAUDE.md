# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TalentStream AI** is a RAG-based talent acquisition system. The core workflow:
1. Upload employee profiles (free-text bio + optional metadata)
2. LLM extracts structured metadata: skills with per-skill experience years, total years of experience
3. Profiles are embedded and stored in Qdrant with metadata
4. Natural language queries are parsed into metadata filters + semantic embeddings for filtered vector search

## Commands

### Docker (recommended)
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
docker compose up --build
```

### Local Development
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt -r frontend/requirements.txt

# Start Qdrant only
docker compose up qdrant -d

# Backend (port 8000) — run from repo root or set PYTHONPATH
cd backend
QDRANT_HOST=localhost OPENAI_API_KEY=sk-... uvicorn main:app --reload --port 8000

# Frontend (port 8501, separate terminal)
cd frontend
API_URL=http://localhost:8000 streamlit run app.py
```

### Testing
```bash
# Must run from backend/ directory for import paths to work
cd backend
python -m pytest tests/ -v

# Single test file
python -m pytest tests/test_parse_employee_profile.py -v
```

Never run test files directly with `python3` — always use pytest.

## Architecture

### Services
- **`backend/app/services/llm_service/`** — LangChain + OpenAI integration
  - `clients.py` — Module-level singletons: `ChatOpenAI` (gpt-4o-mini) and `OpenAIEmbeddings` (text-embedding-ada-002)
  - `prompts.py` — Prompt templates for profile extraction and query parsing
  - `parse_employee_profile.py` — Async function; extracts skills + experience from bio via LLM structured output
  - `parse_query.py` — Async function; decomposes natural language queries into `ParsedQuery` with filters

- **`backend/app/services/qdrant_service/`** — Vector DB operations
  - `client.py` — Module-level `QdrantClient` singleton
  - `ensure_collection.py` — Creates "employees" collection (1536-dim, cosine) if missing
  - `upsert_employee.py` — Embeds profile text and stores with nested skill metadata
  - `search_employees.py` — Builds nested Qdrant filters (per-skill experience thresholds, department, grade, location, total years) then runs filtered vector search

### Schema (`backend/app/schemas.py`)
Key models: `ParseEmployeeProfilePayload` (input), `ParseEmployeeProfileAIMetadata` (LLM-extracted), `ParseEmployeeProfileAI` (complete parsed profile), `QueryRequest` / `ParsedQuery` (search), `SkillFilter` (per-skill filter with min/max years).

### API (`backend/app/api/v1/endpoints.py`)
- `POST /employees/upload` — Ingest, extract metadata, index
- `POST /query` — Natural language search with metadata filtering
- `GET /health`

### Frontend (`frontend/app.py`)
Streamlit app with two tabs: Upload (profile ingestion) and Search (query interface).

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | Required |
| `QDRANT_HOST` | `qdrant` | Qdrant hostname |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `API_URL` | `http://backend:8000` | Backend URL (frontend only) |

## Known Issues / To-Do

- LLM call errors are silently swallowed — should log meaningful errors
- `config.py` has redundant `os.getenv` calls; pydantic-settings should handle env vars directly
- Structured logging not yet implemented for LLM calls and Qdrant operations
