FROM python:3.7

ADD . ./

RUN pip install -r requirements.txt

ENTRYPOINT gunicorn -b :8080 app:APP

