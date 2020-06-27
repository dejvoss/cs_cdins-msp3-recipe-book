# Recipe App
# Flask application for website recipe book
import os
from flask import Flask


app = Flask (__name__)


@app.route('/')
def home():
    return "Welcome World"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

