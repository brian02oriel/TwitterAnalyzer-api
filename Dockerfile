FROM python:3.6.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY main.py /usr/src/app
COPY Twitter /usr/src/app/Twitter

ARG FLASK_ENV=development
ARG FLASK_APP=main.py
ARG FLASK_DEBUG=1
ARG CONSUMER_KEY=ZkaLWawtOntqbTgtcPHlKrO1j
ARG CONSUMER_SECRET=vVzxBCkKRY3iNCASZnbxwAyXMgISI9doZmYS8M8DUcRl7wVZCh
ARG ACCESS_TOKEN=1017240891197657094-D5l0VSWNeRBIRamwNIsioY2JMuz8oJ
ARG ACCESS_SECRET=UXRPR0iwIlpw0QQFStvP4sNu40Gmu6C6OSwlFaO8dUjIU
ARG DEVELOPMENT_TWEETS_COUNT=1000

ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0", "--port=5000"]