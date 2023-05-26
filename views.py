import os
import time
from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

# setup
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'your secret key'


#
# add Db
#
#app.config['SQALCHEMY_DATABASE_URI'] = "sqlite:///images.db"
# init DB
#db = SQLAlchemy(app)


# #GLOBAL VARIABLES
IMG_LIST = os.listdir('static/images')
FOLDER_LIST = os.listdir('static/test_images')
TEST_LIST = os.listdir('static/test_images/Michelangelo')
imgdir = '/static/images/'
test_imgdir = 'static/test_images/'
AI_image = ''


##
# CLASSES
##
# db model
#class User(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  name = db.Column(db.String(200), nullable=False, unique=True)
   # date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create String
    #def __repr__(self):
       # return '<Name %r>' %self.name


class Test_Paintings():
    authors = FOLDER_LIST
    p = {}
    for i in authors:
        temp = os.listdir(test_imgdir+i)
        p[i] = temp
    def print_self(self):
        for k,v in self.p.items():
            print("author:", k, "made:", v)

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


class SelectorFormV2(FlaskForm):
    paintings = Test_Paintings()
    a = ['']
    a = a + paintings.authors
    p = ['']
    print(a)
    print(paintings.p.items())
    author = SelectField("Select the author", choices=a, validators=[DataRequired()])
    paintings = SelectField("Select the paint", choices=paintings.p)
    submit = SubmitField("Start Playing")

    def selectPaint(self, choice):
        paint = self.paintings.p.get(choice)
        print("lil", paint)
        return paint






##
# #ROUTES
##

@app.route("/", methods=["GET", "POST"])
def start():
    selector = SelectorForm()
    author = None
    if request.method == 'POST' and selector.validate_on_submit():
        author = request.form.get('author')
        original = imgdir + author + '.jpg'
        print(original)
        session['original'] = original
        return redirect(url_for('home', author=author))
    return render_template('start.html', selector=selector)


@app.route("/game", methods=['GET', 'POST'])
def home():
    description = None
    author = request.args.get('author', None)

    return render_template("index.html", description=description, author=author)


@app.route("/generate", methods=['POST', 'GET'])
def generate():
    req = request.get_json()
    print(req)
    time.sleep(5)
    response = make_response(jsonify(req), 200)
    return response


@app.route("/final", methods=['POST', 'GET'])
def final():
    painting = session.get('AI_image', None)
    print('ass', painting)
    original = session.get('original', None)
    print(IMG_LIST[1])
    print("or", original)
    return render_template("final.html", images=IMG_LIST, original=original, painting=painting)


@app.route("/getAI", methods=['GET'])
def getAI():
    return


@app.route("/test", methods=['POST', 'GET'])
def test():
    test = SelectorFormV2()
    author = None
    p = None
    print(test.author.choices)
    if test.validate_on_submit():
        author = request.form.get('author')
        p = test.selectPaint(author)
    print("aasas ", p)
    return render_template("test.html", test=test, p=p)


@app.route("/json", methods=['POST', 'GET'])
def json():
    if request.is_json:
        req = request.get_json()
        response = {'message': 'JSON received'}
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"msg": 'no json received'}), 400)
        return res


@app.route("/test/entry", methods=['POST', 'GET'])
def entry():
    req = request.get_json()
    print(req)
    response = make_response(jsonify(req), 200)
    # res="./static/images/dwarf.jpg"
    return response


@app.route("/test/paint" ,methods=['POST', 'GET'])
def paint():
    return
# access json from data
@app.route("/pictures", methods=['GET'])
def get_picture():
    painting = "https://placehold.co/300?text=AI+IMage&font=roboto"
    session['AI_image'] = painting
    print(painting)
    AI_image = painting
    return jsonify(painting)
