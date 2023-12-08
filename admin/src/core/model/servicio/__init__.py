from src.core.model.request.estados.states import Estado
from src.core.model.request.service_request import ServiceRequest
from src.core.model.servicio.servicio import Service
from flask import session
from src.core.database import db


def create_service(**kwargs):
    """Crea un instancia de Servicio, la carga a la base de datos y y retorna la instancia"""
    try:
        service = Service(**kwargs)
        db.session.add(service)
        db.session.commit()
        return True
    except db.exc.IntegrityError:
        db.session.rollback()
        return False

def list_services():
    """Lista a todos los servicios cargados en base de datos"""
    services = Service.query.all()
    return services

def list_services_institution_id(inst_id):
    """Retorna todos los servicios que perteneces a la institución recibida por parámetro"""
    services = Service.query.filter(Service.institution_id == inst_id).all()
    return services

def update_service(id, **kwargs):
    """Actualiza el valor de los atributos"""
    service = search_service(id)
    if service:
        try:
            for key, value in kwargs.items():
                setattr(service, key, value)
            db.session.commit()
            return True
        except db.exc.IntegrityError:
            db.session.rollback()
            return False

def delete_service(id):
    """Elimina de la BD el servicio del id recibido por parametro"""
    service = search_service(id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return True
    
def search_service(id):
    """Retorna el servicio que tiene como id el valor recibido por parámetro"""
    service = Service.query.get(id)
    return service

def list_services_by_keywords_or_name(keyword):
    """Retorna una lista de servicios en las que su nombre o palabra clave, contenga el string recibido por parámetro"""
    return Service.query.filter(db.or_(Service.name.ilike(f"%{keyword}%"), Service.keywords.ilike(f"%{keyword}%"))).all()

def list_services_by_keywords_name_desc_or_inst(keyword):
    """Retorna una lista de servicios en las que su nombre o palabra clave, contenga el string recibido por parámetro"""
    return Service.query.filter(db.or_(
        Service.name.ilike(f"%{keyword}%"), 
        Service.keywords.ilike(f"%{keyword}%"), 
        Service.description.ilike(f"%{keyword}%"), 
        Service.institution.name.ilike(f"%{keyword}%"))).all()

def list_services_by_type(service_type):
    return Service.query.filter(Service.service_type.ilike(f"%{service_type}")).all()



def get_top_requested_services():
    """Obtiene los servicios más solicitados"""
    top_services = (
        db.session.query(Service, db.func.count(ServiceRequest.id).label('request_count'))
        .join(ServiceRequest)
        .group_by(Service)
        .order_by(db.desc('request_count'))
        .limit(10)
        .all()
    )

    result = []
    for service, request_count in top_services:
        result.append({
            "name": service.name,
            "request_count": request_count
        })

    return result


def get_request_per_state():
    """Devuelve la cantidad de solicitudes de servicio por cada estado"""
    states = Estado.query.all()
    result = {}

    for state in states:
        state_name = state.name
        count = ServiceRequest.query.filter_by(estado_id=state.id).count()
        result[state_name] = count

    return result