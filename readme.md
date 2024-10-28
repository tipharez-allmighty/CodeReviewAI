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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tipharez-allmighty/CodeReviewAI.git
   cd CodeReviewAI

2. **Ensure you have Poetry installed, then run:**:
   ```bash
   poetry install

3. **Run Redis (Docker):**:
   ```bash
   docker-compose up --build

4. **Run the application: You can start the FastAPI server using:**:
   ```bash
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Testing the Review Endpoint
To test the review endpoint, follow these steps:

Open your web browser and navigate to http://127.0.0.1:8000/docs.
Authorize your access by following the prompts.
Once authorized, you can test the /review endpoint using the following JSON payload:

    json

{
    "assignment_description": "A sample repo for testing",
    "github_repo_url": "https://github.com/sample/repo",
    "candidate_level": "Junior"
}

Send the request to receive the review results.

# Part 2: What if
To scale the Coding Assignment Auto-Review Tool prototype for handling 100+ new review requests per minute and large repositories with 100+ files, I would implement a microservices architecture with load balancing and asynchronous processing using a message queue (e.g., RabbitMQ or AWS SQS). This decouples incoming requests from processing, allowing for efficient handling of spikes in traffic. A NoSQL database (like MongoDB or DynamoDB) would provide the flexibility to manage dynamic repository structures, while caching layers (e.g., Redis) would improve performance by reducing database load.

For managing increased usage of the OpenAI and GitHub APIs, I would employ a rate limit backoff strategy that gradually increases wait times for requests when limits are approached. Additionally, implementing a Retrieval-Augmented Generation (RAG) approach would allow for efficient handling of data beyond the content window by retrieving relevant information before generating responses. Monitoring and logging would be essential for maintaining system reliability and diagnosing issues during high traffic, ensuring a robust and scalable architecture.
