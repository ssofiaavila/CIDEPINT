import logging
import uuid
import datetime
from functools import wraps
from flask import session
from flask import abort
from flask import url_for
from flask_mail import Message
from src.core.model import auth
from src.core.model.auth import token as token_class
from src.core.model.combined_tables import list_permits_by_user_id, get_institutions_by_user_id
from src.web.email_config import mail

def is_authenticated(session):
    return session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args,**kwargs)
    
    return decorated_function


def has_permits(required_permits_list):
    has_permits = True 
    session_user = session.get("user")
    if (session_user):
        user = auth.find_user_by_id(session.get("user"))
        # print("Los permisos solicitados para acceder al recurso son: %s" %required_permits_list)
        
        user_permits = list_permits_by_user_id(user.id)
        # print("Los permisos del usuario son: %s " %user_permits)
        if (user_permits):
            for permit in required_permits_list:
                if not (permit in user_permits):
                    logging.warning("has_permission == NO EXISTE el permiso %s " %permit)
                    has_permits = False
                    break
            return has_permits
        else:
            logging.warning("has_permission == NO EXISTE NINGUN permiso " )
            return False
    else:
        return False

def generate_confirmation_token():
    token =  token_class.create_token(token=str(uuid.uuid4()))
    
    return token.token


def send_confirmation_email(correo, token_from_mail):
    msg = Message('Confirmación de Registro', sender='grupo19proyectosoftwareunlp@hotmail.com', recipients=[correo])
    msg.body = f'Por favor, haga clic en el siguiente enlace para confirmar su registro: {url_for("home.confirmation", token=token_from_mail , _external=True)}'
    mail.send(msg)
    

def verify_confirmation_token(token):
    token = token_class.find_unique_token(token)
    return token