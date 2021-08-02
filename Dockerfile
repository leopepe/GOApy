FROM python:3.8-slim as requirements

WORKDIR /

RUN pip3 install poetry==1.0.10
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt -o requirements.txt

FROM python:3.8-slim

# app structure
RUN mkdir -p /app/examples
WORKDIR /app

COPY --from=requirements /requirements.txt .
RUN pip3 install -r requirements.txt

COPY examples/*.py /app/

CMD ["python3", "cloud_builder.py"]