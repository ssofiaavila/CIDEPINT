from src.core.database import db

def sort_query(campo, query, orden):
    """Retorna una lista de servicios ordenados por nombre de forma descendente"""
    if orden == 'asc':
        return query.order_by(db.asc(campo))
    else:
        return query.order_by(db.desc(campo))