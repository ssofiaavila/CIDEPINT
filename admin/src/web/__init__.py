from datetime import timedelta
import logging
from flask import Flask
from flask import render_template
from src.web import error
from src.web import blueprints
from src.web.config import config
from src.core import database
from src.core import bcrypt
from src.core import seeds
from src.core import session
from src.web.helpers import auth
from src.web import email_config
from flask_jwt_extended import JWTManager
from flask_cors import CORS


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
backend_root_url = "https://admin-grupo19.proyecto2023.linti.unlp.edu.ar"

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__,static_folder=static_folder)
    app.config['JWT_HEADER_TYPE'] = 'JWT'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    # configuracion basica
    app.config.from_object(config[env])
    
    # mail
    email_config.config_email(app)

    
    # errores
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    
    # extensiones
    session.init_app(app)
    bcrypt.init_app(app)
    database.init_app(app)
    blueprints.register_blueprints(app)   
    
    # jinja
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)

    # CORS configuración
    CORS(app)
    
     
    # Flask comandos
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        
    @app.cli.command(name="populatedb")
    def populatedb ():
        seeds.run()
    
   
    return app


