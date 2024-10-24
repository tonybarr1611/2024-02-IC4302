from flask import Flask, Response
from flask_cors import CORS
from routes_mongo import sample_bp
from routes_posgres import sample_bp as sample_bp2

def createFlask():
    app = Flask(__name__)
    
    # Allow CORS for your frontend URL
    CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})
    
    app.register_blueprint(sample_bp, url_prefix='/')
    app.register_blueprint(sample_bp2, url_prefix='/')
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    
    
    return app
    