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

#import AI as AI
# setup
app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'your secret key'
# add Db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
# init DB
db = SQLAlchemy(app)

# #GLOBAL VARIABLES
FOLDER_LIST = os.listdir('static/images')

TEST_LIST = os.listdir('static/images/Raffaello')
imgdir = 'static/images/'

AI_image = ''


##
# CLASSES
##
# db model temp class
"""

def start_AI(): #chiamato all'avvio
    os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
    AI.mpl.rcParams['figure.figsize'] = (12, 12)  # avvio
    AI.mpl.rcParams['axes.grid'] = False  # avvio
    hub_model = AI.hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def select_weight(author):# author servirà per selezionare il finetuning
    #una volta che l'utente ha selezionato l'opera, dato che poi avremmo più di un possibile autore
    weights_path = '/content/drive/MyDrive/finetuned_stable_diffusion.h5'  # dopo che l'utente ha selezionato l'opera
                                                                            # da cambiare, verrà preso tramite database
    #will be changed to the right path
    img_height = img_width = 512
    paintings_model = AI.keras_cv.models.StableDiffusion(
        img_width=img_width, img_height=img_height
    )  # definizione del modello, prende in input la dimensione dell'immagine, sono funzioni di keras, librerie da importare
    paintings_model.diffusion_model.load_weights(weights_path)  # carica il file .h5


def generate_image(user_prompt):
    AI.prompts=[user_prompt]
    for prompt in AI.prompts:
        generated_images = AI.paintings_model.text_to_image(
            prompt, batch_size=AI.images_to_generate, unconditional_guidance_scale=40
        )
        # questo for applica l'algoritmo di text to image, prendendo l'input(prompt), il n di immagini da generare, dimensioni. mette il risultato in outputs
        AI.outputs.update({prompt: generated_images})

    for prompt in AI.outputs:  # esegue la funzione sopra sull'array outputs
        AI.plot_images(AI.outputs[prompt])

def style_transfer(original, generated): # original e generated sono path
    content_path = generated
    style_path = original
    content_image = AI.load_img(content_path)
    style_image = AI.load_img(style_path)
    #generazione
    stylized_image = AI.hub_model(AI.tf.constant(content_image), AI.tf.constant(style_image))[0]
    # utilizza il modello caricato sopra, gli passa le 2 immagini e genera il risultato finale
    #fine generazione
    final_image = AI.tensor_to_image(stylized_image)
    final_image = final_image.save('finale.jpg')  # salva immagine come file, dovrò trovare il modo
                                                # per salvarle in un path unico, e nel database
                                                # probabilmente verrà fatto solo una volta che l'utente switcha pagina
                                                # almeno evito di salvare l'immagine mille volte

def commit_image(final_image):
    #verrà ulteriormente inserita in una tabella del database.
    final_image.save('path')
"""
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
                print(x)
                temp = dir + j
                painting = Painting_temp.query.filter_by(path=temp).first()
                if painting is None:
                    painting = Painting_temp(id=id, path=temp, aut=i, painting=x)
                    print("afafaf", painting)
                    db.session.add(painting)
                id += 1
    db.session.commit()

def fill_ft():
    db.session.commit()
class Painting_temp(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), primary_key=True)
    aut = db.Column(db.String(100), nullable=False)
    painting = db.Column(db.String(200), nullable=False)

    #finetuning=relationship("Finetuning", backref="authors")
    def __repr__(self):
        return "Painting_temp('path:%s', 'aut: %s','painting: %s'>" \
            % (self.path, self.aut, self.painting)


class Created_imgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    # base_pic = db.Column(db.String(255),
    # db.ForeignKey('Painting_temp.path'))
    votes = db.Column(db.Integer)

class Finetuning(db.Model):
    path = db.Column(db.String(255), primary_key=True)
    #author = db.Column(db.String(255), db.ForeignKey('Painting_temp.author'))
    author = db.Column(db.String(255), unique=True)
    def __repr__(self):
        return "Finetuned models('path:%s', 'author: %s'>" \
            % (self.path, self.author)

with app.app_context():
    db.drop_all()
    db.create_all()


# TO BE REMOVED

class Painting():
    p = {}
    for i in FOLDER_LIST:
        strip = i.rsplit('.', 1)[0]
        p[FOLDER_LIST.index(i)] = strip

    def as_list(self):
        return list(self.p.values())


##
# #ROUTES
##

@app.route("/", methods=["GET", "POST"])
def start():
    painting = None
    author = None
    fill()
    return render_template('start.html', selectedPainting=painting)


@app.route("/getPainting", methods=["GET", "POST"])
def getSelectedPainting():
    selectedpaint = request.get_json()
    print(type(selectedpaint))
    print('aaa', selectedpaint.values())
    print('aaa', selectedpaint['name'])
    session['name'] = selectedpaint['name']
    session['path'] = selectedpaint['path']
    author = Painting_temp.query.filter_by(painting=selectedpaint['name']).first()
    session['author'] = author.aut
    print("made by,", session.get('author'))
    response = make_response(jsonify('success'), 200)
    return response


@app.route("/game", methods=['GET', 'POST'])
def home():
    return render_template("index.html", paintingName=session.get('name'), path=session.get('path'))


@app.route("/vote", methods=['GET', 'POST'])
def vote():
    description = None
    return render_template("vote.html", path=session.get('path'), name=session.get('name'))


@app.route("/vote/votes", methods=['GET', 'POST'])
def increase_votes():
    return



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


@app.route("/result", methods=['POST', 'GET'])
def final():
    AI_image = session.get('AI_image', None)
    print('ass', AI_image)
    original_path = session.get('path', None)
    original_name = session.get('name', None)
    print("or", original_path)
    return render_template("final.html", original_path=original_path,
                           original_name=original_name, AI_image=AI_image)


@app.route("/test", methods=['POST', 'GET'])
def test():
    painting = None
    path = None
    name = None
    print(FOLDER_LIST)
    fill()
    for paint in db.session.query(Painting_temp).all():
        print(paint)

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


@app.route("/getAI", methods=['GET']) #assigns author style to the AI
def getAI():
    return
@app.route("/generate", methods=['POST', 'GET']) # AI creates pictures
# based on the style and prompt. and sends it back to front end
def generate():
    req = request.get_json() #receives the prompt
    print("req is", req)
    time.sleep(5) #to be removed
    painting = "https://placehold.co/512?text=AI+IMage&font=roboto"# temporary

    session['AI_image'] = painting#keeps the image in memory
    # for all the duration of the session
    print(painting)
    AI_image = painting
    response = jsonify(painting)# sends back generated image
    return response
