# pyrefly: ignore [missing-import]
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from groq import Groq
import uvicorn

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="LLM Random Joke API",
    description="FastAPI service that generates random jokes using Groq LLM.",
    version="1.0.0",
)


class JokeResponse(BaseModel):
    joke: str
    topic: Optional[str] = None


def generate_joke_with_groq(topic: Optional[str] = None) -> str:
    """Calls Groq API to generate a joke (random or on a given topic)."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Please configure it in your .env file.")

    model_name = os.getenv("GROQ_MODEL")
    if not model_name:
        raise ValueError("GROQ_MODEL is not set. Please configure it in your .env file.")

    user_prompt = f"Tell me a joke about {topic}." if topic else "Tell me a random joke."

    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a witty comedian. Tell a short, funny, and clean joke. "
                    "Return only the joke without any preamble, explanation, or quotes."
                ),
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        model=model_name,
    )
    joke_content = chat_completion.choices[0].message.content
    return joke_content.strip() if joke_content else "No joke generated."


@app.get("/joke", response_model=JokeResponse, summary="Get a random joke from LLM")
def get_random_joke():
    """Endpoint to get a freshly generated random joke via Groq."""
    try:
        joke_text = generate_joke_with_groq()
        return JokeResponse(joke=joke_text, topic="random")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate joke: {str(e)}")


@app.get("/joke/topic", response_model=JokeResponse, summary="Get a joke for a specific topic from LLM")
def get_joke_by_topic(
    topic: str = Query(..., min_length=1, description="The topic to generate a joke about")
):
    """Endpoint to generate a joke for a user-specified topic via Groq."""
    try:
        joke_text = generate_joke_with_groq(topic=topic)
        return JokeResponse(joke=joke_text, topic=topic)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate joke: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("2_fast_ai_llm:app", host="127.0.0.1", port=8000, reload=True)
