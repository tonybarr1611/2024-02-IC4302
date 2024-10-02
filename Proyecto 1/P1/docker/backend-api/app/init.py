from flask import Flask, Response
from flask_cors import CORS
from routes.auth import auth_bp
from routes.friends import friends_bp
from routes.likes import likes_bp
from routes.posts import posts_bp
from routes.profile import profile_bp
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from metrics import max_processing_time, min_processing_time, avg_processing_time, total_requests

def createFlask():
    app = Flask(__name__)
    
    # Allow CORS for your frontend URL
    CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(friends_bp, url_prefix='/')
    app.register_blueprint(likes_bp, url_prefix='/')
    app.register_blueprint(posts_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
    return app
    