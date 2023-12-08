from src.core.model.auth.user import User
from src.core.database import db
from flask_bcrypt import Bcrypt
from src.core.model import combined_tables

bcrypt = Bcrypt()
def list_users():
    """
    Recupera una lista de todos los usuarios almacenados en la base de datos.
    Returns:
    list[User]: Una lista de objetos User que representan a todos los usuarios registrados.
    Example:
    users = list_users()
    for user in users:
        print(f"ID: {user.id}, Nombre: {user.name}, Apellido: {user.lastname}")
    """
    users = users = User.query.order_by(User.id.asc()).all()
    return users

def create_user(**kwargs):
    """
    Crea un nuevo usuario en la base de datos.
    Args:
    **kwargs: Argumentos clave y valor que representan los datos del nuevo usuario. Debe incluir al menos 'name', 'lastname', 'username', 'email' y 'password'.

    Returns:
    User: El objeto User recién creado y almacenado en la base de datos.
    
    """
    password_hashed = bcrypt.generate_password_hash(kwargs["password"]).decode('utf-8')
    kwargs.update(password=password_hashed)
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    
    return user

def register_user(**kwargs):
    """
    Registra un nuevo usuario en la base de datos.
    Args:
    **kwargs: Argumentos clave y valor que representan los datos del nuevo usuario. Debe incluir al menos 'name', 'lastname', 'username', 'email' y 'password'.
    Returns:
    User: El objeto User recién registrado y almacenado en la base de datos.
    """
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    combined_tables.assign_relation_user_role_institution(user_id=user.id, institution_id=2, role_id=2)
    return user

def confirmation_registration(**kwargs):
    """
    Completa la información de un usuario registrado previamente con la confirmación de su contraseña.
    Args:
    **kwargs: Argumentos clave y valor que representan los datos necesarios para completar la confirmación del usuario. Debe incluir al menos 'email' y 'password'.
    Returns:
    User: El objeto User con la información actualizada si la confirmación fue exitosa, o None si el usuario no se encontró en la base de datos.

    Example:
    confirmation_data = {'email': 'john@example.com', 'password': 'password123'}
    confirmed_user = confirmation_registration(**confirmation_data)
    if confirmed_user:
        print(f"Confirmación exitosa para el usuario con ID-{confirmed_user.id}, Email-{confirmed_user.email}")
    else:
        print("Usuario no encontrado para la confirmación.")
    """
    user = find_user_by_email(kwargs['email'])
    if user:
        password_hashed = bcrypt.generate_password_hash(kwargs["password"]).decode('utf-8')
        user.password = password_hashed
        user.activo = True
        db.session.commit()
        return user
    else:
        return None

def find_user_by_email(email):
    """
    Busca un usuario en la base de datos por su dirección de correo electrónico.
    Args:
    email (str): La dirección de correo electrónico del usuario que se desea buscar.
    Returns:
    User: El objeto User que coincide con la dirección de correo electrónico proporcionada, o None si no se encuentra ningún usuario con esa dirección de correo.
    """
    return User.query.filter_by(email=email).first()
    
def find_user_by_id(id):
    """
    Busca un usuario en la base de datos por su ID.
    Args:
    id (int): El ID del usuario que se desea buscar.
    Returns:
    User: El objeto User que coincide con el ID proporcionado, o None si no se encuentra ningún usuario con ese ID.
    """
    return User.query.filter_by(id=id).first()

def find_user_by_username(username):
    """
    Busca un usuario en la base de datos por su nombre de usuario (username).

    Args:
    username (str): El nombre de usuario del usuario que se desea buscar.

    Returns:
    User: El objeto User que coincide con el nombre de usuario proporcionado, o None si no se encuentra ningún usuario con ese nombre de usuario.
    """
    return User.query.filter_by(username=username).first()


def validate_user(email, passwd):
    """
    Valida las credenciales de un usuario.
    Args:
    email (str): El correo electrónico del usuario.
    passwd (str): La contraseña proporcionada por el usuario.
    Returns:
    User: El objeto User si las credenciales son válidas, o None si no son válidas.

    """
    user = find_user_by_email(email)
    if user:
        if user.password:
            if user and bcrypt.check_password_hash(user.password, passwd):
                return user
    return None
    
def getUserById(id):
    """
    Obtiene un usuario por su ID.
    Args:
    id (int): El ID del usuario que se desea obtener.
    Returns:
    User: El objeto User correspondiente al ID proporcionado, o None si no se encuentra ningún usuario con ese ID.
    """
    return User.query.filter_by(id=id).first()

def is_email_unique(email, user_id):
    """
    Comprueba si una dirección de correo electrónico es única para un usuario.
    Args:
    email (str): La dirección de correo electrónico que se desea comprobar.
    user_id (int): El ID del usuario para el cual se verifica la unicidad del correo electrónico.
    Returns:
    User or None: El objeto User correspondiente al ID proporcionado y dirección de correo electrónico, o None si no se encuentra ningún usuario con esa combinación.
    """

    
    existing_user = User.query.filter_by(email=email, id=user_id).first()
    return existing_user

def updateUser(user, name, lastname, activo):
    """
    Actualiza los datos de un usuario existente en la base de datos.
    Args:
    user (User): El objeto User que se desea actualizar.
    name (str): El nuevo nombre del usuario.
    lastname (str): El nuevo apellido del usuario.
    activo (bool): El nuevo estado de activación del usuario.
    Returns:
    User or None or bool: El objeto User actualizado en caso de éxito, None si el usuario no se encontró, False en caso de error.
    """
    try:
        
        if user:
            user.name = name
            user.lastname = lastname
            user.activo = activo
            db.session.commit()
            return user  # Éxito
        else:
            return None  # Usuario no encontrado
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return False  # Error al actualizar los datos
    
def deleteUsuario(user_id):
    """
    Elimina un usuario de la base de datos por su ID.
    Args:
    user_id (int): El ID del usuario que se desea eliminar.
    Returns:
    bool: True en caso de éxito al eliminar el usuario, False si el usuario no se encontró o si se produjo un error al eliminarlo.
    """
    try:
        # Obtén el usuario por su ID
        user = find_user_by_id(user_id)
        
        if user:
            # Elimina el usuario de la base de datos
            db.session.delete(user)
            db.session.commit()
            return True  # Éxito al eliminar el usuario
        else:
            return False  # Usuario no encontrado
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return False  # Error al eliminar el usuario
    

def usuariosFiltroMail(search_email):
    """
    Filtra usuarios por dirección de correo electrónico.
    Busca usuarios cuyas direcciones de correo electrónico contengan la cadena especificada en `search_email`.
    Args:
    search_email (str): La cadena que se utilizará para filtrar los usuarios por dirección de correo electrónico.
    Returns:
    list: Una lista de objetos de usuario que coinciden con el filtro.

    """
    return User.query.filter(User.email.ilike(f"%{search_email}%")).all()


def filtrar_usuarios_misma_institucion(listado_instituciones ,listado_usuarios):
    """
    realiza un filtrado de lo usuarios segun el listado de instituciones a las que pertenece el usuario de session

    Args:
        listado_instituciones_id (list<Institution>): se utiliza para matchear la institucion a la que pertenece el usuario
        listado_usuarios (list<User>): se filtrara el listado que ingresa 
    Returns:
    list: una lista de objetos de usuario que coinciden con el filtro
    """
    
    listado_instituciones_id = [ inst.id for inst in listado_instituciones]
   
    return combined_tables.validar_institucion(listado_usuarios, listado_instituciones_id)

def filtrar_usuarios_por_estado(listado_usuarios, estado_seleccionado):
    """
    realiza un filtrado de lo usuarios segun el estado seleccionado en el filtrado
    Args:
        listado_usuarios (list<User>): se filtrara el listado que ingresa 
        estado_seleccionado (String): valor del frontend
    Returns:
    list: una lista de objetos de usuario que coinciden con el filtro
    """
    if estado_seleccionado == "activos":
        return list(filter(lambda usu : usu.activo, listado_usuarios))
    elif estado_seleccionado == "inactivos":
        return list(filter(lambda usu : not usu.activo, listado_usuarios))
    else:
        return listado_usuarios
        



def get_id_by_user_email(user_mail):
    user = User.query.filter_by(email=user_mail).first()
    if user:
        return user.id
    return None
