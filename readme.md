# Code Review API

This FastAPI application provides a service to perform code reviews based on the content of GitHub repositories. It utilizes OpenAI's language model to analyze the code and provide feedback based on the candidate's programming level (Junior, Middle, Senior).

## Features

- API key authentication for secure access.
- Retrieves repository files from GitHub.
- Analyzes code quality and provides feedback using OpenAI's language model.
- Caches results in Redis for improved performance.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher (if running locally)
- Docker and Docker Compose installed (if using Docker)
- Redis server installed and running (if running locally)
- GitHub API token
- OpenAI API key

## Installation

Sure! Here’s your markdown edited for consistent styling and formatting:

markdown

# CodeReviewAI Setup Instructions

## Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tipharez-allmighty/CodeReviewAI.git
   cd CodeReviewAI

    Install dependencies: Ensure you have Poetry installed, then run:

    bash

poetry install

Set up environment variables: Create a .env file in the project root with the following content:

bash

echo -e "API_KEY=your_api_key\nAPI_KEY_NAME=your_api_key_name\nAPI_TOKEN_GITHUB=your_github_token\nOPENAI_KEY=your_openai_key" > .env

Replace your_api_key, your_api_key_name, your_github_token, and your_openai_key with your actual keys.

Run Redis (Docker):

bash

docker-compose up --build

Run the application: You can start the FastAPI server using:

bash

    poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    The application will be available at http://localhost:8000.

vbnet


This version maintains a consistent format throughout, making it easier to follow. Let me know if you need any further modifications! 😊


