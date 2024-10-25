from flask import Flask, Response
from flask_cors import CORS
from routes_mongo.refine_mongo_bp import refine_bp as refine_mongo_bp
from routes_posgres.refine_postgres_bp import refine_bp as refine_postgres_bp


def createFlask():
    app = Flask(__name__)
    
    # Allow CORS for your frontend URL
    CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})
    
    #app.register_blueprint(sample_bp, url_prefix='/')
    #app.register_blueprint(sample_bp2, url_prefix='/')
    app.register_blueprint(refine_mongo_bp, url_prefix='/mongo')
    app.register_blueprint(refine_postgres_bp, url_prefix='/postgres')
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    
    
    return app
    