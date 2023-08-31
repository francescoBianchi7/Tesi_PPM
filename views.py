import os
import time
from flask import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextAreaField, \
    validators, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from datetime import datetime
import back_end as be

import AI as AI
# setup
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'your secret key'
# add Db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
# init DB
db = SQLAlchemy(app)
base="http://127.0.0.1:5000/"
# #GLOBAL VARIABLES
FOLDER_LIST = os.listdir('static/images')

TEST_LIST = os.listdir('static/images/Leonardo da vinci')
imgdir = 'static/images/'
created_images_dir = 'static/created_images/'
AI_image = ''


##
# CLASSES
##
# db model temp class
def fill():
    db.session.query(Painting_temp).delete()
    db.session.query(Finetuning).delete()
    db.session.commit()
    id = 0
    for i in FOLDER_LIST:
        print(i)
        dir = imgdir + i + "/"
        print("aaaaaaaaaa", dir)
        for j in os.listdir(dir):
            if j.endswith('.h5'):
                print(j)
                diffusion = Finetuning.query.filter_by(path=dir+j).first()
                if diffusion is None:
                    diffusion = Finetuning(path=dir+j, author=i)
                    print("finetune", diffusion)
                    db.session.add(diffusion)
            else:
                if j.endswith('.jpg'):
                    x = j.replace('.jpg', '')
                    x = x.replace('_', ' ')
                elif j.endswith('.png'):
                    x = j.replace('.png', '')
                    x = x.replace('_', ' ')
                elif j.endswith('.jpeg'):
                    x = j.replace('.jpeg', '')
                    x = x.replace('_', ' ')
                print(x)
                temp = dir + j
                painting = Painting_temp.query.filter_by(path=temp).first()
                if painting is None:
                    painting = Painting_temp(id=id, path=temp, aut=i, painting=x)
                    print("afafaf", painting)
                    db.session.add(painting)
                id += 1
    db.session.commit()
"""
def change():
    p1 = Painting_temp.query.filter_by(painting='Leonardo da Vinci, Gioconda').first()
    c=Created_Imgs.query.filter_by(original=p1.path).all()
    print("gioconda",c)
    for entry in c:
        print("sda",entry)
        goal=created_images_dir+p1.painting+str(entry.id)+".jpg"
        print("changed to", goal)
        entry.path=goal
        print("after change", entry)
    p2 = Painting_temp.query.filter_by(painting='Leonardo da Vinci, Madonna of the Yarnwinder').first()
    c2=Created_Imgs.query.filter_by(original=p2.path).first()
    print("madonna", c2)
    c2.path = created_images_dir+p2.painting+str(1)+".jpg"
    c2.original = p2.path
    print("madonna2", c2)
    db.session.commit()
"""

"""avvio"""
hub_model = AI.hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
print("AI started", hub_model)
# caricamente del modello per il style transfer, è già fatto e va scaricato
def fill_ft():
    db.session.commit()

class Painting_temp(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), primary_key=True)
    aut = db.Column(db.String(100), nullable=False)
    painting = db.Column(db.String(200), nullable=False)

    #finetuning=db.Relationship("Finetuning", backref="authors")
    #created=db.relationship("created_imgs", backref='painting')
    def __repr__(self):
        return "Painting_temp('path:%s', 'aut: %s','painting: %s'>" \
            % (self.path, self.aut, self.painting)


class Created_Imgs(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), primary_key=True)
    original = db.Column(db.String(255), nullable=False)
    # base_pic = db.Column(db.String(255),
    #db.ForeignKey('Painting_temp.name'),)
    votes = db.Column(db.Integer)
    def __repr__(self):
        return "created models('path:%s','id:%s', 'original: %s'>" \
            % (self.path, self.id, self.original)

class Finetuning(db.Model):
    path = db.Column(db.String(255), primary_key=True)
    #author = db.Column(db.String(255), db.ForeignKey('Painting_temp.author'))
    author = db.Column(db.String(255), unique=True)
    def __repr__(self):
        return "Finetuned models('path:%s', 'author: %s'>" \
            % (self.path, self.author)

def add_new_created_img(original_name,AI_image):
    db.session.query(Created_Imgs)
    ori = Painting_temp.query.filter_by(painting=original_name).first()
    same_paint = Created_Imgs.query.filter_by(original=ori.path).all()
    print("sane", same_paint)
    l=len(same_paint)
    print("l", l)

    same_paint = Created_Imgs(id=l+1, path=AI_image, original=ori.path, votes=0)
    print(same_paint)
    db.session.add(same_paint)
    print(Created_Imgs.query.filter_by(original=ori.path).all())
    print("length after",l)
    print(same_paint)
    print(type(same_paint))
    db.session.commit()


with app.app_context():
    db.create_all()

##
# #ROUTES
##
def Ai_start():
    session["hub_model"] = AI.start_AI()
    print(session["hub_model"])

@app.route("/back_end", methods=["GET", "POST"])
def back_end():
    psw = None
    pic=None
    form = be.PswForm()
    picForm = be.FT_Pictures()
    #Validate Form
    if form.validate_on_submit():
        psw = form.psw.data
        form.psw.date = ''
    return render_template("back-end.html",
                           psw=psw,form=form, pic=pic, picForm=picForm)

@app.route("/", methods=["GET", "POST"])
def start():
    painting = None
    author = None
    #change()
    p=Painting_temp.query.filter_by(painting='Leonardo da Vinci, Gioconda').first()
    pc=Created_Imgs.query.all()
    mod=Created_Imgs.query.filter_by(path="static/created_images/Leonardo da Vinci, Gioconda3.jpg").first()
    print("pre",mod)

    print("created", pc)
    print(p)
    print(p.painting)
    #add_new_created_img(p.path)
    #fill()
    pa=Created_Imgs.query.filter_by(id=2).first()
    print("agaga", pa.path)
    return render_template('start.html', selectedPainting=painting,created=pa.path)


@app.route("/getPainting", methods=["POST"])
def getSelectedPainting():
    selectedpaint = request.get_json()
    session['name'] = selectedpaint['name']
    session['path'] = selectedpaint['path']
    author = Painting_temp.query.filter_by(painting=selectedpaint['name']).first()
    session['author'] = author.aut
    response = make_response(jsonify('success'), 200)
    return response


@app.route("/game", methods=['GET', 'POST'])
def home():
    print('path', session.get('path'))
    paint = Painting_temp.query.filter_by(painting=session.get('name')).first()
    path= paint.path
    print('path2', path)
    return render_template("index.html", paintingName=session.get('name'), path=session.get('path'))

@app.route("/getAI", methods=['GET']) #assigns author style to the AI
def getAI():
    return

model=None
@app.route("/generate", methods=['POST', 'GET']) # AI creates pictures
# based on the style and prompt. and sends it back to front end
def generate():
    req = request.get_json() #receives the prompt
    print("req is", req)
    prompt = req.get('message')
    print(prompt)
    global model
    if model is None:
        author = session.get("author", None)
        t = Finetuning.query.filter_by(author=author).first()
        model = AI.select_weight(t.path)
        print("author selected", t.author)
        print("finetune path", t.path)
    print('starting generation')
    path, output = AI.generate_image(prompt, model)
    print("created path is", path)
    print(session.get('name'))
    print(session.get('path'))
    original_p = Painting_temp.query.filter_by(painting=session.get('name')).first()
    final = AI.style_transfer(original_p.path, path, hub_model)
    print("final image", final)

    im = AI.PIL.Image.open("finale.jpg")
    same_paint = Created_Imgs.query.filter_by(original=original_p.path).all()
    path = AI.commit_image(final, created_images_dir, original_p.painting, len(same_paint)+1)
    l=len(same_paint)+1
    painting_path = created_images_dir+original_p.painting+str(l)+".jpg"
    session['AI_image'] = painting_path# keeps the image in memory for all the duration of the session
    print("created path is", path)

    response = jsonify(painting_path)# sends back generated image
    return response

@app.route("/result", methods=['POST', 'GET'])
def final():
    AI_image = session.get('AI_image', None)
    print('ass', AI_image)
    original_path = session.get('path', None)
    original_name = session.get('name', None)
    add_new_created_img(original_name, AI_image)
    res1 = Created_Imgs.query.with_entities(Created_Imgs.path).all()
    print("ada", res1)
    print("or", original_path)
    return render_template("final.html", original_path=original_path,
                           original_name=original_name, AI_image=AI_image)

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    description = None
    created_AI=session.get('AI_image', None)
    return render_template("vote.html", path=session.get('path'),
                           name=session.get('name'), AI_image=created_AI)

@app.route("/get_created", methods=['GET'])
def get_similar_creation():
    print("xd", session.get('name',None))
    orig=Painting_temp.query.filter_by(painting=session.get('name')).first()
    print("ar",orig)
    res = Created_Imgs.query.filter_by(original=orig.path).all()
    d = {}
    for entry in res:
        print(entry)
        d[entry.path] = entry.votes
    print("end_d", d)
    response = jsonify(d)
    return d




@app.route("/votes_update", methods=['GET', 'POST'])
def increase_votes():
    entry = request.get_json()
    print("updated", entry)
    print("ada", str(entry.get('path')))
    path=str(entry.get('path'))
    path=path.removeprefix("http://127.0.0.1:5000/")
    path=path.replace('%20', ' ')
    print("proper", path)
    updated = Created_Imgs.query.filter_by(path=path).first()
    updated.votes = entry.get('votes')
    db.session.commit()
    response = entry.get("votes")
    return jsonify(response)


@app.route("/start_paints", methods=['POST', 'GET'])
def get_all():
    res1 = Painting_temp.query.with_entities(Painting_temp.painting).all()
    print("ada", res1)
    res2 = Painting_temp.query.with_entities(Painting_temp.path).all()
    print("ada3", res2)
    d = {}
    for i in range(len(res2)):
        t = Painting_temp.query.filter_by(id=i).first()
        d[t.painting] = t.path
    print("end_d", d)
    response = jsonify(d)
    return response





@app.route("/test", methods=['POST', 'GET'])
def test():
    painting = None
    path = None
    name = None
    print(FOLDER_LIST)

    if request.method == ' POST':
        author = request.form.get('painting')
        print("aasas ", path)
        return redirect(url_for('home', author=author))

    our_paintings = Painting_temp.query.order_by(path)
    return render_template("test.html",
                           name=name, our_painting=our_paintings)


@app.route("/test/paint", methods=['POST', 'GET'])
def paint():
    aut = request.get_json()
    print("aut select", aut)
    temp = imgdir + aut
    print("list directory", temp)
    paint_list = []
    paint_list = paint_list + os.listdir(temp)
    print("list of paintings", paint_list)
    response = make_response(jsonify(paint_list), 200)
    return response


@app.route("/test/get_paint_db", methods=['POST', 'GET'])
def get_painting():
    ids = request.get_json()
    print(ids)
    print("xd", Painting_temp.query.with_entities(Painting_temp.painting, Painting_temp.path).all())
    painting = Painting_temp.query.filter_by(id=ids).first()
    print("aaa", painting)
    p = painting.path
    print(p)
    response = jsonify(p)
    return response


@app.route("/test/search_paint_db", methods=['POST', 'GET'])
def test_get_all():
    res1 = Painting_temp.query.with_entities(Painting_temp.painting).all()
    res2 = Painting_temp.query.with_entities(Painting_temp.path).all()
    res4 = []
    d = {}
    for i in range(len(res2)):
        t = Painting_temp.query.filter_by(id=i).first()
        res4.append(t.path)
        d[t.painting] = t.path
    print("aagagaga", res4)
    print("end_d", d)
    response = jsonify(d)
    return response