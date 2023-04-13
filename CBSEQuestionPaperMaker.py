import json

from flask import Flask, render_template

# load the project configuration from json file
with open("config.json", "r") as f:
    params = json.load(f)["params"]


app = Flask(__name__)


@app.route("/")
def home():
    """Home page route
    """
    return render_template("index.html", params=params)


if __name__ == "__main__":
    app.run(debug=True)
