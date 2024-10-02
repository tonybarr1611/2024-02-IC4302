from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.friends import friends_bp
from routes.likes import likes_bp
from routes.posts import posts_bp
from routes.profile import profile_bp

def createFlask():
    app = Flask(__name__)
    
    # Allow CORS for your frontend URL
    CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(friends_bp, url_prefix='/')
    app.register_blueprint(likes_bp, url_prefix='/')
    app.register_blueprint(posts_bp, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')
    
    return app
    