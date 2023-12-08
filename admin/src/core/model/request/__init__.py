from src.core.model.request.service_request import ServiceRequest
from src.core.database import db
from src.core.model.servicio import search_service, list_services_institution_id
from src.core.model.request.estados import find_estado_by_id
from src.core.model.request.estados import create_estado
from datetime import datetime

def create_request(**kwargs):
    """
    Crea una solicitud de servicio en la base de datos con los detalles proporcionados. Le instancia un estado inicial y un primer comentario.
    Args:
    **kwargs: Datos de la solicitud de servicio, como `service_id`, `user_id`, etc.
    Returns:
    ServiceRequest: retorna la instancia creada
    """
    kwargs["comment"] = f"{get_hora_y_dia_actual()} - Solicitud de servicio recibida\n"
    if kwargs['comments']:
        kwargs["comment"] += f"Comentario/s: {kwargs['comments']}\n"
    request = ServiceRequest(**kwargs)
    db.session.add(request)
    db.session.commit()
    return request

def list_requests():
    """
    Obtiene una lista de todas las solicitudes de servicio en la base de datos.
    Returns:
    list: Una lista de objetos ServiceRequest que representan las solicitudes.
    """
    requests = ServiceRequest.query.all()
    return requests

def search_request(id):
    """
    Busca una solicitud de servicio por su ID en la base de datos.
    Args:
    id (int): El ID de la solicitud que se desea buscar.
    Returns:
    ServiceRequest or None: La solicitud de servicio si se encuentra, o None si no se encuentra.
    """
    request = ServiceRequest.query.get(id)
    return request

def list_request_by_service_id(service_id):
    """
    Obtiene una lista de solicitudes de servicio asociadas a un servicio específico.
    Args:
    service_id (int): El ID del servicio.
    Returns:
    list: Una lista de objetos ServiceRequest que representan las solicitudes asociadas al servicio.
    """
    requests = ServiceRequest.query.filter(
        ServiceRequest.service_id == service_id).all()
    return requests

def list_request_by_institution(id):
    """
    Obtiene una lista de solicitudes de servicio asociadas a una lista de servicios de institución.
    Args:
    institution_services_list (list): Una lista de objetos de servicios de institución.
    Returns:
    list: Una lista de objetos ServiceRequest que representan las solicitudes asociadas a los servicios de institución.
    """
    institution_services_list = list_services_institution_id(id)
    institution_service_id_list = [ serv.id for serv in institution_services_list]
    requests = list(filter(
        lambda req : req.service_id in institution_service_id_list, list_requests()))
    return requests

def list_request_by_user_id_paginated(user_id):
    """
    Obtiene una lista de solicitudes de servicio asociadas a un usuario específico.
    Args:
    user_id (int): El ID del usuario.
    Returns:
    list: Una lista de objetos ServiceRequest que representan las solicitudes asociadas al usuario.
    """
    requests = ServiceRequest.query.filter(ServiceRequest.user_id == user_id)
    return requests


def list_request_by_user_id(user_id):
    """
    Obtiene una lista de solicitudes de servicio asociadas a un usuario específico.
    Args:
    user_id (int): El ID del usuario.
    Returns:
    list: Una lista de objetos ServiceRequest que representan las solicitudes asociadas al usuario.
    """
    requests = ServiceRequest.query.filter(ServiceRequest.user_id == user_id).all()
    return requests

def switch_status( request_id, estado_id,):
    """
    Cambia el estado a una solicitud de servicio existente.
    Args:
    estado_id(int): El ID que se actualizara a la solicitud.
    request_id (int): El ID de la solicitud a la que se agregará el comentario.
    Returns:
    None
    """
    request = search_request(request_id)
    request.estado_id = estado_id
    add_comment(f"Se ha cambio el estado a {request.estados.name}", request_id)
    db.session.commit()

def add_comment(comment, request_id):
    """
    Agrega un comentario a una solicitud de servicio existente.
    Args:
    comment (str): El comentario que se agregará a la solicitud.
    request_id (int): El ID de la solicitud a la que se agregará el comentario.
    Returns:
    None
    """
    request = search_request(request_id)
    request.comment = f"{request.comment}{get_hora_y_dia_actual()} - {comment}\n"
    db.session.commit()

def delete_request(id):
    """
    Elimina una solicitud de servicio de la base de datos por su ID.
    Args:
    id (int): El ID de la solicitud que se eliminará.
    Returns:
    bool: True si la solicitud se eliminó con éxito, False si no se encontró la solicitud.
    """
    request = search_request(id)
    if request:
        db.session.delete(request)
        db.session.commit()
        return True
    else:
        return False    
    
def mapper_to_request_data(request_list):
    """
    Convierte una lista de objetos ServiceRequest en una lista de datos de solicitud estructurados.
    Args:
    request_list (list): Una lista de objetos ServiceRequest.
    Returns:
    listado_final: Una lista de diccionarios que representan los datos de las solicitudes.
    """
    listado_final = [ map_request(req) for req in request_list ]
    return listado_final

def map_request(request):
    """
    Convierte un objeto ServiceRequest en un diccionario de datos.
    Los campos del diccionario son: user, id, comment, service, service_type, status, requested, institution.
    """
    servicio = search_service(request.service_id)
    dict_request = {
        "user":f"{request.users.name} {request.users.lastname}",
        "id":request.id,
        "comment":text_replace(request.comment),
        "service":servicio.name,
        "service_type":servicio.service_type,
        "status":find_estado_by_id(request.estado_id).name,
        "requested": formatted_datetime(request.inserted_at),
        "institution":servicio.institution.name
    }
    return dict_request

def formatted_datetime(dateandtime):
    """
    Convierte un objeto datetime en una cadena de texto con formato DD-MM-AAAA HH:MM:SS.
    """
    return f'{dateandtime.strftime("%d-%m-%Y %H:%M:%S")}'

def get_hora_y_dia_actual():
    """
    Retorna la fecha y hora actual en formato DD-MM-AAAA HH:MM:SS.
    """
    return formatted_datetime(datetime.now())

def text_replace(text):
    """
    Reemplaza los saltos de línea en un texto por la etiqueta <br> de HTML.
    """
    return text.replace('\n', '<br>')