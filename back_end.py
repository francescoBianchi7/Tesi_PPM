from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, SubmitField, SelectField, MultipleFileField, FileField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
import os
from datetime import datetime

imgdir = 'static/images/'


class PswForm(FlaskForm):
    psw = StringField("insert psw", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FT_Pictures(FlaskForm):
    author = StringField("inserire autore", validators=[DataRequired()])
    nome = StringField("inserire nome", validators=[DataRequired()])
    saved_pic = FileField("Picture that will be shown to users", validators=[DataRequired()])
    class_prompt = StringField("inserire il class prompt dell'opera", validators=[DataRequired()])
    train_pics = MultipleFileField("Pictures to insert")


class temp_add_Pictures(FlaskForm):
    author = StringField("inserire autore", validators=[DataRequired()])
    nome = StringField("inserire nome", validators=[DataRequired()])
    saved_pic = FileField("Picture that will be shown to users", validators=[DataRequired()])
    submit = SubmitField("Submit")


def upload_painting(author, name, file):
    folder_path = imgdir + author
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    path = folder_path + "/"
    shown_name = author + ", " + name
    filename = author + ", " + name + ".jpg"
    # filename = secure_filename(file)
    file.save(os.path.join(path, filename))
    full_path = path + filename
    return full_path, shown_name


def delete_painting(author, paint):
    dir_path=imgdir+author
    paint_path = dir_path+"/"+paint
    if os.path.exists(paint_path):
        os.remove(paint_path)
    directory=os.listdir(dir_path)
    print(len(directory))
    if len(directory) == 0:
        os.rmdir(dir_path)
        print("directory", dir_path, "was removed")