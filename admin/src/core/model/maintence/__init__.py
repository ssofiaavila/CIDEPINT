from .maintence import Maintence
from src.core.database import db

def create_maintence(**kwargs):
    """Crea el mantenimiento con los **kwargs pasados por parametros"""
    maintence = Maintence(**kwargs)
    db.session.add(maintence)
    db.session.commit()
    return maintence