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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
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
    collection = db.Column(db.String(200), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    #poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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
    image_path = db.Column(db.String(200), primary_key=True)
    image_name = db.Column(db.String(50),nullable=False)

    #museum = db.relationship('Museum', backref='museum')

class Painting_temp(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), primary_key=True)
    aut = db.Column(db.String(100), nullable=False)
    painting = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Painting_temp('path:%s', 'aut: %s','painting: %s'>" \
            % (self.path, self.aut, self.painting)


class Paintings(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), primary_key=True)
    painting = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Painting('painting: %s',, 'id: %i' 'aut: %s','path:%s'>" \
            % (self.painting, self.id, self.aut, self.path)


class Created_Imgs(db.Model):
    id = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(255), primary_key=True)
    original = db.Column(db.String(255), nullable=False)

    votes = db.Column(db.Integer)

    def __repr__(self):
        return "created models('path:%s','id:%s', 'original: %s'>" \
            % (self.path, self.id, self.original)


class Finetuning(db.Model):
    path = db.Column(db.String(255), primary_key=True)
    # author = db.Column(db.String(255), db.ForeignKey('Painting_temp.author'))
    author = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return "Finetuned models('path:%s', 'author: %s'>" \
            % (self.path, self.author)