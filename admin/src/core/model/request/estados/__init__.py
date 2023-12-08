from src.core.database import db
from src.core.model.request.estados.states import Estado

def create_estado(**kwargs):
    """
    Crea y guarda un nuevo estado en la base de datos.
    Args:
    **kwargs: Argumentos clave-valor que representan los atributos del estado a crear.
    Returns:
    bool: True si el estado se creó con éxito, False en caso de error.
    """
    estado = Estado(**kwargs)
    db.session.add(estado)
    db.session.commit()
    return estado

def list_estados():
    """
    devuelve un listado con los posibles estados que tiene cargado la base de datos
    """
    return Estado.query.order_by(Estado.id.asc()).all()

def find_estado_by_id(id):
    """
    Busca un estado por su ID en la base de datos.
    Args:
    id (int): El ID del estado que se desea buscar.
    Returns:
    Estado: El objeto Estado si se encontró, None si no se encontró un estado con el ID especificado.
    """
    return Estado.query.get(id)

