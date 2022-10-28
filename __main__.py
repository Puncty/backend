from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.get("/")
def default() -> str:
    return "ok"


if __name__ == "__main__":
    app.run("localhost", "3000")
