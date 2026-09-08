import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Random Joke API",
    description="A simple FastAPI service to get random jokes from a predefined list.",
    version="1.0.0",
)

# Predefined list of jokes
JOKES: List[dict] = [
    {
        "id": 1,
        "setup": "Why do programmers prefer dark mode?",
        "punchline": "Because light attracts bugs!",
    },
    {
        "id": 2,
        "setup": "Why do Java developers wear glasses?",
        "punchline": "Because they don't C#!",
    },
    {
        "id": 3,
        "setup": "There are only 10 types of people in the world:",
        "punchline": "Those who understand binary and those who don't.",
    },
    {
        "id": 4,
        "setup": "A SQL query walks into a bar, walks up to two tables and asks...",
        "punchline": "Can I join you?",
    },
    {
        "id": 5,
        "setup": "How many programmers does it take to change a light bulb?",
        "punchline": "None. It's a hardware problem.",
    },
    {
        "id": 6,
        "setup": "Why was the JavaScript developer sad?",
        "punchline": "Because they didn't know how to 'null' their feelings.",
    },
    {
        "id": 7,
        "setup": "What's the best thing about a boolean?",
        "punchline": "Even if you are wrong, you are only off by a bit.",
    },
    {
        "id": 8,
        "setup": "Why did the developer go broke?",
        "punchline": "Because they used up all their cache.",
    },
]


class Joke(BaseModel):
    id: int
    setup: str
    punchline: str


@app.get("/", summary="Root endpoint")
def read_root():
    return {
        "message": "Welcome to the Joke API! Visit /docs for interactive documentation.",
        "endpoints": {
            "random_joke": "/joke",
            "all_jokes": "/jokes",
        },
    }


@app.get("/joke", response_model=Joke, summary="Get a random joke")
def get_random_joke():
    """Fetch and return a random joke from the list."""
    return random.choice(JOKES)


@app.get("/jokes", response_model=List[Joke], summary="Get all jokes")
def get_all_jokes():
    """Return all available jokes."""
    return JOKES


@app.get("/jokes/{joke_id}", response_model=Joke, summary="Get joke by ID")
def get_joke_by_id(joke_id: int = Path(..., ge=1, description="The ID of the joke to retrieve")):
    """Retrieve a specific joke by its ID."""
    for joke in JOKES:
        if joke["id"] == joke_id:
            return joke
    raise HTTPException(status_code=404, detail="Joke not found")


# if __name__ == "__main__":
#     uvicorn.run("1_fast_ai:app", host="127.0.0.1", port=8000, reload=True)