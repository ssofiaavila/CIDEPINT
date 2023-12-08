from src.core.model.pagination.pagination import Pagination
from src.core.database import db

def create_pagination(cant):
    """
    Crea un registro de paginación en la base de datos con la cantidad especificada de elementos por página.
    Args:
    cant (int): La cantidad de elementos por página.
    Returns:
    None
    """
    pagination = Pagination(cant=cant)
    db.session.add(pagination)
    db.session.commit()

def update_pagination(cant):
    """
    Actualiza la cantidad de elementos por página en el registro de paginación existente en la base de datos.
    Args:
    cant (int): La nueva cantidad de elementos por página.
    Returns:
    None
    """
    pagination = Pagination.query.get(1)
    pagination.cant = cant
    db.session.commit()

def get_pagination():
    """
    Obtiene la cantidad de elementos por página desde la base de datos.
    Args:
    None
    Returns:
    int: La cantidad de elementos por página.
    """
    return Pagination.query.get(1).cant