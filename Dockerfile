FROM python:3.6.7-alpine
ADD . /code
WORKDIR /code
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip install -r requriments-dev.txt --no-cache
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]