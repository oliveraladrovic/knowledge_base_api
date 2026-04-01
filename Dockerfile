FROM python:3.12-slim
WORKDIR /app
COPY poetry.lock pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
COPY src/knowledge_base_api ./knowledge_base_api
CMD ["uvicorn", "knowledge_base_api.main:app", "--host", "0.0.0.0", "--port", "8000"]