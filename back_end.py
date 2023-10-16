from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, PasswordField,BooleanField,ValidationError, SubmitField, SelectField, MultipleFileField, FileField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, EqualTo, Length
import os
from datetime import datetime
import AI_train

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
    username= StringField("enter a username(you will login with this)",validators=[DataRequired()])
    password_hash = PasswordField("Insert password", validators=[DataRequired(),EqualTo('password_hash2',message='passwords must match')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username= StringField("museumName", validators=[DataRequired()])
    password= PasswordField("password", validators=[DataRequired()])
    submit= SubmitField("Submit")

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


def upload_painting(author, name, file, training):
    folder_path = imgdir + author
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    path = folder_path + "/"
    shown_name = author + ", " + name
    filename = author + ", " + name + ".jpg"
    AI_train.make_concept_list(author, name)
    add_training_files(author, training, name)
    # filename = secure_filename(file)
    file.save(os.path.join(path, filename))
    full_path = path + filename
    return full_path, shown_name


def delete_painting(author, paint):
    dir_path = imgdir + author
    paint_path = dir_path + "/" + paint
    if os.path.exists(paint_path):
        os.remove(paint_path)
    directory = os.listdir(dir_path)
    print(len(directory))
    if len(directory) == 0:
        os.rmdir(dir_path)
        t = training_dir + "/" + author
        remove_training_files(t)
        os.rmdir(t)
        print("directory", dir_path, "was removed")


def add_training_files(author, training, name):
    class_data_dir = training_dir + "/" + name
    os.makedirs(class_data_dir)
    train_img_path = training_dir + "/" + author
    if not os.path.exists(train_img_path):
        os.makedirs(train_img_path)
    elif len(os.listdir(train_img_path)) != 0:
        remove_training_files(train_img_path)
    for i in training:
        print("s", i)
        print("xx", i.filename)
        i.save(os.path.join(train_img_path, i.filename))


def remove_training_files(directory):
    filelist = [f for f in os.listdir(directory)]
    for f in filelist:
        os.remove(os.path.join(directory, f))
