FROM python:3.12.3-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install "poetry==1.8.3" setuptools wheel

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-ansi 

COPY  . ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000