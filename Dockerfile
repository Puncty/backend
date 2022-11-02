FROM python:3.10

WORKDIR /app

COPY ./src ./src
COPY ./api.py ./api.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD [ "gunicorn", "-w 4", "-b 127.0.0.1:3000", "api:app" ]
