FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install requests requests_oauthlib
RUN apt-get update && apt-get install git -y

ENTRYPOINT ["python", "builder.py"]