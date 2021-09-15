FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv install

COPY ./start.sh .
RUN chmod +x ./start.sh

COPY ./app ./app

COPY ./alembic.ini .
COPY ./migrations ./migrations

CMD ["./start.sh"]
