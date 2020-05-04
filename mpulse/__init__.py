from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

test_config = None
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    file_path = os.path.abspath(os.getcwd())+"/mpulse.db"
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'+file_path,
        SCHEMA=os.path.join(os.path.dirname(__file__), 'schema.sql'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        JSON_SORT_KEYS=False
   )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # init database
    db.init_app(app)
 
    with app.app_context():
 
        # Create tables if they don't exist
        db.create_all()  
        
        # Include our api Routes for members
        from . import members
        # Register Blueprints
        app.register_blueprint(members.bp)

        return app

