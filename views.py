import os
import time

from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response,session
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, \
    validators, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

views = Blueprint(__name__, "views")
IMG_LIST = os.listdir('static/images')
imgdir = '/static/images/'
AI_image = ''

class Painting():
    p = {}
    for i in IMG_LIST:
        strip = i.rsplit('.', 1)[0]
        p[IMG_LIST.index(i)] = strip

    def as_list(self):
        return list(self.p.values())


# import requests module
import requests

# create a session object
s = requests.Session()


class SelectorForm(FlaskForm):
    paintings = Painting()
    choices = ['']
    choices = choices + paintings.as_list()
    print(choices)
    author = SelectField("Select the painting", choices=choices, validators=[DataRequired()])
    submit = SubmitField("Start Playing")


class PromptForm(FlaskForm):
    description = TextField("Describe what you remember", validators=[DataRequired()],
                            id="description", _name='description')
    submitbutton = SubmitField("Generate")


@views.route("/", methods=["GET", "POST"])
def start():
    selector = SelectorForm()
    author = None
    if request.method == 'POST' and selector.validate_on_submit():
        author = request.form.get('author')
        original = imgdir+author+'.jpg'
        print(original)
        session['original'] = original
        return redirect(url_for('views.home', author=author))
    return render_template('start.html', selector=selector)


@views.route("/game", methods=['GET', 'POST'])
def home():
    description = None
    form = PromptForm()
    author = request.args.get('author', None)
    if form.validate_on_submit():
        description = form.description.data
    return render_template("index.html", description=description, form=form, author=author)


@views.route("/generate", methods=['POST', 'GET'])
def generate():
    req = request.get_json()
    print(req)
    time.sleep(5)
    response = make_response(jsonify(req), 200)
    return response


@views.route("/final", methods=['POST', 'GET'])
def final():
    painting = session.get('AI_image', None)
    print('ass', painting)
    original = session.get('original', None)
    print(IMG_LIST[1])
    print("or", original)
    return render_template("final.html", images=IMG_LIST, original=original, painting=painting)

@views.route("/getAI",methods=['GET'])
def getAI():
    return
@views.route("/test", methods=['POST', 'GET'])
def test():
    return render_template("test.html")


@views.route("/json", methods=['POST', 'GET'])
def json():
    if request.is_json:
        req = request.get_json()
        response = {'message': 'JSON received'}
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"msg": 'no json received'}), 400)
        return res


@views.route("/test/entry", methods=['POST', 'GET'])
def entry():
    req = request.get_json()
    print(req)
    response = make_response(jsonify(req), 200)
    # res="./static/images/dwarf.jpg"
    return response


# access json from data
@views.route("/pictures", methods=['GET'])
def get_picture():
    painting = "https://placehold.co/300?text=AI+IMage&font=roboto"
    session['AI_image'] = painting
    print(painting)
    AI_image = painting
    return jsonify(painting)
