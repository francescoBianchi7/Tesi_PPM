from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, PasswordField, BooleanField, ValidationError, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, EqualTo, Length
import os
import numpy as np
from datetime import datetime
import torch
import open_clip

from sentence_transformers import util
from PIL import Image
import random
import cv2

from roboflow import Roboflow
from matplotlib import pyplot as plt


imgdir = "static/images/"
# FORMS
class PswForm(FlaskForm):
    select_op = SelectField("Select operation", choices=["Delete Painting", "Add Painting"])
    psw = StringField("insert psw", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MuseumForm(FlaskForm):
    museum = StringField("insert museum name", validators=[DataRequired()])
    username = StringField("enter a username(you will login with this)", validators=[DataRequired()])
    password_hash = PasswordField("Insert password", validators=[DataRequired(), EqualTo('password_hash2',
                                                                                         message='passwords must match')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField("museum username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddPicturesForm(FlaskForm):
    author = StringField("Insert author", validators=[DataRequired()])
    collection_select = SelectField('Select the Collection of the painting', validators=[DataRequired()])
    name = StringField("Insert name", validators=[DataRequired()])
    saved_pic = FileField("Picture that will be shown to users", validators=[DataRequired()])
    description = TextAreaField('Insert a description of the painting to show to the users',
                                validators=[DataRequired()])
    training_text = TextAreaField("Insert a description for training", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddCollectionForm(FlaskForm):
    collection_name = StringField('Insert name of collection')
    submit = SubmitField('Submit')


def upload_painting(collection, author, name, file):
    folder_path = imgdir + collection
    print(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    path = folder_path + "/"
    print(path)
    shown_name = author.data + ", " + name.data
    print(shown_name)
    filename = shown_name + ".jpg"
    print(filename)
    file.data.save(os.path.join(path, filename))
    full_path = path + filename
    return full_path, shown_name


def delete_painting(paint_path, dir_path):
    print("deleting", paint_path)
    if os.path.exists(paint_path):
        os.remove(paint_path)
        directory = os.listdir(dir_path)
        print(len(directory))
        return True
    else:
        return False

def remove_collection(path):
    if len(os.listdir(path)) == 0:
        print('dIREctory empty')
        os.rmdir(path)
        return True
    else:
        print('directory not empty')
        return False


def image_compare(orig, created):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16-plus-240', pretrained="laion400m_e32")
    model.to(device)
    score = generateScore(orig,created,preprocess, model, device)
    return score
def imageEncoder(img,preprocess,model,device):
    img1 = Image.fromarray(img).convert('RGB')
    img1 = preprocess(img1).unsqueeze(0).to(device)
    img1 = model.encode_image(img1)
    return img1

def generateScore(image1, image2,preprocess,model,device):
    test_img = cv2.imread(image1, cv2.IMREAD_UNCHANGED)
    data_img = cv2.imread(image2, cv2.IMREAD_UNCHANGED)
    img1 = imageEncoder(test_img,preprocess,model,device)
    img2 = imageEncoder(data_img,preprocess,model,device)
    cos_scores = util.pytorch_cos_sim(img1, img2)
    score = round(float(cos_scores[0][0]) * 100, 2)
    return score


def generateUserId():
    a = f'{random.randrange(1, 10 ** 5):05}'
    use= 'User#'+a
    return use