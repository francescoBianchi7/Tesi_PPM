from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, PasswordField,BooleanField,ValidationError, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, EqualTo, Length
import os
from datetime import datetime

imgdir = 'static/images/'

training_dir = 'content'
p = 'psw'


#FORMS
class PswForm(FlaskForm):
    select_op = SelectField("Select operation", choices=["Delete Painting", "Add Painting"])
    psw = StringField("insert psw", validators=[DataRequired()])
    submit = SubmitField("Submit")

class MuseumForm(FlaskForm):
    museum = StringField("insert museum name", validators=[DataRequired()])
    username = StringField("enter a username(you will login with this)",validators=[DataRequired()])
    password_hash = PasswordField("Insert password", validators=[DataRequired(),EqualTo('password_hash2',message='passwords must match')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField("museum username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddPicturesForm(FlaskForm):
    author = StringField("Insert author", validators=[DataRequired()])
    name = StringField("Insert name", validators=[DataRequired()])
    saved_pic = FileField("Picture that will be shown to users", validators=[DataRequired()])
    description = TextAreaField('Insert a brief description of the painting', validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddCollectionForm(FlaskForm):
    collection_name = StringField('Insert name of collection')
    submit = SubmitField('Submit')

def upload_painting(collection,author, name, file):
    folder_path = imgdir + collection
    print(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    path = folder_path + "/"
    print(path)
    shown_name = author.data+", "+name.data
    print(shown_name)
    filename = name.data + ".jpg"
    print(filename)
    file.data.save(os.path.join(path, filename))
    full_path = path + filename
    return full_path, shown_name


def delete_painting(author, paint):
    dir_path = imgdir + author
    paint_path = dir_path + "/" + paint
    if os.path.exists(paint_path):
        os.remove(paint_path)
    directory = os.listdir(dir_path)
    print(len(directory))

