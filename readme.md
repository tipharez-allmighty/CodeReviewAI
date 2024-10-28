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


