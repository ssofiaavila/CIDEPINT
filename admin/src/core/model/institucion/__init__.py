from sqlalchemy import desc, func
from src.core.model.request.service_request import ServiceRequest
from src.core.model.institucion.institucion import Institution
from src.core.model.days_hours.days_hours import DiasHorarios, FranjaHoraria, Dias, DiasHorarios, FranjaHoraria
from src.core.model.combined_tables.user_has_role import User_has_role
from src.core.database import db
from src.web.helpers.geocodificacion import geocodificacion
from src.core.model.servicio import Service

def load_dict(dictionary):
    """Carga el dicciionario con todos los elementos pasados por parametro y transofrma los 'enabled' en True o False respectivamente y posteriormente retorna
    el diccionario ya cargado."""
    kwargs_result = dict()
    for clave, valor in dictionary.items():
        kwargs_result[clave] = valor

    if kwargs_result["enabled"] == "True":
        kwargs_result["enabled"] = True
    else: 
        kwargs_result["enabled"] = False

    return kwargs_result

def list_institutions():
    """Lista todas las instituciones y las retorna."""
    institutions = Institution.query.all()
    return institutions

def create_institution(**kwargs):
    """Crea la institucion con los datos pasados en los **kwargs, si hay caso de error por integracion (nombre duplicado) entonces se hace un rollback(), es decir,
    revierte las transacciones NO CONFIRMADAS.
    También se llama a la función geocodificacion, que se encarga de obtener la latitud y longitud de la dirección pasada por parametro en los **kwargs.
    """
    try:
        kwargs['location'] = geocodificacion(kwargs['address'])
        institution = Institution(**kwargs)
        db.session.add(institution)
        db.session.commit()
        return institution
    except db.exc.IntegrityError:
        db.session.rollback()
        return False

def delete(id):
    """Busca en la tabla instituciones el ID pasado por parametro, luego aplica lo mismo con la tabla DiasHorarios, en caso de encontrar esa dependencia la borra
    y lo mismo aplica para las dependencias de user_has_role, y elimina todo; inlcuido las instituciones."""
    institution = Institution.query.get(id)

    days_hours_dependency = DiasHorarios.query.filter(DiasHorarios.institution_id==id).all()
    for insti in days_hours_dependency:
        db.session.delete(insti)
        db.session.commit()

    if search_dependency(id):
        delete_dependency(id)
    db.session.delete(institution)
    db.session.commit()
    return True

def search_dependency(id):
    """Retorna true o false en caso de que haya dependencias."""
    dependency = User_has_role.query.filter(User_has_role.institution_id==id).all()
    return True if dependency else False

def delete_dependency(id):
    """Busca en la tabla User_has_role por id de institucion y nos da TODAS las dependencias en esa tabla y, posteriormente, las borra."""
    dependency  = User_has_role.query.filter(User_has_role.institution_id==id).all()
    for insti in dependency:
        db.session.delete(insti)
        db.session.commit()  

def update_institution(id,**kwargs):
    """Busca en la tabla institucion por id, cuando la encuentra actualiza todos los datos que se pasaron por parametro en el **kwargs."""
    institution = Institution.query.get(id)
    if institution:
        for key, value in kwargs.items():
            setattr(institution, key, value)
        db.session.commit()
        return True
    return False

def get_institution_by_id(id):
    """Busca en la tabla institucion por id y retorna la institucion."""
    return Institution.query.get(id)

def get_institution_by_name(name):
    """Busca en la tabla institucion por nombre y retorna la institucion."""
    institution = Institution.query.filter_by(name=name).first()
    return institution

def update_days(institution_id, selected_days, selected_time_slots):
    """Busca en la tabla de 'DiasHoriarios' la ID de la institucion pasada por paramaetro, cuando la encuentra consulta si se encontro, en caso de hacerlo busca en la tabla de
    Dias la ID de la columna 'dia_id' de la tabla 'DiasHorarios', cuando la encuentra setea todos los trues o falses pasados por parametro en el selected_days, luego le setea la franja
    seleccionada, pasada por parametro tambien, selected_time_slots, realiza el commit fin."""
    days_hour = DiasHorarios.query.filter(
        DiasHorarios.institution_id == institution_id).first()

    if days_hour:
        days = Dias.query.get(days_hour.dia_id)
        for key, value in selected_days.items():
            setattr(days, key, value)
        days_hour.franja_horaria_id = selected_time_slots
        db.session.commit()
        return True
    else:
        return False


def list_institution_by_keywords_or_name(keyword):
    """Retorna una lista de instituciones en las que su nombre o palabra clave, contenga el string recibido por parámetro"""
    return Institution.query.filter(
        db.or_(Institution.name.ilike(
            f"%{keyword}%"), Institution.keywords.ilike(f"%{keyword}%")
               )
        ).all()


def get_all_services():
    institution_with_services = db.session.query(Institution, Service).join(Service).all()

    services_per_institution = []
    current_institution_id = None
    for institution, service in institution_with_services:
        if institution.id != current_institution_id:
            services_per_institution.append({
                'id': institution.id,
                'name': institution.name,
                'services': []
            })
            current_institution_id = institution.id
        services_per_institution[-1]['services'].append({
            'name': service.name,
            'description': service.description
        })

    return services_per_institution


def get_top_institutions():
    # Obtener las 10 instituciones con mayor cantidad de solicitudes
    top_institutions = (
            db.session.query(Institution, db.func.count(ServiceRequest.id).label('request_count'))
            .select_from(Institution)
            .join(Service)
            .join(ServiceRequest)
            .group_by(Institution)
            .order_by(db.desc('request_count'))
            .limit(10)
            .all()
        )

        # Crear una lista de resultados
    result = []
    for institution, request_count in top_institutions:
            result.append({
                "name": institution.name,
                "request_count": request_count
            })

    return result