FROM python:3.10

WORKDIR /app

COPY ./src ./src
COPY ./api.py ./api.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD [ "gunicorn", "-b 0.0.0.0:8002", "api:app" ]

