FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry

RUN poetry install --no-dev

COPY ./my_project ./my_project

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "my_project.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
