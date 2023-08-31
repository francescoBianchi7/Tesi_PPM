from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, SubmitField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

from datetime import datetime

class PswForm(FlaskForm):
    psw = StringField("insert psw", validators=[DataRequired()])
    submit = SubmitField("Submit")

class FT_Pictures(FlaskForm):
    pic = FileField("Pictures to insert")