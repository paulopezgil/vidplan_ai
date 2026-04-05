# Backend Architecture

## Directory Structure

```text
backend/
├── core/           # Application config, security, and DB connection singletons
├── routers/        # API routing and endpoint definitions
│   ├── agent.py      # Endpoints for interacting with the Pydantic AI agent
│   └── database.py   # Endpoints for CRUD operations on standard DB entities and frontend tab data
├── services/       # Core business logic (LLM orchestration, DB operations)
├── models/         # Database ORM models (SQLAlchemy table structures)
├── schemas/        # Pydantic validation schemas (API requests/responses)
└── app.py
```

## Core Concept: Tab-to-Table Mapping

The backend database schema is designed to map explicitly 1:1 with the frontend UI tabs. 

Each tab in the frontend workspace corresponds directly to a database table. FastAPI exposes specific endpoints for each of these tables to allow the frontend to read and update the vertically stacked fields in each tab. 

Crucially, **these exact same update operations are exposed as function tools to the AI Agent**. This ensures that whether a user manually edits a text box in the UI, or the AI agent generates content in execution mode, both go through the exact same data lifecycle.

The mapping is as follows:
1. **Project Tab** → `projects` table (updated via `PUT /projects/{id}`)
2. **Chat Tab** → `messages` table (updated implicitly via chat interaction)
3. **Script Tab** → `scripts` table (updated via `PUT /projects/{id}/script`)
4. **Social Network Tab** → `social_media_posts` table (updated via `PUT /projects/{id}/social-media`)

## Database Schema

### 1. Projects Table (`projects`)
Stores metadata about each project. Mapped to the **Project Tab**.

| Column      | Type        | Description |
|-------------|-------------|-------------|
| id          | UUID (PK)   | Unique project identifier |
| title       | TEXT        | Project title |
| description | TEXT        | Project description |
| created_at  | TIMESTAMPTZ | Timestamp of creation |
| updated_at  | TIMESTAMPTZ | Timestamp of last update |

### 2. Messages Table (`messages`)
Stores chat history for the AI agent per project. Mapped to the **Chat Tab**.

| Column      | Type        | Description |
|-------------|-------------|-------------|
| id          | UUID (PK)   | Unique message identifier |
| project_id  | UUID (FK)   | Links to project |
| role        | TEXT        | `user` or `assistant` |
| content     | TEXT        | Message text |
| created_at  | TIMESTAMPTZ | Timestamp of message |

### 3. Scripts Table (`scripts`)
Stores the generated video scripts. Mapped to the **Script Tab**.

| Column      | Type        | Description |
|-------------|-------------|-------------|
| id          | UUID (PK)   | Unique script identifier |
| project_id  | UUID (FK)   | Links to project (One-to-One or One-to-Many) |
| content     | TEXT        | The script content / sections |
| created_at  | TIMESTAMPTZ | Timestamp of creation |
| updated_at  | TIMESTAMPTZ | Timestamp of last update |

### 4. Social Media Posts Table (`social_media_posts`)
Stores generated captions, descriptions, and hashtags. Mapped to the **Social Network Tab**.

| Column      | Type        | Description |
|-------------|-------------|-------------|
| id          | UUID (PK)   | Unique post identifier |
| project_id  | UUID (FK)   | Links to project (One-to-One or One-to-Many) |
| content     | TEXT        | The social media caption/hashtags |
| created_at  | TIMESTAMPTZ | Timestamp of creation |
| updated_at  | TIMESTAMPTZ | Timestamp of last update |

## AI Agent

- Implemented using **Pydantic AI**.
- Enforces structured interaction with two modes:
  - **Brainstorming mode**: Chat-only operations. Saves context to the `messages` table.
  - **Execution mode**: Writes data directly to the specific UI tabs/tables.
- The agent is provided explicit function tools that mirror the API endpoints:
  - `update_project_tab(project_id, title, description, tags)`
  - `update_script_tab(project_id, content)`
  - `update_social_media_tab(project_id, content)`
- Backend handles all database writes; the AI never accesses the DB directly.

## Backend Responsibilities

1. Expose explicit CRUD endpoints in `database.py` for the frontend to manually edit each tab.
2. Receive user messages from the frontend via the `agent.py` router.
3. Fetch relevant context for the LLM from the `messages`, `scripts`, and `social_media_posts` tables.
4. Call OpenAI API via Pydantic AI (handled in `services/`).
5. Parse AI response:
   - If intent = `brainstorming_mode` → append to `messages`.
   - If intent = `execution_mode` → invoke the specific tool (`update_script_tab`, etc.) to write to the designated table.
6. Return response to frontend (validated via schemas in `schemas/`).