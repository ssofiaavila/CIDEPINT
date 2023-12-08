from src.core.model.auth.rol.role import Role
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.model.auth import list_users, getUserById, updateUser, deleteUsuario, usuariosFiltroMail, find_user_by_id, filtrar_usuarios_misma_institucion, filtrar_usuarios_por_estado
from src.web.helpers import auth
from flask import session, jsonify
from flask import flash, redirect, url_for
from src.core.model.auth import User
from src.web.controllers.home import mantenimiento_required
from src.core.model.combined_tables import get_user_rol, update_role, list_roles, delete_rol, get_institutions_by_user_id, institutions_and_roles_per_user, get_super_admin_ids
from src.core.model.institucion import list_institutions, get_institution_by_id
from flask_bcrypt import Bcrypt
from src.web.controllers.home import mantenimiento_required
from src.core import pagination
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from src.web.helpers.validations import institution_name
from flask_cors import cross_origin

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, JWTManager

bcrypt = Bcrypt()

from src.web.forms.forms import UserForm



users_bp = Blueprint("users", __name__, url_prefix="/users")

# Esta es tu lista negra de tokens. En una aplicación real, probablemente querrías almacenar esto en una base de datos.
blacklist = set()
jwt = JWTManager()

@users_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Cierra la sesión del usuario agregando su token a la lista negra.
    """
    jti = get_jwt()['jti']  # JTI es el identificador único del token
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """
    Verifica si un token está en la lista negra.
    """
    jti = jwt_payload['jti']
    return jti in blacklist

@auth.login_required
@users_bp.get('/')
@mantenimiento_required
def index():
    """
    Muestra una lista de usuarios y permite filtrarlos por dirección de correo electrónico.
    Este método se utiliza para mostrar una lista de usuarios en el sitio web. Los usuarios
    pueden filtrar la lista ingresando una dirección de correo electrónico en el campo de búsqueda.
    Si se especifica una dirección de correo electrónico, se mostrarán solo los usuarios cuyas
    direcciones coincidan con la consulta. Si no se proporciona un filtro de búsqueda, se mostrarán
    todos los usuarios (excepto el usuario con ID 1).
    :return: Si se proporciona un filtro de búsqueda y se encuentran usuarios que coincidan con
             la consulta, se muestra una lista paginada de usuarios que cumplen con el filtro. En caso
             de no proporcionar un filtro de búsqueda, se muestra una lista paginada de todos los usuarios
             (excepto el usuario con ID 1). Si el usuario no tiene permisos para acceder a esta función,
             se muestra un mensaje de error y se redirige a la página de inicio.
    :rtype: str
    """
    
    if not auth.has_permits(["user_index"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    
    search_email = request.args.get('search_email')
    
    selected_option = request.args.get('active')
    
    if search_email:
        # Realiza la búsqueda filtrada por email
        users = list(filter(lambda usu : usu.id != session["user"] and usu.id not in get_super_admin_ids(), usuariosFiltroMail(search_email)))
    else:
        # Si no hay un filtro de búsqueda, muestra todos los usuarios
        users = list(filter(lambda usu: usu.id != session['user'] and usu.id not in get_super_admin_ids(), list_users()))
        
    users = filtrar_usuarios_por_estado(users, selected_option)
    
    users = users if (session["role"] == "Super Administrador" or session["role"] == "Dueño") else filtrar_usuarios_misma_institucion(session["institutions"], users)
    institution_per_user, rol_per_user = institutions_and_roles_per_user(users)
    
    users, total_page, page = pagination(users)
    email_buscado= search_email if search_email else ""
        
    return render_template('users/index.html', users=users, total_pages= total_page,
                           current_page = page, institution_per_user = institution_per_user,
                           rol_per_user=rol_per_user, selected_option=selected_option,
                           email_buscado=email_buscado)
    


@auth.login_required
@users_bp.route('create_user', methods=['GET','POST'])
@mantenimiento_required
def create_user():
    """
    Crea un nuevo usuario en el sistema.
    Este método permite a un usuario con los permisos adecuados crear un nuevo usuario en el sistema.
    El usuario debe completar un formulario con la información del nuevo usuario, incluyendo su nombre,
    apellido, nombre de usuario, dirección de correo electrónico, rol y afiliación a una institución.    
    Si el método recibe una solicitud POST, procesará los datos del formulario y creará el nuevo usuario
    en el sistema. Luego, se mostrará un mensaje de éxito y se redirigirá a la lista de usuarios.    
    Si la solicitud es de tipo GET, se muestra el formulario para crear un nuevo usuario, permitiendo
    al usuario ingresar la información necesaria.
    :return: Si la solicitud es de tipo POST y se crea el nuevo usuario con éxito, se muestra un mensaje de
             éxito y se redirige a la lista de usuarios. Si la solicitud es de tipo GET, se muestra el formulario
             para crear un nuevo usuario. Si el usuario no tiene permisos para acceder a esta función, se muestra
             un mensaje de error y se redirige a la página de inicio.
    :rtype: str
    """
    if not auth.has_permits(["user_new"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    if request.method == 'POST':
        name=request.form.get('name')
        lastname=request.form.get('lastname')
        username= request.form.get('username')
        email=request.form.get('email')
        role_id=request.form.get('rol')
        institucion_id=request.form.get('institucion')
        activo=request.form.get('activo')

        #if (createUser(name,lastname,username,email) and createUserRole(role_id) and addMember(institucion_id))
        flash('Usuario creado con éxito.', 'success')
        return redirect(url_for('users.index')) # FALTA LOS CASOS QUE FALLE POR ALGO
    else:
        roles= list_roles()
        instituciones= list_institutions()
        return render_template('users/createUser.html', instituciones=instituciones, roles=roles)

@auth.login_required
@users_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@mantenimiento_required
def delete_user(user_id):
    """
    Elimina un usuario del sistema.
    Este método permite a un usuario con los permisos adecuados eliminar un usuario existente del sistema.
    El usuario debe confirmar la eliminación del usuario seleccionado. Si la solicitud es de tipo POST y
    la eliminación se realiza con éxito, se mostrará un mensaje de éxito y se redirigirá a la lista de usuarios.
    Si la solicitud es de tipo GET, se mostrará una página de confirmación.
    :param user_id: El ID del usuario que se va a eliminar.
    :type user_id: int
    :return: Si la solicitud es de tipo POST y la eliminación se realiza con éxito, se muestra un mensaje de éxito
             y se redirige a la lista de usuarios. Si la solicitud es de tipo GET, se muestra una página de confirmación.
             Si el usuario no tiene permisos para acceder a esta función, se muestra un mensaje de error y se redirige
             a la página de inicio.
    :rtype: str
    """
    if not auth.has_permits(["user_destroy"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    if request.method == 'POST':
        delete_rol(user_id)
        if deleteUsuario(user_id)  :
            flash('Usuario eliminado con éxito.', 'success')
        else:
            flash('Falló la eliminación del usuario', 'error')
        return redirect(url_for('users.index'))

    # Si se accede a la página con un método GET, simplemente muestra una página de confirmación.
    user = getUserById(user_id)
    return render_template('users/deleteUser.html', user=user)

@users_bp.get("/profile/<int:id>")
@auth.login_required
@mantenimiento_required
def user_profile(id):
    """
    Muestra el perfil de un usuario.
    Este método permite a un usuario con los permisos adecuados ver el perfil de un usuario específico.
    El perfil del usuario se muestra en una plantilla de perfil, y se requiere el ID del usuario como parámetro.
    :param id: El ID del usuario cuyo perfil se va a mostrar.
    :type id: int
    :return: Si el usuario tiene los permisos necesarios y el ID del usuario es válido, se muestra la plantilla
             de perfil del usuario. Si no se cumplen estas condiciones, se muestra un mensaje de error y se redirige
             a la página de inicio.
    :rtype: str
    """
    
    if not auth.has_permits(["user_show"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    
    user_profile = find_user_by_id(id)
    if user_profile:
        return render_template("users/profile.html", user=user_profile)
    
    flash("El ID del usuario no se encuentra en registrado","error")
    return redirect(url_for("home.index"))



@users_bp.route("/api/auth", methods=["POST"])
def authenticate():
    """
    Autentica un usuario y genera un token de acceso.
    Este endpoint permite a un usuario iniciar sesión proporcionando un nombre de usuario y una contraseña.
    Si las credenciales son válidas, se genera un token de acceso que puede utilizarse para acceder a recursos protegidos.
    :return: Un token de acceso si la autenticación es exitosa. En caso de credenciales inválidas, se devuelve un
             mensaje de error.
    :rtype: tuple
    """
    data = request.get_json()
    user = data.get("user")
    password = data.get("password")

    user = User.query.filter_by(email=user).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify(token=access_token), 200
    else:
        return jsonify(error="Credenciales inválidas"), 400
    
@users_bp.route("/api/me/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """
    Obtiene el perfil del usuario autenticado.
    Este endpoint permite a un usuario autenticado obtener su perfil. Requiere que el usuario haya iniciado sesión
    previamente y proporcionado un token de acceso válido.
    :return: Un objeto JSON que contiene la información del perfil del usuario, incluyendo nombre de usuario, correo
             electrónico, nombre, apellido y estado de activación. Si el usuario no se encuentra en la base de datos, se
             devuelve un mensaje de error.
    :rtype: tuple
    """
    user_email = get_jwt_identity()

    user = User.query.filter_by(email=user_email).first()
    if user:
        profile_data = {
            "user": user.username,
            "email": user.email,
            "name": user.name,
            "lastname": user.lastname,
            "activo": user.activo,
        }
        return jsonify(profile_data), 200
    else:
        # Si el usuario no se encuentra en la base de datos, devuelve un error 404 o un mensaje de error apropiado.
        return jsonify({"error": "Usuario no encontrado"}), 404
    

@auth.login_required
@users_bp.route('/modify_user/<int:user_id>', methods=['GET', 'POST'])
@mantenimiento_required
def modify_user(user_id):
    """
    Modifica un usuario existente.
    Este endpoint permite a un usuario con los permisos adecuados modificar los datos de un usuario existente. Se pueden
    cambiar el nombre, apellido, rol y estado de activación del usuario.
    :param int user_id: El ID del usuario que se desea modificar.
    :return: Si el usuario tiene los permisos necesarios, se muestra un formulario para modificar los datos del usuario.
             Después de enviar el formulario, los datos se actualizan en la base de datos. Si la modificación es exitosa,
             se muestra un mensaje de éxito y se redirige a la página de usuarios. Si la modificación falla, se muestra un
             mensaje de error.
    :rtype: tuple
    """
    if not auth.has_permits(["user_update"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
 
    user = getUserById(user_id) 
    
         
    roles = list(filter(lambda rol : rol.id != 1 , list_roles()))  
    instituciones_disponibles = list(filter(lambda inst : inst.id>2, list_institutions()))
    
    form = UserForm(obj=user)

    form.institutions.choices = [(inst.id, inst.name) for inst in instituciones_disponibles]
    form.rol.choices = [(rol.id, rol.name) for rol in roles]
    
    if request.method == 'POST' and form.validate():
        
        name = form.name.data
        lastname = form.lastname.data
        role_id = form.rol.data
        estado = bool(int(form.estado.data))
        
        selected_institutions = form.institutions.data

        if updateUser(user, name, lastname, estado) and update_role(user_id, role_id, selected_institutions):
                flash('Datos modificados con éxito.', 'success') ## falta guardar datos en BD            
        else:
            flash('Fallo la modificacion del usuario, revise si el correo electronico ya esta en uso o los datos ingresdos son validos.', 'error') 
        return redirect(url_for('users.index'))  # Redirigir a la página de usuarios 
    
    
    return render_template('users/modifyUserModal.html', form=form, user_id=user.id)
        

        
       
    

