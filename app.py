from flask import Flask
from views import app
import os

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))
