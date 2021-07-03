FROM python:3.9-slim-buster

WORKDIR /src

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip && pip install --no-cache-dir pipenv
COPY Pipfile* /src/
RUN pipenv install --system --deploy --ignore-pipfile

VOLUME /src
COPY src /src

CMD ./manage.py migrate && ./manage.py collectstatic --noinput