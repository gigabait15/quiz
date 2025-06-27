FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install psycopg2-binary && \
    pip install -r requirements.txt

CMD ["gunicorn", "QuizDRF.wsgi:application", "--bind", "0.0.0.0:8000"]
