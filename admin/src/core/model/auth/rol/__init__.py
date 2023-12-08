from src.core.model.auth.rol.role import Role
from src.core.database import db

def list_roles():
    """
    Obtiene una lista de todos los roles disponibles en la base de datos.
    Returns:
    list[Role]: Una lista de objetos Role que representan los roles disponibles.
    """
    roles = Role.query.all()
    
    return roles

def create_role(**kwargs):
    """
    Crea un nuevo rol en la base de datos.
    Args:
    **kwargs: Parámetros que representan los atributos del rol, como 'name' y 'description'.
    Returns:
    Role: El objeto Role recién creado y almacenado en la base de datos.
    """
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    
    return role

def get_rol_by_id(role_id):
    """
    Recupera un objeto Role a partir de su ID.
    Args:
    role_id (int): El ID del rol que se desea recuperar.
    Returns:
    Role: El objeto Role correspondiente al ID proporcionado, o None si no se encuentra ningún rol con ese ID.
    """
    rol = Role.query.filter_by(id=role_id).first()
    return rol


def get_super_admin_role():
    '''
        recupera el objeto a partir del String "Super Administrador"
    '''
    return Role.query.filter_by(name = "Super Administrador").first()