import os
import json
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from prompts import code_review_prompt
from openai import OpenAI
from openai import OpenAIError
import redis

from github_api import GitHubAPI

load_dotenv()

rd = redis.Redis(host="localhost", port=6379, db=0)

app = FastAPI()

API_KEY = os.environ["API_KEY"]
API_KEY_NAME = os.environ["API_KEY_NAME"]
API_TOKEN_GITHUB = os.environ["API_TOKEN_GITHUB"]
OPENAI_KEY = os.environ["OPENAI_KEY"]

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


class Repository(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: Literal["Junior", "Middle", "Senior"]


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the provided API key against the stored key."""
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return api_key


@app.get("/test-auth")
async def test_auth(api_key: str = Depends(get_api_key)):
    """Test the API key authentication."""
    return {"api_key": api_key}


def generate_cache_key(repo: Repository) -> str:
    """Generate a unique cache key based on the repository's data."""
    return json.dumps(repo.model_dump(), sort_keys=True)


def get_openai_response(
    openai_key: str, repo_content: str, repo_files: str, candidate_level: str
) -> str:
    """Request a code review from OpenAI based on repository content and candidate level."""
    try:
        client = OpenAI(api_key=openai_key)
        review = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": code_review_prompt},
                {
                    "role": "user",
                    "content": f"Please review this code for the programmer level of {candidate_level}. Here are the repository files: {repo_content} and the files code: {repo_files}",
                },
            ],
        )

        review_result = review["choices"][0]["message"]["content"]
        return review_result

    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

    except KeyError:
        raise HTTPException(
            status_code=500, detail="Unexpected response format from OpenAI API."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/review")
async def review(repo: Repository, api_key: str = Depends(get_api_key)) -> JSONResponse:
    """Handle the code review request, checking cache and retrieving data from GitHub."""
    cache_key: str = generate_cache_key(repo)
    cached_result = rd.get(cache_key)

    if cached_result:
        return JSONResponse(content=json.loads(cached_result))

    repo_retriever = GitHubAPI(repo.github_repo_url, API_TOKEN_GITHUB)
    repo_content, repo_files = await repo_retriever.get_all_files()

    ai_response = get_openai_response(
        OPENAI_KEY, repo_content, repo_files, repo.candidate_level
    )

    review_result = {"message": ai_response, "repository": repo.model_dump()}

    rd.set(
        cache_key, json.dumps(review_result), ex=60
    )
    return JSONResponse(content=review_result)
