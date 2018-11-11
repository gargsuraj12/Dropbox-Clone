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
    __tablename__ = 'USER'
    uId = db.Column('UID', db.Integer, primary_key=True)
    username = db.Column('USERNAME', db.Unicode, unique = True)
    passwd = db.Column('PASSWD', db.Unicode)
    name = db.Column('NAME', db.Unicode) 
    email = db.Column('EMAIL', db.Unicode) 
    phone = db.Column('PHONE', db.Unicode) 
    files = db.relationship('File', backref='USER')
    folders = db.relationship('Folder', backref='USER')

class File(db.Model):
    __tablename__ = 'FILE'
    fileId = db.Column('FILEID', db.Integer, primary_key=True)
    fileName = db.Column('FILENAME', db.Unicode)
    filePerm = db.Column('FPERMISSION', db.Boolean)
    size = db.Column('SIZE', db.Float)
    uId = db.Column('UID', db.Integer, db.ForeignKey('USER.UID'))
    pFolderId = db.Column('P_FOLDERID', db.Integer, db.ForeignKey('FOLDER.FOLDERID'))

class Folder(db.Model):
    __tablename__ = 'FOLDER'
    folderId = db.Column('FOLDERID', db.Integer, primary_key=True)
    folderName = db.Column('FOLDERNAME', db.Unicode)
    uId = db.Column('UID', db.Integer, db.ForeignKey('USER.UID'))
    pFolderId = db.Column('P_FOLDERID', db.Integer, db.ForeignKey('FOLDER.FOLDERID'))
