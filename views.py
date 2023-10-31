import os
import time
from database import Flask
from flask import Blueprint, render_template, request, jsonify, redirect, \
    url_for, flash, make_response, session


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
    #db.drop_all()
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
@app.route("/test", methods=['GET', 'POST'])
def test():
    our_paints = database.Paintings.query.order_by(database.Museums.date_added)
    our_collection = database.Collection.query.order_by(database.Museums.date_added)
    our_museums = database.Museums.query.order_by(database.Museums.date_added)

    return render_template('test.html', our_users=our_museums, collections=our_collection, paints=our_paints,)

@app.route('/museum/add', methods=['GET', 'POST'])
def add_museum():
    museum = None
    username = None
    form = be.MuseumForm()
    if form.validate_on_submit():
        museum = database.Museums.query.filter_by(museum=form.museum.data).first()
        if museum is None:
            hashed_pw = database.generate_password_hash(form.password_hash.data, "sha256")
            museum = database.Museums(museum=form.museum.data, username=form.username.data,
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
                return redirect(url_for('back_end'))
            else:
                flash("Wrong password- Try Again!")
        else:
            flash("Username doesn't exist")
    return render_template('museum_login.html', form=form)


@app.route("/back_end", methods=["GET", "POST"])
@database.login_required
def back_end():
    print("adfa", database.current_user.username)
    print("adfaf", database.current_user.museum)
    museum = database.Museums.query.filter_by(username=database.current_user.username).first()
    museum_name = museum.museum
    print(museum_name)
    # Validate Form
    return render_template("back-end.html", museum_name=museum_name)

@app.route("/back_end/add_painting", methods=["GET", "POST"])
@database.login_required
def add_painting():
    active_collection = database.Collection.query.order_by(database.Collection.date_added).first()
    print(database.Paintings.query.order_by(database.Paintings.id).all())
    all_collections = database.Collection.query.order_by(database.Collection.date_added).all()
    col= {}
    col1=[]
    print("d", all_collections)
    for c in all_collections:
        col[c.id] = c.collection_name
        col1.append(c.collection_name)
    print("12", col)
    print(col1)
    form = be.AddPicturesForm()
    form.collection_select.choices = [(collect.collection_name, collect.collection_name) for collect in all_collections]
    print("choices", form.collection_select.choices)
    if form.validate_on_submit():
        f = form.saved_pic
        print("selected_collection", form.collection_select.data)
        form_col = database.Collection.query.filter_by(collection_name=form.collection_select.data).first()
        print(form_col)
        paintings = database.Paintings.query.filter_by(collection=form_col.id).all()
        '''TBD add check for already existing painting'''
        full_path, shown_name = be.upload_painting(form.collection_select.data, form.author, form.name, f)
        painting = database.Paintings(id=len(paintings), path=full_path, painting_name=shown_name,
                                      description=form.description.data, collection=form_col.id)
        db.session.add(painting)
        db.session.commit()
        return redirect(url_for('back_end'))
    return render_template('add_painting.html', form=form, all_col=col)



@app.route("/back_end/get_collections", methods=["GET"])
def get_collections():
    museum_collections = database.Collection.query.filter_by(museum=database.current_user.username).all()
    collection_names = []
    print(museum_collections[0].collection_name)
    for i in range(len(museum_collections)):
        print('xd', museum_collections[i].collection_name)
        collection_names.append(museum_collections[i].collection_name)
    response = jsonify(collection_names)
    return response


@app.route('/back_end/add_collection', methods=['GET', 'POST'])
@database.login_required
def add_collection():
    collection = None
    path = None
    museum = None
    form = be.AddCollectionForm()
    if form.validate_on_submit():
        print("ada", form.collection_name)
        print("ada", form.collection_name.data)
        collection_name = database.Collection.query.filter_by(collection_name=form.collection_name.data).first()
        print("asd", collection_name)
        if collection_name is None:
            path = be.imgdir+form.collection_name.data
            print("xd", path)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            collection = database.Collection(museum=database.current_user.username, collection_name=form.collection_name
                                             .data, collection_path=path,)
            db.session.add(collection)
            db.session.commit()
        else:
            flash("Collection already exist- Try Again!")
        form.collection_name.data = ''
    flash("collection added successfully")
    our_collection = database.Collection.query.order_by(database.Collection.date_added)
    return render_template('add_collection.html', form=form, name=collection,
                           our_users=our_collection)

@app.route("/back_end/delete_collection/<int:id>")
def delete_collection(id):
    collection = None
    path = None
    museum = None
    form = be.AddCollectionForm()
    our_collection = database.Collection.query.order_by(database.Collection.date_added)
    collection_to_delete = database.Collection.query.filter_by(id=id).first()

    try:
        empty = be.remove_collection(collection_to_delete.collection_path)
        if empty:
            db.session.delete(collection_to_delete)
            db.session.commit()
        return render_template('add_collection.html', form=form, name=collection,
                               our_users=our_collection)
    except:
        flash('there was a problem deleting the collection')
        return render_template('add_collection.html', form=form, name=collection,
                               our_users=our_collection)


@app.route("/back_end/get_paints_by_collection", methods=['POST', 'GET'])
def get_paintings_of_author():
    selected_collection = request.get_json()
    print(selected_collection)
    d = {}
    collection = database.Collection.query.filter_by(collection_name=selected_collection).first()
    print(collection)
    collection_paints = collection.collection_path + "/"
    print("test",collection_paints)
    paints = database.Paintings.query.filter_by(collection=collection.id).all()
    for i in os.listdir(collection_paints):
        p = database.Paintings.query.filter_by(path=collection_paints+i).first()
        print(p)
        v= { 'path':p.path, 'description':p.description}
        d[p.painting_name] = v
        print(d)
    response = jsonify(d)
    return response

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
    museum = database.Museums.query.order_by(database.Museums.id).first()
    # change()
    # print(AI.torch.cuda.is_available())
    # print(AI.torch.version.cuda)
    # add_new_created_img(p.path)
    # fill()

    return render_template('start.html', selectedPainting=painting, museum=museum.museum)


@app.route("/getPainting", methods=["POST"])
def getSelectedPainting():
    selectedpaint = request.get_json()
    session['name'] = selectedpaint['name']
    session['path'] = selectedpaint['path']
    author = database.Paintings.query.filter_by(painting_name=selectedpaint['name']).first()
    # session['author'] = author.aut
    print(selectedpaint['name'])
    response = make_response(jsonify('success'), 200)
    return response


@app.route("/start_paints", methods=['POST', 'GET'])
def get_all():
    d = {}
    painting_dir = "./static/images"
    collection_dir = database.Collection.query.order_by(database.Collection.id).all()

    for sub_folder in os.listdir(painting_dir):
        print(sub_folder)
        sub_folder_dir = "./static/images/" + sub_folder
        for image in os.listdir(sub_folder_dir):
            d[image] = sub_folder_dir + "/" + image
    for colle in collection_dir:
        if os.listdir(colle.collection_path) is not None:
            for painting in os.listdir(colle.collection_path):
                sub_folder = colle.collection_path
                print("afaf",sub_folder)
                print(painting)
                p = database.Paintings.query.filter_by(path=colle.collection_path+"/"+painting).first()
                d[p.painting_name] = p.path

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
    museum = database.Museums.query.order_by(database.Museums.id).first()
    # paint = Painting_temp.query.filter_by(painting=session.get('name')).first()
    # path = paint.path
    # print('path2', path)
    return render_template("index.html", paintingName=session.get('name'), path=session.get('path'),museum=museum.museum)


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
    #res1 = database.Created_Imgs.query.with_entities(database.Created_Imgs.path).all()
    museum = database.Museums.query.order_by(database.Museums.id).first()
    #print("ada", res1)
    # print("or", original_path)
    return render_template("final.html", original_path="static/images/Botticelli/Botticelli,Birth of Venus.jpg",
                           original_name="botticelli, birth of venus", AI_image=AI_image, museum=museum.museum)


@app.route("/userCollection")
def userCollection():
    AI_image = session.get('AI_image', None)
    museum = database.Museums.query.order_by(database.Museums.id).first()
    return render_template('user-collection.html',
                           original_path="static/images/Botticelli/Botticelli,Birth of Venus.jpg",
                           AI_image=AI_image,museum=museum.museum)


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



@app.route("/remove_painting", methods=['POST', 'GET'])
def delete():
    entry = request.get_json()
    print(entry)
    be.delete_painting(entry.get("author"), entry.get("painted"))
    f = str(entry.get("painted")) + "was deleted"
    print(f)
    response = jsonify(f)
    return response
