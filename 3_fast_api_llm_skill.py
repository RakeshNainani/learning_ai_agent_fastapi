# pyrefly: ignore [missing-import]
import os
from pathlib import Path
import sys

# Ensure current directory is in sys.path for local module resolution
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import Groq
import uvicorn

from utils.models import AgentRequest, AgentResponse
from utils.skill_loader import Skill, discover_skills


load_dotenv()

app = FastAPI(
    title="Skill-Based AI Agent",
    version="1.0.0",
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

skills: dict[str, Skill] = discover_skills(BASE_DIR / "skills")


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Skill-based AI agent is running"
    }


@app.get("/skills")
def list_skills() -> list[dict[str, str]]:
    return [
        {
            "name": skill.name,
            "description": skill.description,
        }
        for skill in skills.values()
    ]


@app.post("/agent", response_model=AgentResponse)
def run_agent(request: AgentRequest) -> AgentResponse:
    skill = skills.get(request.skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{request.skill_name}' was not found",
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI agent executing a specialized skill.\n\n"
                f"Skill name: {skill.name}\n"
                f"Skill description: {skill.description}\n\n"
                f"{skill.instructions}"
            ),
        },
        {
            "role": "user",
            "content": request.message,
        },
    ]

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=messages,
    )

    content = completion.choices[0].message.content

    return AgentResponse(
        skill_used=skill.name,
        response=content or "",
    )


# if __name__ == "__main__":
#     uvicorn.run("3_fast_api_llm_skill:app", host="127.0.0.1", port=8000, reload=True)
