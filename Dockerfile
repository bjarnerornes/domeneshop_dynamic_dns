# Use an official Python runtime as a parent image
FROM python:3.11-slim

COPY install-packages.sh .
RUN ./install-packages.sh

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /app
WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

WORKDIR /app/domeneshop_dynamic_dns/
# Run app.py when the container launches
CMD ["python", "run.py"]
