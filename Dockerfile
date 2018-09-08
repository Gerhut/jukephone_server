FROM python:2.7

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

RUN pip install pipenv uwsgi

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock /usr/src/app/
RUN pipenv install --system --deploy

COPY . /usr/src/app

EXPOSE 3031

CMD ["uwsgi", "uwsgi.ini"]

STOPSIGNAL SIGQUIT
