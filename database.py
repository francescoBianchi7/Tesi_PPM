from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__, static_url_path="/static")
CORS(app)
app.config['SECRET_KEY'] = 'your secret key'
#postgres://tesi_bianchi_user:aA5FNkIE6xmcCzO6c8wT8BWnt2t0ZxuS@dpg-ck4qm6l8ggls739oato0-a.frankfurt-postgres.render.com/tesi_bianchi
# add Db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tesi_bianchi_user:aA5FNkIE6xmcCzO6c8wT8BWnt2t0ZxuS@dpg-ck4qm6l8ggls739oato0-a.frankfurt-postgres.render.com/tesi_bianchi'

# init DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#FLASK LOGIN STUFF
login_manager=LoginManager()
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
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
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
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), primary_key=True)
    painting_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    collection = db.Column(db.Integer, db.ForeignKey('collection.id'))
    finetuning_path = db.Column(db.String(200))

    def __repr__(self):
        return "Painting('painting: %s', 'id: %i' 'description: %s','path:%s'>" \
            % (self.painting_name, self.id, self.description, self.path)


class Created_Imgs(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), primary_key=True)
    original = db.Column(db.String(255), nullable=False)

    votes = db.Column(db.Integer)

    def __repr__(self):
        return "created models('path:%s','id:%s', 'original: %s'>" \
            % (self.path, self.id, self.original)


