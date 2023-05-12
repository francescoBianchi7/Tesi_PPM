from flask import Flask
from views import views, redirect, url_for

from wtforms import StringField, SubmitField

app = Flask(__name__, static_url_path="/static")
app.register_blueprint(views, url_prefix="/views")
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def hello_world():
    return redirect(url_for('views.start'))


if __name__ == '__main__':
    app.run(debug=True)
