#!/usr/bin/python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/prakashjha/Desktop/nitish/scripting_project-master/dropbox.db'
db_path = os.path.join(os.path.dirname(__file__), 'dropbox.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    uId = db.Column('uid', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode, unique = True)
    passwd = db.Column('passwd', db.Unicode)
    name = db.Column('name', db.Unicode) 
    email = db.Column('email', db.Unicode) 
    phone = db.Column('phone', db.Unicode) 
    files = db.relationship('File', backref='owner')
    folders = db.relationship('Folder', backref='owner')

class File(db.Model):
    __tablename__ = 'file'
    fileId = db.Column('fileid', db.Integer, primary_key=True)
    fileName = db.Column('filename', db.Unicode)
    filePerm = db.Column('fpermission', db.Boolean)
    size = db.Column('size', db.Float)
    uId = db.Column('uid', db.Integer, db.ForeignKey('user.uid'))
    pFolderId = db.Column('p_folderid', db.Integer, db.ForeignKey('folder.folderid'))

class Folder(db.Model):
    __tablename__ = 'folder'
    folderId = db.Column('folderid', db.Integer, primary_key=True)
    folderName = db.Column('foldername', db.Unicode)
    uId = db.Column('uid', db.Integer, db.ForeignKey('user.uid'))
    pFolderId = db.Column('p_folderid', db.Integer, db.ForeignKey('folder.folderid'))
