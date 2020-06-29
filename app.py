# Recipe App
# Flask application for website recipe book
import os
from flask import Flask, render_template


app = Flask (__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)

