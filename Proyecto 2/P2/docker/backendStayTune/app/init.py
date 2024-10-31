from flask import Flask, Response
from flask_cors import CORS
from routes.transform import transform_bp as transform_bp
from routes.song import song_bp as song_bp
from routes.filters import filters_bp as filters_bp

def createFlask():
    app = Flask(__name__)
    
    # Allow CORS for your frontend URL
    CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})

    app.register_blueprint(transform_bp, url_prefix="/")
    app.register_blueprint(song_bp, url_prefix="/")
    app.register_blueprint(filters_bp, url_prefix="/")
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    return app
    