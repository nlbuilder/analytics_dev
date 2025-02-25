FROM python:3.11.5-alpine

#  install gcc and g++
RUN apk add --no-cache g++ gcc libffi-dev musl-dev

# install required packages from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt