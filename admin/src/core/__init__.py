from flask import request
from src.core.model.pagination import Pagination

def pagination(filter):
    """Realiza la paginación de una lista de elementos, la función calcula la paginación de los elementos en función de la página solicitada y
    la cantidad de elementos por página.
    Si el parámetro 'filter' es un objeto query, se utiliza el método 'slice' (si está disponible) para realizar la paginación de manera eficiente.
    Si 'filter' es una lista, se realiza la paginación de forma estándar."""
    
    # Obtiene el número de página solicitada de la URL.
    page = request.args.get('page', type=int, default=1)

    # Obtiene la cantidad de elementos por página desde una fuente externa.
    per_page = Pagination.query.get(1).cant

    # Intenta contar la cantidad total de elementos en 'filter'.
    # Si no es posible (por ejemplo, 'filter' es una lista), usa 'len' para obtener la cantidad.
    try:
        total_filter = filter.count()
    except:
        total_filter = len(filter)

    # Calcula la cantidad total de páginas necesarias para mostrar todos los elementos paginados.
    total_pages = (total_filter + per_page - 1) // per_page

    # Calcula el índice de inicio y fin para la página actual.
    start = (page - 1) * per_page
    end = start + per_page

    # Obtiene los elementos que corresponden a la página actual.
    # Utiliza 'slice' si 'filter' es un objeto query, de lo contrario, corta la lista.
    try:
        filters = filter.slice(start, end)
    except:
        filters = filter[start:end]

    # Devuelve una tupla que contiene los elementos de la página actual, el número total de páginas y el número de página actual.
    return filters, total_pages, page