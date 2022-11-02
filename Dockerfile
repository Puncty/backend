FROM python:3.10

WORKDIR /app

COPY ./src ./src
COPY ./__main__.py ./__main__.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD [ "gunicorn", "-w 4", "-b 127.0.0.1:3000", "api:app" ]
