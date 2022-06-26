FROM python:3.8

# ENVS
ENV DATABASE_PORT=5432
ENV DATABASE_HOST=database
ENV DATABASE_NAME=postgres
ENV DATABASE_USERNAME=postgres
ENV DATABASE_PASSWORD=postgres

ENV TZ Europe/Moscow

# VIRTUAL ENVIRONMENT
RUN mkdir /application
COPY pyproject.toml /application
COPY poetry.lock /application
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
WORKDIR /application
RUN poetry install --no-dev

# CODE
COPY /app /application/app
COPY main.py /application

EXPOSE 80

CMD ["python", "main.py"]