#! /usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    pass


@app.route('/files/<filename>')
def file(filename):
    pass

if __name__ == '__main__':
    app.run()

