FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install requests requests_oauthlib

ENTRYPOINT ["python", "${APP_HOME}/builder.py"]