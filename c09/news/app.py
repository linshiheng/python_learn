#! /usr/bin/env python3
import os
import json
from flask import Flask, render_template, abort,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from pymongo import MongoClient

app = Flask(__name__)
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/mydb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',backref=db.backref('file', lazy='dynamic'))
    content = db.Column(db.Text)
    
    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title

    def add_tag(self, tag_name):
        mgdb = MongoClient('127.0.0.1',27017).news
        tag = {'file_title':self.title,'tag_name':tag_name}
        mgdb.tags.insert_one(tag)
        
    def remove_tag(self, tag_name):
        mgdb = MongoClient('127.0.0.1',27017).news
        mgdb.tags.delete_one({'file_title':self.title,'tag_name':tag_name})

    @property
    def tags(self):
        
        tags = []
        mgdb = MongoClient('127.0.0.1',27017).news
        
        for tag in mgdb.tags.find({'file_title':self.title}):
            
            tags.append(tag['tag_name'])
            
        
        return tags


@app.route('/')
def index():
    file_list = File.query.all()
    
    return render_template('index.html', file_list=file_list)


@app.route('/files/<file_id>')
def file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        tags = file.tags
        
        return render_template('file.html', file=file, tags=tags)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    manager.run()
