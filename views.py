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
    museum = database.Museums.query.filter_by(username=database.current_user.username).first()
    museum_name = museum.museum
    return render_template("back-end.html", museum_name=museum_name)

@app.route("/back_end/add_painting", methods=["GET", "POST"])
@database.login_required
def add_painting():

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
        print(form.training_text)
        print(form.training_text.data)
        print(form.author)
        print(form.author.data)
        train_desc = form.training_text.data + "by" + form.author.data
        print("training description", train_desc)
        print("selected_collection", form.collection_select.data)
        form_col = database.Collection.query.filter_by(collection_name=form.collection_select.data).first()

        paintings = database.Paintings.query.filter_by(collection=form_col.id).all()
        '''TBD add check for already existing painting'''
        full_path, shown_name = be.upload_painting(form.collection_select.data, form.author, form.name, f)
        painting = database.Paintings(id=len(paintings), path=full_path, painting_name=shown_name,
                                      description=form.description.data, collection=form_col.id,
                                      finetuning_description=train_desc)
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

@app.route("/back_end/get_finetuning", methods=['POST', 'GET'])
def get_finetuning():

    """TBD if finetune is present return it's path, response will be {painting_path: finetune_path} also save it to db"""
    response={}

    return response
@app.route("/back_end/remove_painting", methods=['POST', 'GET'])
def delete_painting():
    entry = request.get_json()
    print(database.Collection.query.filter_by(collection_name=entry['collection']))
    sel_collection = database.Collection.query.filter_by(collection_name=entry['collection']).first()
    print('selected col', sel_collection)
    paints = database.Paintings.query.filter_by(collection=sel_collection.id, painting_name=entry['name']).first()
    print('all colle paints', paints)
    url_to_remove = paints.path
    print(url_to_remove)
    try:
        removed = be.delete_painting(url_to_remove, sel_collection.collection_path)
        if removed:
            db.session.remove(paints)
            db.session.commit()
            return redirect(url_for('back_end'))
    except:
        flash('painting not found')
    #print(database.Paintings.query.filter_by(path=url_to_remove).first())
    #be.delete_painting(entry.get("author"), entry.get("painted"))
    f = paints.path+"was deleted"
    #print(f)
    response = jsonify(f)
    return response


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
        print(p.finetuning_description)
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
    database.db_add_new_painting(author, shown_name, full_path)
    response = make_response(jsonify(full_path), 200)
    time.sleep(5)
    return response

@app.route("/",methods=['GET', 'POST'])
def init():
    a = be.generateUserId()
    session['User'] = a
    print(a)
    return redirect(url_for('start'))

@app.route("/start", methods=["GET", "POST"])
def start():
    painting = None
    author = None
    museum = database.Museums.query.order_by(database.Museums.id).first()


    createdimgs=database.Createdimgs.query.order_by(database.Createdimgs.path).all()
    for created in createdimgs:
        print("created",created)
    print('User already present', session['User'])
    return render_template('start.html', selectedPainting=painting, museum=museum.museum, Userid=session['User'])


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

    for colle in collection_dir:
        if os.listdir(colle.collection_path) is not None:
            for painting in os.listdir(colle.collection_path):
                sub_folder = colle.collection_path
                print("afaf",sub_folder)
                print(painting)
                p = database.Paintings.query.filter_by(path=colle.collection_path+"/"+painting).first()
                d[p.painting_name] = p.path


    print("end_d", d)
    response = jsonify(d)
    return response


@app.route("/game", methods=['GET', 'POST'])
def game():
    print('path', session.get('path'))
    print(session.get('name'))
    p= 'static/images/MyFirstCollection/Leonardo da Vinci, Gioconda.jpg'
    museum = database.Museums.query.order_by(database.Museums.id).first()
    print('\n \n gioconda')

    return render_template("index.html", paintingName=session.get('name'), path=session.get('path'),
                           museum=museum.museum,Userid=session['User'])


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
    orig = database.Paintings.query.filter_by(painting_name=session.get('name')).first()
    print(orig)
    created = database.Createdimgs.query.filter_by(original=orig.path).first()
    print(created)
    # orig_path = 'static/MyFirst/Collection'+orig_name+'.jpg'
    similarity = be.image_compare(orig.path, created.path)
    print(similarity)
    session['similarity'] = similarity
    """TBD add REST call"""
    # same_paint = Created_Imgs.query.filter_by(original=original_p.path).all()
    # l = len(same_paint)+1
    painting_path = created.path
    session['AI_image'] = painting_path  # keeps the image in memory for all the duration of the session
    print(session.get('AI_image'))
    response="200" # sends back generated image
    return response
@app.route("/get_similarity",methods=['GET'])
def get_similarity():

    simil=session.get('similarity',None)
    response=jsonify(simil)
    return response
@app.route("/compare_imgs",methods=['POST,GET'])
def compare():
    AI_image = session.get('AI_image', None)
    orig_name = session.get('name', None)
    orig=database.Paintings.query.filter_by(painting_name=orig_name).first()
    print(orig)
    created = database.Createdimgs.query.filter_by(original=orig.path).first()
    print(created)
    #orig_path = 'static/MyFirst/Collection'+orig_name+'.jpg'
    similarity = be.image_compare(orig.path,AI_image )
    response = jsonify(similarity)
    return response
@app.route("/result", methods=['POST', 'GET'])
def final():
    AI_image = session.get('AI_image', None)
    print('ass', AI_image)
    original_name = session.get('name', None)
    db_orig = database.Paintings.query.filter_by(painting_name=original_name).first()
    if db_orig:
        description = db_orig.description
    else:
        description = 'description not found'
    museum = database.Museums.query.order_by(database.Museums.id).first()
    return render_template("final.html", original_path=session.get('path',None),
                           original_name=original_name, AI_image=AI_image, museum=museum.museum,
                           description=description)



@app.route("/userCollection")
def userCollection():
    original= session.get('name')
    paint = database.Paintings.query.filter_by(painting_name=original).first()
    AI_image = session.get('AI_image', None)
    museum = database.Museums.query.order_by(database.Museums.id).first()
    return render_template('user-collection.html',
                           original_path=paint.path,
                           AI_image=AI_image, museum=museum.museum, Userid=session['User'])

@app.route("/userCollection/getUserImgs",methods=['GET','POST'])
def getuserImgs():
    dict = {}
    created = database.Createdimgs.query.filter_by(User='User#63664').all()
    for c in created:
    
        orig = database.Paintings.query.filter_by(path=c.original).first()

        v={'original_path': c.original, 'original_name':orig.painting_name, 'description':orig.description}
        print("adad", v)
        print(c.path)
        dict[c.path]=v

    print("adadadad", dict)
    print(dict.keys())
    response = jsonify(dict)
    return response


@app.route("/vote", methods=['GET', 'POST'])
def vote():
    description = None
    created_AI = session.get('AI_image', None)
    return render_template("vote.html", path=session.get('path'),
                           name=session.get('name'), AI_image=created_AI)


@app.route("/get_created", methods=['GET'])
def get_similar_creation():
    print("xd", session.get('name', None))
    #orig = database.Painting_temp.query.filter_by(painting=session.get('name')).first()
    #print("ar", orig)
    #res = database.Created_Imgs.query.filter_by(original=orig.path).all()
    #d = {}
    #for entry in res:
     #   print(entry)
     #   d[entry.path] = entry.votes
    # print("end_d", d)
    # response = jsonify(d)
    # return d


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





def fill_ft():
    db.session.commit()


def fill():
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

                id += 1
    db.session.commit()



