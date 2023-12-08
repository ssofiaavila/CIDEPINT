from flask import jsonify, render_template
from flask import Blueprint
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from flask_cors import cross_origin
from src.core.model.auth import confirmation_registration, find_user_by_email
from src.web.helpers.auth import generate_confirmation_token, send_confirmation_email, verify_confirmation_token
from src.core.model import auth
from functools import wraps
from src.web.helpers.validations import only_numbers, is_valid_email, is_valid_name, validate_maintence, is_gmail_domain

from src.core.model.pagination import update_pagination
from src.core.model.maintence import Maintence

from src.core.database import db



home_bp = Blueprint("home", __name__, url_prefix="/")

def mantenimiento_required(f):
    """
    Verifica si el sistema está en modo de mantenimiento.
    Este decorador se utiliza para comprobar si el sistema está en modo de mantenimiento.
    Si la variable global 'maintence' está configurada en True, se muestra una página de mantenimiento
    y se devuelve un código de estado 503 (Servicio no disponible).
    De lo contrario, la función decorada se ejecuta normalmente.
    Args:
        f (function): La función que se va a decorar.
    Returns:
        function: La función decorada que verifica si el sistema está en modo de mantenimiento.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        maintence = Maintence.query.get(1)
        if maintence.estado:
            return render_template('home/maintence.html', maintence=maintence), 503
        return f(*args, **kwargs)
    return decorated_function


@home_bp.get("/")
@mantenimiento_required
def index():
    """
    Renderiza la página de inicio de la aplicación.
    Esta función maneja la solicitud de la página de inicio de la aplicación. Verifica si el sistema
    está en modo de mantenimiento antes de mostrar la página de inicio. Si el sistema está en modo
    de mantenimiento, se mostrará una página de mantenimiento y se devolverá un código de estado 503.
    Returns:
    """    
    return render_template("home/home.html")


@home_bp.get("/register")
@mantenimiento_required
def register():
    """
    Renderiza la página de registro de la aplicación.
    Esta función maneja la solicitud de la página de registro de la aplicación. La página de registro permite
    a los usuarios registrarse en la aplicación. Puedes habilitar un formulario de registro en este punto para
    recopilar la información necesaria de los usuarios.
    Returns:
        Response: La página de registro donde los usuarios pueden registrarse.
    """
    
    return render_template("home/register.html")

@home_bp.post("/registration")
@mantenimiento_required
def registration():
    """
    Maneja el proceso de registro de usuarios.
    Esta función maneja la solicitud de registro de un nuevo usuario en la aplicación. Verifica si el correo electrónico y el nombre de usuario ya existen en la base de datos. Si el correo electrónico o el nombre de usuario ya existen, muestra un mensaje de error y redirige al usuario de vuelta a la página de registro.
    Si el correo electrónico y el nombre de usuario son únicos, se genera un token de confirmación y se envía un correo electrónico al usuario con un enlace de confirmación. Luego, se registra al usuario en la base de datos y se muestra un mensaje informativo.
    Returns:
        Response: La página de inicio u otra página relevante después del proceso de registro.
    """
    params = request.form
    errors = []
    # Si encuentra un email igual al ingresado, entonces da mensaje de error, redirecciona al registro de usuario y NO crea el usuario
    fallo = ""
    required_fields = ["name", "lastname", "username", "email"]
    for field in required_fields:
            if not request.form.get(field).strip():
                errors.append(f"El campo {field} no puede ser un blanco.")
            elif not request.form.get(field):
                errors.append(f"El campo {field} es obligatorio.")

    if auth.find_user_by_email(params["email"]) :
        fallo = "email"
    
    if auth.find_user_by_username(params["username"]):
        fallo = fallo + " username"

    if not is_valid_email(params['email']):
        errors.append('El E-MAIL ingresado es invalido.')
    
    if not is_valid_name(params['name']):
        errors.append('Nombre invalido')

    if not is_valid_name(params['lastname']):
        errors.append('Apellido invalido')


    if fallo != "":
        errors.append('Los campos | %s | ingresados ya se encuentran registrados' %fallo)
    if errors:
            for error in errors:
                flash(error,'error')
            return redirect(url_for('home.register'))

    token = generate_confirmation_token()
    send_confirmation_email(params["email"], token)
    user = auth.register_user(name=params["name"], lastname=params["lastname"], username=params["username"], email=params["email"])
    flash('Se ha enviado un email a %s , por favor para su primer acceso ingrese utilizando el link provisto en el correo electronico' %params['email'], "info")
    return redirect(url_for('home.index'))



@home_bp.route("/registro", methods=["POST"])
@mantenimiento_required
def registro():
    params = request.get_json()
    errors = []
    fallo = ""
    required_fields = ["name", "lastname", "username", "email"]
    for field in required_fields:
            if not params[field].strip():
                errors.append(f"El campo {field} no puede ser un blanco.")
            elif not params[field]:
                errors.append(f"El campo {field} es obligatorio.")

    if auth.find_user_by_email(params["email"]) :
        fallo = "email"
    
    if auth.find_user_by_username(params["username"]):
        fallo = fallo + " username"

    if not is_valid_email(params['email']):
        errors.append('El E-MAIL ingresado es invalido.')
    
    if not is_valid_name(params['name']):
        errors.append('Nombre invalido')

    if not is_valid_name(params['lastname']):
        errors.append('Apellido invalido')


    if fallo != "":
        errors.append('Los campos | %s | ingresados ya se encuentran registrados' %fallo)

    if errors:
        return jsonify({'success': False, 'errors': errors}), 400

    token = generate_confirmation_token()
    send_confirmation_email(params["email"], token)
    user = auth.register_user(name=params["name"], lastname=params["lastname"], username=params["username"], email=params["email"])

    response_data = {'success': True,
                     'message': f'Se ha enviado un email a {params["email"]}. Por favor, para su primer acceso, ingrese utilizando el enlace proporcionado en el correo electrónico.'}
    return jsonify(response_data)


@home_bp.get("/registerConGoogle")
@mantenimiento_required
def register_google():
    """
    Renderiza la página de registro de la aplicación.
    Esta función maneja la solicitud de la página de registro de la aplicación. La página de registro permite
    a los usuarios registrarse en la aplicación. Puedes habilitar un formulario de registro en este punto para
    recopilar la información necesaria de los usuarios.
    Returns:
        Response: La página de registro donde los usuarios pueden registrarse.
    """
    
    return render_template("home/register_google.html")

@home_bp.post("/registrationConGoogle")
@mantenimiento_required
def registration_con_google():
    """
    Maneja el proceso de registro de usuarios.
    Esta función maneja la solicitud de registro de un nuevo usuario en la aplicación. Verifica si el correo electrónico y el nombre de usuario ya existen en la base de datos. Si el correo electrónico o el nombre de usuario ya existen, muestra un mensaje de error y redirige al usuario de vuelta a la página de registro.
    Si el correo electrónico y el nombre de usuario son únicos, se genera un token de confirmación y se envía un correo electrónico al usuario con un enlace de confirmación. Luego, se registra al usuario en la base de datos y se muestra un mensaje informativo.
    Returns:
        Response: La página de inicio u otra página relevante después del proceso de registro.
    """
    params = request.form
    errors = []
    # Si encuentra un email igual al ingresado, entonces da mensaje de error, redirecciona al registro de usuario y NO crea el usuario
    fallo = ""
    required_fields = ["name", "lastname", "username", "email"]
    for field in required_fields:
            if not request.form.get(field).strip():
                errors.append(f"El campo {field} no puede ser un blanco.")
            elif not request.form.get(field):
                errors.append(f"El campo {field} es obligatorio.")

    if auth.find_user_by_email(params["email"]) :
        fallo = "email"
    
    if auth.find_user_by_username(params["username"]):
        fallo = fallo + " username"

    if not is_valid_email(params['email']):
        errors.append('El E-MAIL ingresado es invalido.')
    
    if not is_gmail_domain(params['email']):
        errors.append("El Email ingresado no pertenece al dominio @gmail.com ")
    
    if not is_valid_name(params['name']):
        errors.append('Nombre invalido')

    if not is_valid_name(params['lastname']):
        errors.append('Apellido invalido')


    if fallo != "":
        errors.append('Los campos | %s | ingresads ya se encuentran registrados' %fallo)
    if errors:
            for error in errors:
                flash(error,'error')
            return redirect(url_for('home.register'))

    user = auth.register_user(name=params["name"], lastname=params["lastname"], username=params["username"], email=params["email"], activo=True)
    flash('Se ha registrado en el sitio con el email %s , por favor para su acceso, ingrese utilizando sus credenciales de google' %params['email'], "info")
    return redirect(url_for('home.index'))
    

@home_bp.route('/confirmacion/<string:token>', methods=['GET', 'POST'])
@mantenimiento_required
def confirmation(token):
    """
    Procesa la confirmación de registro a través de un enlace de confirmación.
    Este método verifica el token proporcionado y procesa la confirmación de registro
    permitiendo a los usuarios configurar su nombre de usuario y contraseña.
    :param token: El token de confirmación proporcionado en el enlace.
    :type token: str
    :return: Si el token es válido, renderiza una página para que los usuarios completen
             su información de usuario. Si el registro se completa con éxito, redirige
             al usuario a la página de inicio de sesión. En caso de un token inválido, se
             muestra un mensaje indicando que el enlace de confirmación no es válido.
    :rtype: str
    """
    if verify_confirmation_token(token):
        if request.method == 'POST':
            email = request.form.get('email')
            contraseña = request.form.get('password')    
            user = confirmation_registration(email=email, password=contraseña)
            if user:
                flash('Usuario %s creado con éxito.' %user.name, 'success')
                return redirect(url_for('auth.login')) 
            else:
                flash('Verifique que el email ingresado sea correcto y coincida con el que se registro')         
        
        return render_template('home/confirmation.html', token=token)

        
    return 'Enlace de confirmación no válido'

@home_bp.route('/confirmacion/mantenimiento', methods=['GET','POST'])
def confirmation_maintence():
    """
    Habilita o deshabilita el modo de mantenimiento del sitio web.
    Este método permite habilitar o deshabilitar el modo de mantenimiento del sitio web.
    Cuando el modo de mantenimiento está habilitado, el sitio web puede mostrar una
    página de mantenimiento y restringir el acceso a usuarios no autorizados.
    :return: Si se envía una solicitud POST para habilitar el modo de mantenimiento, se
             pone el sitio en modo de mantenimiento, se muestra un mensaje de éxito y se
             redirige a la página de inicio. Si se envía una solicitud POST para deshabilitar
             el modo de mantenimiento, se desactiva el modo de mantenimiento y se muestra
             un mensaje de éxito. En caso de una solicitud GET, se muestra una página para
             habilitar o deshabilitar el modo de mantenimiento.
    :rtype: str
    """
    errors = []
    if request.method == 'POST':
        maintence = Maintence.query.get(1)
        if (request.form.get('enabled') == "True"):

            errors = validate_maintence(request)
            if errors:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('home.confirmation_maintence'))
            
            flash('Se puso el sitio en mantenimiento correctamente', 'success')
            maintence.estado = True
            maintence.message = request.form.get('message_info')
            maintence.contact = request.form.get('contact')
            db.session.commit()
            return redirect(url_for('home.index'))
        else:
            maintence.estado = False
            db.session.commit()
        flash('No se puso el sitio en mantenimiento', 'success')
        return redirect(url_for('home.index'))
    return render_template("home/confirm_maintence.html")

@home_bp.route('/configuracion/paginacion', methods=['GET','POST'])
def config_paginate():
    """
    Configura la paginación del sitio web.
    Este método permite configurar la cantidad de elementos que se mostrarán por página
    en el sitio web. Los usuarios pueden especificar la cantidad deseada a través de
    un formulario.
    :return: Si se envía una solicitud POST con una cantidad válida de elementos por
             página, se actualiza la configuración de paginación y se muestra un mensaje
             de éxito. Si se envía una solicitud POST con errores, se muestran los errores
             y se redirige de vuelta a la página de configuración. En caso de una solicitud
             GET, se muestra la página de configuración de paginación.
    :rtype: str
    """
    errors = []
    if request.method == 'POST':

        cant_elem = request.form.get('cant_pagination')

        if not only_numbers(cant_elem):
            errors.append(f"Se debe ingresar solo un numero")
        if not cant_elem.strip():
            errors.append(f"La cantidad de elementos por pagina no puede ser un blanco.")
        elif not cant_elem:
            errors.append(f"El campo cantidad de elementos es obligatorio.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('home.config_paginate', id=id))

        update_pagination(cant_elem)
        flash(f'Se puso {cant_elem} elementos por pagina exitosamente', 'success')
        return redirect(url_for('home.index'))
    return render_template("home/config_pagination.html")

