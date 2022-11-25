FROM python:3.8.2-alpine

LABEL "repo"="https://https://github.com/sfunkernw/dew"

RUN apk --no-cache add iputils netcat-openbsd curl

WORKDIR /flask
COPY requirements.txt /flask/
RUN pip install -r requirements.txt
WORKDIR /dew
COPY app /dew
ENTRYPOINT ["python", "dew.py"]
EXPOSE 4000
