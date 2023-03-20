from flask import Flask
from views import views, redirect, url_for
app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

@app.route('/')
def hello_world():
    return redirect(url_for('views.home'))

if __name__ == '__main__':
    app.run()
