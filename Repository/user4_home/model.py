#!/usr/bin/python3
from app import db


class User(db.Model):
    __tablename__ = 'user'
    uId = db.Column('uid', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode, unique = True)
    passwd = db.Column('passwd', db.Unicode)
    name = db.Column('name', db.Unicode) 
    email = db.Column('email', db.Unicode, unique=True) 
    phone = db.Column('phone', db.Unicode, unique=True) 
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
