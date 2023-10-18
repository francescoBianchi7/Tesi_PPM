import os
import time
from database import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session

from wtforms import Form, TextAreaField, \
    validators, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

import back_end as be
# import AI_train

# setup
import database
from database import app, db

base = "http://127.0.0.1:5000/"
# #GLOBAL VARIABLES
FOLDER_LIST = os.listdir('static/images')
created_images_dir = 'static/created_images/'
AI_image = ''


# db model temp class

with app.app_context():
    db.create_all()

"""avvio"""


# hub_model = AI.hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# print("AI started", hub_model)
# caricamente del modello per il style transfer, è già fatto e va scaricato

##
# #ROUTES
##
# def Ai_start():
# session["hub_model"] = AI.start_AI()
# print(session["hub_model"])

@app.route('/museum/add', methods=['GET', 'POST'])
def add_museum():
    museum = None
    username = None
    form = be.MuseumForm()
    if form.validate_on_submit():
        museum = database.Museums.query.filter_by(museum=form.museum.data).first()
        if museum is None:
            hashed_pw = database.generate_password_hash(form.password_hash.data, "sha256")
            museum = database.Museums(museum=form.museum.data, username=form.username.data, collection=None,
                                      password_hash=hashed_pw)
            db.session.add(museum)
            db.session.commit()
        form.museum.data = ''
        form.password_hash.data = ''
    flash("museum added successfully")
    our_museums = database.Museums.query.order_by(database.Museums.date_added)
    return render_template('add_museum.html', form=form, name=museum, username=username,
                           our_users=our_museums)

@app.route('/logout', methods=["GET", "POST"])
@database.login_required
def logout():
    database.logout_user()
    return redirect(url_for('start'))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = be.LoginForm()
    if form.validate_on_submit():
        museum = database.Museums.query.filter_by(username=form.username.data).first()
        if museum:
            #check hash
            if database.check_password_hash(museum.password_hash, form.password.data):
                database.login_user(museum)
                flash("login successfull")
                return redirect(url_for('back_end'))
            else:
                flash("Wrong password- Try Again!")
        else:
            flash("Username doesn't exist")
    return render_template('museum_login.html', form=form)


@app.route("/back_end", methods=["GET", "POST"])
@database.login_required
def back_end():
    museum = database.Museums.query.filter_by(username=database.current_user.username).first()
    museum_name=museum.museum
    print(museum_name)
    pic = None
    operation = None
    picForm = be.FT_Pictures()
    tempForm = be.temp_add_Pictures
    # Validate Form
    return render_template("back-end.html",
                   pic=pic, picForm=picForm, operation=operation, museum_name=museum_name)
@app.route("/add_painting", methods=["GET", "POST"])
@database.login_required
def add_painting():

    return render_template('add_painting.html')

@app.route("/upload-img", methods=["POST", "GET"])
def upload_img():
    print("called")
    print(request.data)
    author = request.form['author']
    name = request.form['name']
    file = request.files['file']
    training_files = request.files.getlist('training[]')
    print("files for trainig", training_files)
    for i in training_files:
        print("x", i)

    full_path, shown_name = be.upload_painting(author, name, file, training_files)
    print("full path is", full_path)
    db_add_new_painting(author, shown_name, full_path)
    response = make_response(jsonify(full_path), 200)
    time.sleep(5)
    return response


@app.route("/", methods=["GET", "POST"])
def start():
    painting = None
    author = None
    # change()
    # print(AI.torch.cuda.is_available())
    # print(AI.torch.version.cuda)
    # add_new_created_img(p.path)
    # fill()
    db.session.query(database.Painting_temp).delete()
    db.session.commit()

    return render_template('start.html', selectedPainting=painting)


@app.route("/getPainting", methods=["POST"])
def getSelectedPainting():
    selectedpaint = request.get_json()
    session['name'] = selectedpaint['name']
    session['path'] = selectedpaint['path']
    author = database.Painting_temp.query.filter_by(painting=selectedpaint['name']).first()
    # session['author'] = author.aut
    print(selectedpaint['name'])
    response = make_response(jsonify('success'), 200)
    return response


@app.route("/start_paints", methods=['POST', 'GET'])
def get_all():
    d = {}
    painting_dir = "./static/images"
    for sub_folder in os.listdir(painting_dir):
        print(sub_folder)
        sub_folder_dir = "./static/images/" + sub_folder
        for image in os.listdir(sub_folder_dir):
            d[image] = sub_folder_dir + "/" + image

    d["Durer, Hare"] = "/static/images/Durer/Durer, Hare.jpg"
    d["Botticelli, Birth of Venus"] = "/static/images/Botticelli/Botticelli,Birth of Venus.jpg"
    # for i in range(len(res2)):
    #   t = Painting_temp.query.filter_by(id=i).first()
    #  d[t.painting] = t.path
    print("end_d", d)
    response = jsonify(d)
    return response


@app.route("/game", methods=['GET', 'POST'])
def game():
    print('path', session.get('path'))
    # paint = Painting_temp.query.filter_by(painting=session.get('name')).first()
    # path = paint.path
    # print('path2', path)
    return render_template("index.html", paintingName=session.get('name'), path=session.get('path'))


@app.route("/postDescription", methods=['POST'])
def postDescription():
    req = request.get_json()
    print(req.get('message'))
    session['description'] = req.get('message')
    print(session.get('description', None))
    return jsonify('description posted successfully')


model = None


@app.route("/loading", methods=['GET', 'POST'])
def loading():
    return render_template('loading.html')


@app.route("/generate", methods=['POST', 'GET'])  # AI creates pictures
# based on the style and prompt. and sends it back to front end
def generate():
    prompt = session.get('description', None)
    print(prompt)
    user_prompt = prompt
    training_prompt = ""
    print(session.get('name'))
    print(session.get('path'))
    # original_p = Painting_temp.query.filter_by(painting=session.get('name')).first()

    print("final image", final)
    # same_paint = Created_Imgs.query.filter_by(original=original_p.path).all()
    # l = len(same_paint)+1
    painting_path = created_images_dir + "Botticelli, Venere1.jpg"
    session['AI_image'] = painting_path  # keeps the image in memory for all the duration of the session
    response="200" # sends back generated image
    return response


@app.route("/result", methods=['POST', 'GET'])
def final():
    AI_image = session.get('AI_image', None)
    print('ass', AI_image)
    # original_path = session.get('path', None)
    # original_name = session.get('name', None)
    # add_new_created_img(original_name, AI_image)
    res1 = database.Created_Imgs.query.with_entities(database.Created_Imgs.path).all()
    print("ada", res1)
    # print("or", original_path)
    return render_template("final.html", original_path="static/images/Botticelli/Botticelli,Birth of Venus.jpg",
                           original_name="botticelli, birth of venus", AI_image=AI_image)


@app.route("/userCollection")
def userCollection():
    AI_image = session.get('AI_image', None)
    return render_template('user-collection.html',
                           original_path="static/images/Botticelli/Botticelli,Birth of Venus.jpg",
                           AI_image=AI_image)


@app.route("/vote", methods=['GET', 'POST'])
def vote():
    description = None
    created_AI = session.get('AI_image', None)
    return render_template("vote.html", path=session.get('path'),
                           name=session.get('name'), AI_image=created_AI)


@app.route("/get_created", methods=['GET'])
def get_similar_creation():
    print("xd", session.get('name', None))
    orig = database.Painting_temp.query.filter_by(painting=session.get('name')).first()
    print("ar", orig)
    res = database.Created_Imgs.query.filter_by(original=orig.path).all()
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
    path = str(entry.get('path'))
    path = path.removeprefix("http://127.0.0.1:5000/")
    path = path.replace('%20', ' ')
    print("proper", path)
    updated = database.Created_Imgs.query.filter_by(path=path).first()
    updated.votes = entry.get('votes')
    db.session.commit()
    response = entry.get("votes")
    return jsonify(response)


def add_new_created_img(original_name, AI_image):
    db.session.query(database.Created_Imgs)
    ori = database.Painting_temp.query.filter_by(painting=original_name).first()
    same_paint = database.Created_Imgs.query.filter_by(original=ori.path).all()
    print("sane", same_paint)
    l = len(same_paint)
    print("l", l)

    same_paint = database.Created_Imgs(id=l + 1, path=AI_image, original=ori.path, votes=0)
    print(same_paint)
    db.session.add(same_paint)
    print(database.Created_Imgs.query.filter_by(original=ori.path).all())
    print("length after", l)
    print(same_paint)
    print(type(same_paint))
    db.session.commit()


def db_add_new_painting(author, painting_name, path):
    paintings = db.session.query(database.Paintings)
    print("x", paintings)
    pt = db.session.query(database.Painting_temp)
    print(pt)
    r = database.Painting_temp.query.count()
    print(r)
    rows = database.Paintings.query.filter_by(aut=author).first()
    print("c", rows)
    if database.Paintings.query.filter_by(aut=author).first() is None:
        print("no entry for author")
        rows = 0
    else:
        rows = database.Paintings.query.filter_by(aut=author).count()
        print(rows)
    print(rows)

    new_painting_entry = database.Paintings(id=rows + 1, path=path, aut=author, painting=painting_name)
    print("new entry", new_painting_entry)
    db.session.add(new_painting_entry)


def fill_ft():
    db.session.commit()


def fill():
    db.session.query(database.Painting_temp).delete()
    db.session.query(database.Finetuning).delete()
    db.session.commit()
    id = 0
    for i in FOLDER_LIST:
        print(i)
        dir = be.imgdir + i + "/"
        print("aaaaaaaaaa", dir)
        for j in os.listdir(dir):
            if j.endswith('.h5'):
                print(j)
                diffusion = database.Finetuning.query.filter_by(path=dir + j).first()
                if diffusion is None:
                    diffusion = database.Finetuning(path=dir + j, author=i)
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
                painting = database.Painting_temp.query.filter_by(path=temp).first()
                if painting is None:
                    painting = database.Painting_temp(id=id, path=temp, aut=i, painting=x)
                    print("afafaf", painting)
                    db.session.add(painting)
                id += 1
    db.session.commit()


@app.route("/authors", methods=['POST', 'GET'])
def get_all_authors():
    d = []
    for i in FOLDER_LIST:
        print(i)
        d.append(i)
    print(d)
    response = jsonify(d)
    return response


@app.route("/get_paints_by_author", methods=['POST', 'GET'])
def get_paintings_of_author():
    author = request.get_json()
    print(author)
    d = []
    author_paints = be.imgdir + str(author) + "/"
    for i in os.listdir(author_paints):
        d.append(i)
    print(d)
    response = jsonify(d)
    return response


@app.route("/remove_painting", methods=['POST', 'GET'])
def delete():
    entry = request.get_json()
    print(entry)
    be.delete_painting(entry.get("author"), entry.get("painted"))
    f = str(entry.get("painted")) + "was deleted"
    print(f)
    response = jsonify(f)
    return response
