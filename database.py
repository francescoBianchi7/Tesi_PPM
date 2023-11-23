from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#postgres://tesi_bianchi_user:aA5FNkIE6xmcCzO6c8wT8BWnt2t0ZxuS@dpg-ck4qm6l8ggls739oato0-a.frankfurt-postgres.render.com/tesi_bianchi
# add Db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'

app = Flask(__name__, static_url_path="/static")
CORS(app)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SESSION_PERMANENT'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tesi_bianchi_user:aA5FNkIE6xmcCzO6c8wT8BWnt2t0ZxuS@dpg-ck4qm6l8ggls739oato0-a.frankfurt-postgres.render.com/tesi_bianchi'
# init DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

@login_manager.user_loader
def load_museum(museum_id):
    return Museums.query.get(int(museum_id))

class Museums(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    museum = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), nullable=False,
                       unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    # Museum Can Have Many Collections
    collections = db.relationship('Collection', backref='collections')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<museum %r' %self.museum


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(200), nullable=False)
    museum = db.Column(db.String(20), db.ForeignKey('museums.username'))
    collection_path = db.Column(db.String(200), unique=True)
    # Collections Have Many Paintings
    paintings = db.relationship('Paintings', backref='paintings')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return "Collection('name: %s',, 'id: %i' 'museum: %s','collection_name:%s',>" \
            % (self.collection_name, self.id,self.museum, self.collection_path)


class Paintings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), primary_key=True)
    painting_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    collection = db.Column(db.Integer, db.ForeignKey('collection.id'))
    finetuning_path = db.Column(db.String(400))
    finetuning_description = db.Column(db.String(400), nullable=False)
    created_imgs = db.relationship('Createdimgs', backref='createdimgs')

    def __repr__(self):
        return "Painting('painting: %s', 'id: %i' 'description: %s','path:%s'>" \
            % (self.painting_name, self.id, self.description, self.path)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    #created = db.relationship('Created_Imgs', backref='created_imgs')


class Createdimgs(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), primary_key=True)
    original = db.Column(db.String(200), db.ForeignKey('paintings.path'))
    User = db.Column(db.String(255), nullable=False)
    votes = db.Column(db.Integer)

    def __repr__(self):
        return "created models('path:%s','id:%s', 'original: %s'>" \
            % (self.path, self.id, self.original)

def db_add_new_painting(author, painting_name, path):
    paintings = db.session.query(Paintings)
    print("x", paintings)
    pt = db.session.query(Paintings)
    print(pt)

    rows = Paintings.query.filter_by(aut=author).first()
    print("c", rows)
    if Paintings.query.filter_by(aut=author).first() is None:
        print("no entry for author")
        rows = 0
    else:
        rows = Paintings.query.filter_by(aut=author).count()
        print(rows)
    print(rows)

    new_painting_entry = Paintings(id=rows + 1, path=path, aut=author, painting=painting_name)
    print("new entry", new_painting_entry)
    db.session.add(new_painting_entry)
