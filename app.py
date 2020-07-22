from flask import Flask, render_template, request, url_for
from models.counter import addVisitorRoot, viewVisitorRoot
import os

app = Flask(__name__)

@app.route("/")
def hello():
    addVisitorRoot()
    views = viewVisitorRoot()
    return "<h1 style='color:blue'>Hello There! Views: {0}</h1>".format(views)

if __name__ == "__main__":
    app.run(host='0.0.0.0')