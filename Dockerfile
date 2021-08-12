FROM python:3.9-alpine
LABEL maintainer = 'Abdulrehman ajmal'

ENV PYTHONUNBUFFERED 1


COPY ./requirement.txt /requirement.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app/
RUN adduser -D user
USER user

