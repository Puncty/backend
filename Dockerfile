FROM python:alpine3.10

WORKDIR /app

COPY ./src ./src
COPY ./api.py ./api.py
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

CMD [ "gunicorn", "-b 0.0.0.0:8002", "api:app" ]

