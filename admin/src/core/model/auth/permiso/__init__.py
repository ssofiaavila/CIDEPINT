from src.core.model.auth.permiso.permit import Permit
from src.core.database import db

def list_permits():
    """
    Recupera una lista de todos los objetos Permit en la base de datos.
    Returns:
    list of Permit: Una lista que contiene todos los objetos Permit en la base de datos.
    """
    permits = Permit.query.all()
    
    return permits


def list_permits_by_id(id):
    """
    Recupera un objeto Permit de la base de datos según su ID.
    Parameters:
    id (int): El ID del objeto Permit que se desea recuperar.
    Returns:
    Permit or None: El objeto Permit correspondiente al ID proporcionado, o None si no se encuentra.
    """
    permit =  Permit.query.filter_by(id=id).first()
    return permit

def create_permit(**kwargs):
    """
    Crea y almacena un nuevo objeto Permit en la base de datos.
    Parameters:
    kwargs (dict): Un diccionario que contiene los atributos del nuevo objeto Permit.
    Returns:
    Permit: El objeto Permit recién creado y almacenado en la base de datos.
    Example:
    new_permit = create_permit(name='Permission Name', description='Permission Description')
    """
    permit = Permit(**kwargs)
    db.session.add(permit)
    db.session.commit()
    
    return permit