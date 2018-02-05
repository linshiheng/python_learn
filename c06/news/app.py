#! /usr/bin/env python3
import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

files_path = '/home/shiyanlou/files'
#files_path = 'i:\\code\\python_learn\\c06\\files\\'


@app.route('/')
def index():
    
    files = []

    for (dirpath, dirnames, filenames) in os.walk(files_path):
        for filename in filenames:
            if filename[-4:] == 'json':
                files += [os.path.join(dirpath, filename)]

    file_list = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            filename = data['title']
            file_list.append(filename)

    return render_template('index.html', file_list=file_list)


@app.route('/files/<filename>')
def file(filename):
    file = files_path + '/'+filename + '.json'
    
    if os.path.exists(file):
        with open(file, 'r') as f:
            post = json.load(f)
        return render_template('file.html', post=post)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
