# Chapter 1: FastAPI Joke Services & Skill-Based AI Agent

A comprehensive collection of **FastAPI** applications demonstrating API development from static responses to LLM integration and dynamic, skill-driven AI agents using **Groq**.

---

## Features

1. **Static Joke Service (`1_fast_ai.py`)**:
   - Random joke selection from a curated list.
   - List all available jokes.
   - Lookup joke by integer ID with 404 validation.

2. **LLM Joke Generator (`2_fast_ai_llm.py`)**:
   - Dynamic joke generation powered by Groq LLM.
   - Topic-based joke generation (`/joke/topic?topic=...`).
   - Configurable model and API key via `.env`.

3. **Skill-Based AI Agent (`3_fast_api_llm_skill.py`)**:
   - Dynamic discovery of specialized skills from the `skills/` directory.
   - Markdown + YAML frontmatter format (`SKILL.md`) for defining skills and instructions.
   - Endpoint to list available skills (`GET /skills`).
   - Dynamic prompt assembly and execution via agent endpoint (`POST /agent`).

---

## Project Structure

```text
chapter_1/
├── 1_fast_ai.py              # Static joke service
├── 2_fast_ai_llm.py          # LLM joke generator (random & topic)
├── 3_fast_api_llm_skill.py   # Skill-based AI agent service
├── models.py                 # Pydantic models (AgentRequest, AgentResponse)
├── skill_loader.py           # Skill discovery and YAML parser
├── skills/                   # Directory containing specialized skills
│   └── joke-writer/
│       └── SKILL.md          # Joke writer skill definition & instructions
├── pyproject.toml            # Project metadata & dependencies
├── README.md                 # Complete documentation
├── .env                      # Local environment configuration (ignored by git)
├── .env.example              # Template for environment variables
└── uv.lock                   # Dependency lockfile
```

---

## Prerequisites

- **Python**: `>= 3.12`
- **Package Manager**: [`uv`](https://docs.astral.sh/uv/) (recommended) or standard `pip`
- **Groq API Key**: Free key from [Groq Console](https://console.groq.com/keys) (required for LLM services)

---

## Installation & Setup

### 1. Open the Project Directory

```powershell
cd c:\Work\code_practise\chapter_1
```

### 2. Install Dependencies

#### Option A: Using `uv` (Recommended)

Sync all dependencies from `pyproject.toml`:

```powershell
uv sync
```

Or install explicitly:
```powershell
uv add fastapi uvicorn groq python-dotenv pyyaml
```

#### Option B: Using standard `venv` & `pip`

```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn groq python-dotenv pyyaml
```

---

## Environment Configuration

Create a `.env` file from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Ensure the following variables are configured in `.env`:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

> **Supported Models**: `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`, or `qwen/qwen3.6-27b`.

---

## Running the Applications

### 1. Static Joke API (`1_fast_ai.py`)

```powershell
uv run uvicorn 1_fast_ai:app --reload
```

### 2. LLM Joke API (`2_fast_ai_llm.py`)

```powershell
uv run uvicorn 2_fast_ai_llm:app --reload
```

### 3. Skill-Based AI Agent API (`3_fast_api_llm_skill.py`)

```powershell
uv run uvicorn 3_fast_api_llm_skill:app --reload
```

> **Note**: Always reference module names as `<module>:app` (e.g. `3_fast_api_llm_skill:app`). Do not use file paths like `.\3_fast_api_llm_skill.py:app`.

All servers run by default on:
- **Base URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints Reference

### 1. Static Joke Service (`1_fast_ai.py`)

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | API status and endpoint directory |
| `GET` | `/joke` | Returns a single random joke from static list |
| `GET` | `/jokes` | Returns all static jokes |
| `GET` | `/jokes/{joke_id}` | Returns a static joke by integer ID |

### 2. LLM Joke Service (`2_fast_ai_llm.py`)

| Method | Route | Description |
|---|---|---|
| `GET` | `/joke` | Generates a random joke via Groq LLM |
| `GET` | `/joke/topic?topic={topic}` | Generates a joke on a user-specified topic via Groq LLM |

### 3. Skill-Based AI Agent Service (`3_fast_api_llm_skill.py`)

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Service health status |
| `GET` | `/skills` | Lists all dynamically discovered skills |
| `POST` | `/agent` | Executes a specialized skill with user input |

---

## Example Requests & Responses

### 1. Get a Random Joke (`2_fast_ai_llm.py`)

**Request**:
```bash
curl http://127.0.0.1:8000/joke
```

**Response (`200 OK`)**:
```json
{
  "joke": "Why did the scarecrow win an award? Because he was outstanding in his field.",
  "topic": "random"
}
```

### 2. Get Joke by Topic (`2_fast_ai_llm.py`)

**Request**:
```bash
curl "http://127.0.0.1:8000/joke/topic?topic=pizza"
```

**Response (`200 OK`)**:
```json
{
  "joke": "Why did the pizza go to therapy? It needed to get its toppings straight!",
  "topic": "pizza"
}
```

### 3. List Discovered Skills (`3_fast_api_llm_skill.py`)

**Request**:
```bash
curl http://127.0.0.1:8000/skills
```

**Response (`200 OK`)**:
```json
[
  {
    "name": "joke-writer",
    "description": "Generates short, funny and clean jokes about a user-provided topic."
  }
]
```

### 4. Execute AI Agent Skill (`3_fast_api_llm_skill.py`)

**Request**:
```bash
curl -X POST http://127.0.0.1:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "joke-writer", "message": "python programming"}'
```

**Response (`200 OK`)**:
```json
{
  "skill_used": "joke-writer",
  "response": "Why do Python programmers wear glasses? Because they can't C."
}
```

---

## How Skills Work

Skills are defined as modular directories inside `skills/`. Each skill directory contains a `SKILL.md` file:

```markdown
---
name: joke-writer
description: Generates short, funny and clean jokes about a user-provided topic.
---

# Joke Writer

## Instructions
1. Generate exactly one joke.
2. Keep the joke family-friendly.
3. Keep the response under 60 words.
4. Use the topic provided by the user.
5. Return only the joke.
```

- [`skill_loader.py`](file:///c:/Work/code_practise/chapter_1/skill_loader.py) parses the YAML frontmatter (`name`, `description`) and extracts instructions.
- [`3_fast_api_llm_skill.py`](file:///c:/Work/code_practise/chapter_1/3_fast_api_llm_skill.py) injects these instructions into the LLM system prompt dynamically.
- To add a new capability, create a new subfolder in `skills/` with its own `SKILL.md`—no code changes required!

---

## Troubleshooting

### 1. `TypeError: the 'package' argument is required to perform a relative import`
- **Cause**: Passing file paths like `.\1_fast_ai.py:app` to Uvicorn.
- **Fix**: Use Python module syntax without `.\` or `.py` extension:
  ```powershell
  uv run uvicorn 3_fast_api_llm_skill:app --reload
  ```

### 2. `ModuleNotFoundError: No module named 'yaml'`
- **Cause**: PyYAML package is not installed.
- **Fix**: Run `uv add pyyaml` or `pip install pyyaml`.

### 3. Port `8000` is already in use
- Find and terminate lingering processes:
  ```powershell
  Get-NetTCPConnection -LocalPort 8000
  ```
- Or run your server on an alternative port:
  ```powershell
  uv run uvicorn 3_fast_api_llm_skill:app --reload --port 8080
  ```
