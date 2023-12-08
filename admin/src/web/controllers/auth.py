import os
import pathlib
import requests
from flask import render_template
from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.web.helpers import auth as auth_helper
from src.core.model import auth
from src.core.model import  combined_tables
from src.core.model.institucion import get_institution_by_id
from src.web.controllers.home import mantenimiento_required

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


#Bypass for dev environment only
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


#Google
google_client_id = "1071048740950-62fih2va3m2o2r0jrbuhgm0gjka0e4je.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent.parent, "client_secret.json")
callback_uri= "https://admin-grupo19.proyecto2023.linti.unlp.edu.ar/auth/callback"
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=callback_uri
)

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/callback")
def callback_google_sign_in():
    flow.fetch_token(authorization_response=request.url)
    if not session['state'] == request.args["state"]:
        flash("El usuario no puso ser autenticado correctamente por medio de google","error")
        return redirect(url_for("home.index"))
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=google_client_id
    )

    user = auth.find_user_by_email(id_info.get("email"))
    
    if not user:
        session.clear()
        flash("El usuario no pudo ser autenticado correctamente por medio de google, ya que NO se encuentra registrado","error")
        return redirect(url_for("home.index"))
    
    user_login_validations_and_session_info(user)
    
    flash("La sesion se inicio correctamente con Google", "success")
    return redirect(url_for("home.index"))

@auth_blueprint.get("/login")
def login():
    """
    Renderiza la página de inicio de sesión.
    Esta función renderiza la página de inicio de sesión, permitiendo que los usuarios introduzcan sus credenciales
    para autenticarse en la aplicación.
    Returns:
        render_template: Una plantilla HTML para la página de inicio de sesión.
    Ejemplo:
        Al acceder a la URL "/login" en el navegador, se renderiza la página de inicio de sesión.
    """
    
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return render_template("home/login.html", authorization_url=authorization_url)


@auth_blueprint.post("/authenticate")
def authenticate():
    """
    Autentica al usuario y establece una sesión.
    Esta función toma los datos del formulario de inicio de sesión (correo electrónico y contraseña), 
    valida al usuario y, si las credenciales son correctas, establece una sesión de usuario. 
    También asigna instituciones y roles al usuario en la sesión.
    Returns:
        redirect: Redirige al usuario a la página de inicio si la autenticación es exitosa, 
        de lo contrario, muestra un mensaje de error y lo redirige nuevamente a la página de inicio de sesión.
    Ejemplo:
        Al enviar un formulario de inicio de sesión con credenciales válidas, el usuario se autentica y se redirige a la página de inicio.
    """
    params = request.form
    user = auth.validate_user(params["email"], params["password"])
    
    if not user:
        flash("Email incorrecto","error")
        return redirect(url_for("auth.login"))
    
    user_login_validations_and_session_info(user)
    flash("La sesion se inicio correctamente", "success")
    return redirect(url_for("home.index"))


@auth_blueprint.get("/logout")
def logout():
    """
    Cierra la sesión del usuario.
    Esta función verifica si hay una sesión de usuario activa y la cierra. 
    Luego, muestra un mensaje de confirmación y redirige al usuario a la página de inicio de sesión.
    Returns:
        redirect: Redirige al usuario a la página de inicio de sesión después de cerrar la sesión. 
        Muestra un mensaje de información si no hay sesión activa.    
    """
    if session.get("user") or session["google_id"]:
        session.clear()
        flash("La session se cerro correctamente","info")
    else:
        flash("No hay session inciada", "info")
        
    return redirect(url_for("auth.login"))


@auth_blueprint.get("/profile")
@auth_helper.login_required
@mantenimiento_required
def profile():
    """
    Muestra el perfil del usuario actual.
    Esta función permite a un usuario autenticado y con permisos de mantenimiento ver su perfil.
    Se valida si el usuario tiene los permisos adecuados para acceder a esta función.
    El perfil del usuario, incluida su información personal, se recupera de la base de datos y se muestra en una plantilla.
    Returns:
        render_template: Renderiza la plantilla de perfil del usuario, mostrando la información del usuario.
        Redirige al usuario a la página de inicio si no tiene los permisos adecuados para acceder.
    Ejemplo:
        Al acceder a esta ruta, un usuario autenticado con permisos de mantenimiento verá su perfil en una página web.
        Si el usuario no tiene los permisos necesarios, se mostrará un mensaje de error y se lo redirigirá a la página de inicio.
    """
    
    if not auth_helper.has_permits(["user_show"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    
    user_profile = auth.find_user_by_id(session.get("user"))
    return render_template("users/profile.html", user=user_profile)


def user_login_validations_and_session_info(user):
    if not user.activo:
        flash("El usuario se encuentra desactivado, contacte al administrador", "error")
        return redirect(url_for("auth.login"))
    
    session["user"] = user.id
    institutions = combined_tables.get_institutions_by_user_id(user.id)
    institution_defaut = get_institution_by_id(2)
    session["institutions"] =  institutions if len(institutions) > 0 else [institution_defaut]
    role_default = combined_tables.get_rol_by_id(2)
    user_role = combined_tables.get_user_rol(user.id)
    session["role"] = user_role.name if user_role else role_default.name
