import datetime
import re
from flask import Blueprint, request, flash, jsonify, url_for, redirect, session, render_template
from flask import render_template
from src.core.model.institucion.institucion import Institution
from src.core.model.request.estados.states import Estado
from src.core.model.servicio import *
from src.core.model.servicio.servicio import TipoServicio
from src.core.model.request.service_request import ServiceRequest
from src.core.model.servicio import create_service, list_services, list_services_by_keywords_or_name, search_service, update_service, delete_service, get_request_per_state
from src.core.model.request import create_request, list_request_by_user_id, mapper_to_request_data, list_request_by_institution, search_request, map_request, add_comment, switch_status,list_request_by_user_id_paginated, search_request
from src.web.helpers import auth
from src.core.model.auth import getUserById, get_id_by_user_email
from src.core.model.institucion import list_institutions
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import logging
from src.core.database import db
from src.web.helpers.validations import institution_name, is_valid_search_term, is_valid_service_type
from src.web.controllers.home import mantenimiento_required
from src.core import pagination
from src.core.model.pagination import get_pagination
from src.core.model.request.estados import list_estados
from src.web.helpers.ids_estados import ids_estados
from src.web.error import parametrosInvalidos
from src.web.helpers.list_sorting import sort_query

service_bp = Blueprint("services", __name__, url_prefix="/services")

@service_bp.route("/")
@auth.login_required
@mantenimiento_required
def index():
    """
    Muestra la lista de servicios disponibles y permite filtrarlos por palabras clave.
    Returns:
        Flask response: Muestra una lista de servicios disponibles y permite filtrarlos por palabras clave. 
                        También admite la paginación para mostrar un número limitado de servicios por página.
                        Si el usuario no tiene acceso o no está autenticado, se redirige a la página de inicio de sesión.
    Note:
        - Se requiere el rol de mantenimiento para acceder a esta vista.
        - Los servicios se pueden filtrar por palabras clave proporcionadas a través de la consulta 'search_services'.
        - La paginación se aplica para mostrar un número limitado de servicios por página.
    """

    if not auth.has_permits(["serv_index"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    keyword = request.args.get('search_services')
    if keyword:
        services_list = list(filter(lambda serv : serv.enabled, list_services_by_keywords_or_name(keyword)))
    else:
        services_list = list(filter(lambda serv : serv.enabled, list_services()))
    services_list, total_pages, page = pagination(services_list)
    return render_template("services/index.html", services=services_list,  total_pages=total_pages, current_page=page)


@auth.login_required
@service_bp.route("/create")
@mantenimiento_required
def create():
    """
    Muestra el formulario de creación de un nuevo servicio.
    Returns:
        Flask response: Muestra el formulario de creación de un servicio, permitiendo a los usuarios con rol de mantenimiento
                        agregar un nuevo servicio. Si el usuario no tiene acceso o no está autenticado, se redirige a la página
                        de inicio de sesión.
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden acceder a esta vista.
    """
    if not auth.has_permits(["serv_new"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    institutions_list = session["institutions"]
    return render_template("services/create.html", institutions=institutions_list)


@auth.login_required
@service_bp.route("/created", methods=["POST"])
@mantenimiento_required
def created():
    """
    Crea un nuevo servicio o muestra el formulario de creación de servicios.
    Returns:
        Flask response: Si la solicitud es GET, muestra el formulario de creación de servicios.
                        Si la solicitud es POST y la creación se realiza con éxito, redirige a la vista "Mis Servicios" con un mensaje de éxito.
                        Si la creación no se puede completar, muestra un mensaje de error.
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden acceder a esta vista.
    """
    if not auth.has_permits(["serv_new"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    kwargs = dict()
    errors = []
    if request.method == 'POST':

        required_fields = ["name", "description", "keywords"]
        for field in required_fields:
            if not request.form.get(field).strip():
                errors.append(f"El campo {field} no puede ser un blanco.")
            elif not request.form.get(field):
                errors.append(f"El campo {field} es obligatorio.")

        if not institution_name(request.form.get('name')):
            errors.append(f"Nombre de servicio invalido.")

        if errors:
            for error in errors:
                flash(error,'error')
            return redirect(url_for('services.create'))

        for clave, valor in request.form.items():
            kwargs[clave] = valor
        if create_service(**kwargs):
            flash('La institucion se ha creado exitosamente', 'success')
        else:
            flash('Ya existe un servicio con ese nombre', 'error')
    return my_services(kwargs["institution"])


@auth.login_required
@service_bp.route("/modify/<int:id>", methods=['GET', 'POST'])
@mantenimiento_required
def modify(id):
    """
    Permite la modificación de un servicio existente y muestra el formulario de modificación.
    Args:
        id (int): El ID del servicio que se desea modificar.
    Returns:
        Flask response: Si la solicitud es GET, muestra el formulario de modificación.
                        Si la solicitud es POST y la modificación se realiza con éxito, redirige a la vista "Mis Servicios" con un mensaje de éxito.
                        Si la modificación no se puede completar, muestra un mensaje de error.
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden acceder a esta vista.
    """
    if not auth.has_permits(["serv_update"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    a_service = search_service(id)
    return render_template("services/modify.html", service=a_service)


@auth.login_required
@service_bp.route("modified/<int:id>", methods=['POST'])
@mantenimiento_required
def modified(id):
    """
    Modifica un servicio existente y muestra un mensaje de éxito o error.
    Args:
        id (int): El ID del servicio que se desea modificar.
    Returns:
        Flask response: Redirige a la vista de "Mis Servicios" después de realizar la modificación del servicio.
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden acceder a esta vista.
    """
    if not auth.has_permits(["serv_update"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    kwargs = dict()
    if request.method == 'POST':
        for clave, valor in request.form.items():
            kwargs[clave] = valor
        kwargs["enabled"] = True if request.form["enabled"] == "True" else False
        if update_service(id, **kwargs):
            flash('El servicio se ha modificado exitosamente', 'success')
        else:
            flash('No se logró modificar el servicio', 'error')
    return my_services(search_service(id).institution_id)


@auth.login_required
@mantenimiento_required
@service_bp.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    """
    Muestra una página para confirmar la eliminación de un servicio.
    Args:
        id (int): El ID del servicio que se desea eliminar.
    Returns:
        Flask response: Renderiza una página de confirmación de eliminación para el servicio seleccionado.        
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden acceder a esta vista.
    """
    if not auth.has_permits(["serv_destroy"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    a_service = search_service(id)
    return render_template("services/delete.html", service=a_service)


@auth.login_required
@service_bp.route("deleted/<int:id>", methods = ['POST'])
@mantenimiento_required
def deleted(id):
    """
    Elimina un servicio por su ID y redirige a la página de inicio.
    Args:
        id (int): El ID del servicio que se va a eliminar.
    Returns:
        Flask response: Redirige a la página de inicio y muestra un mensaje de éxito si el servicio se elimina correctamente.
    Note:
        - Se requiere autenticación para acceder a esta vista.
        - Solo los usuarios con el rol de mantenimiento pueden eliminar servicios.
    """
    if not auth.has_permits(["serv_destroy"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    if delete_service(id):
        flash('El servicio se ha eliminado exitosamente','success')
    return index()



@service_bp.route("/api/services/search", methods=["GET"])
def search_services():
    """
    Realiza una búsqueda de servicios según los parámetros especificados y devuelve los resultados en formato JSON.
    Args:
        q (str, optional): Término de búsqueda principal. Por defecto, está vacío.
        type (str, optional): Tipo de servicio. Por defecto, está vacío.
        page (int, optional): Número de página actual. Por defecto, es 1.
    Returns:
        str: Un objeto JSON que contiene una lista de servicios que coinciden con los parámetros de búsqueda.
    Raises:
        400 (Bad Request): Si no se proporciona un término de búsqueda ni un tipo de servicio válido.
    Note:
        - Los resultados de búsqueda se paginan para mostrar solo una cantidad limitada de servicios por página.
        - Los parámetros de búsqueda se combinan con una operación "Y" (es decir, deben coincidir con ambos para obtener resultados).
    """
    # Obtén los parámetros de la consulta (q, type, page)
    search_term = request.args.get("q", default="", type=str) # término de búsqueda ppal
    service_type = request.args.get("type", default="", type=str) #tipo de servicio
    page = request.args.get("page", default=1, type=int) #nro de página actual
    order = request.args.get("order", default="", type=str) #campo de ordenamiento

    # Validación de parámetros
    if search_term and not is_valid_search_term(search_term):
        return parametrosInvalidos()
    if service_type and not is_valid_service_type(service_type):
        return parametrosInvalidos()

    # Aplica filtro de busqueda para obtener los servicios de las instituciones habilitadas
    query = Service.query.filter(Service.institution.has(Institution.enabled == True))
   
    # Aplica filtro de busqueda para obtener los servicios habilitados
    query = query.filter(Service.enabled == True)

    # # Aplica los filtros según los parámetros recibidos
    if search_term:
        query = query.filter(db.or_(
        Service.name.ilike(f"%{search_term}%"),
        Service.description.ilike(f"%{search_term}%"),
        Service.keywords.ilike(f"%{search_term}%"),
        Service.institution.has(Institution.name.ilike(f"%{search_term}%"))))

    if service_type:
        query = query.filter(Service.service_type.ilike(f"{service_type}"))

    # Obtiene la cantidad de elementos por página desde una fuente externa(la base de datos).
    per_page = get_pagination()

    # Ordena los resultados según el campo de ordenamiento
    ordenacion = sort_query(Service.name, query, order)

    # Pagina los resultados
    pagination = ordenacion.paginate(page=page, per_page=per_page)
    
    # Obtiene los servicios de la paginación
    services = pagination.items

    # Formatea los resultados como un diccionario
    result = {
        "data": [{
            "name": service.name,
            "description": service.description,
            "type": service.service_type,
            "laboratory": service.institution.name,  # Añade aquí la información correspondiente
            "id": service.id,
        } for service in services],
        "total_pages": pagination.pages,
        "total": len(services)
    }

    return jsonify(result), 200


@service_bp.route("/api/services/all", methods=["GET"])
def get_all_services():
    """
    Devuelve todos los servicios en formato JSON.
    Returns:
        str: Un objeto JSON que contiene una lista de todos los servicios.
    """
    # Obtiene todos los servicios
    all_services = Service.query.all()

    # Formatea los resultados como un diccionario
    result = {
        "data": [{
            "name": service.name,
            "description": service.description,
            "laboratory": service.institution.name,  # Añade aquí la información correspondiente
            "keywords": service.keywords,
            "enabled": service.enabled,
            "id": service.id,
            "type": service.service_type,
        } for service in all_services],
        "total": len(all_services)
    }

    return jsonify(result), 200


@service_bp.route("/api/services/<int:id>", methods=["GET"])
def get_service(id):
    """
    Obtiene los detalles de un servicio específico y lo devuelve como JSON.
    Args:
        id (int): El ID del servicio que se desea obtener.
    Returns:
        str: Un objeto JSON que contiene los detalles del servicio, o un mensaje de error si no se encuentra el servicio.
    Requires:
        - El usuario debe estar autenticado con un token JWT válido.
    """
    # Busca el servicio en la base de datos por su ID
    service = Service.query.get(id)

    if service:
        # Construye el JSON de respuesta con los detalles del servicio
        service_details = {
            "name": service.name,
            "description": service.description,
            "laboratory": service.institution_id,  # Aquí debes proporcionar la información del laboratorio
            "keywords": service.keywords,
            "enabled": service.enabled
        }

        return jsonify(service_details), 200
    else:
        # Si no se encuentra el servicio, devuelve un error 404 o un mensaje de error apropiado
        return jsonify({"error": "Servicio no encontrado"}), 404


@service_bp.route("/api/services-types", methods=["GET"])
def get_service_types():
    """
    Obtiene los tipos de servicios disponibles.
    Esta función permite obtener una lista de los tipos de servicios disponibles. Se requiere autenticación con un token JWT.
    Returns:
    - Un JSON que contiene una lista de los tipos de servicios disponibles.    
    Example JSON Response:
    {
        "data": ["Tipo de Servicio 1", "Tipo de Servicio 2", "Tipo de Servicio 3"]
    }
    - Si se produce una excepción, como una validación, devuelve un JSON de error con un código de estado 400 (Solicitud Incorrecta).
    """
    # Trae los servicios que tengo
    service_types = {tipo_servicio.name: tipo_servicio.value for tipo_servicio in TipoServicio}

    # Formatea los tipos de servicios en una respuesta JSON
    response = {
        "data": service_types
    }

    return jsonify(response), 200


@auth.login_required
@service_bp.route("/my_services/<int:id>", methods = ['GET'])
def my_services(id):
    """
    Renderiza una página que muestra los servicios disponibles para un usuario con el rol de 'mantenimiento'.
    Args:
        search_services (str, optional): Término de búsqueda para filtrar los servicios. Si no se proporciona,
        se muestran todos los servicios disponibles para las instituciones asociadas al usuario.
    Returns:
        str: Una representación HTML de la página que lista los servicios.
    Requires:
        - El usuario debe tener el rol de 'mantenimiento'.
    """
    if not auth.has_permits(["serv_index"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    keyword = request.args.get('search_services')
    if keyword:
        services_list = list(filter(lambda serv : serv.institution_id == id, list_services_by_keywords_or_name(keyword)))
    else:
        services_list = list(filter(lambda serv : serv.institution_id == id, list_services()))
    services_list, total_pages, page = pagination(services_list)
    return render_template("services/my_services.html", services = services_list, total_pages=total_pages, current_page=page, institution=id)

@auth.login_required
@service_bp.route("/request", methods=['GET'])
@mantenimiento_required
def service_request():
    """
    Renderiza una página para que un usuario con el rol de 'mantenimiento' pueda crear una solicitud de servicio.
    Returns:
        str: Una representación HTML de la página de creación de solicitud de servicio.
    Requires:
        - El usuario debe estar autenticado.
        - El usuario debe tener el rol de 'mantenimiento'.
    """
    if not auth.has_permits(["req_index"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    institutions = list_institutions()
    user_name = getUserById(session["user"])
    services_list = list(filter(lambda serv: serv.enabled, list_services()))
    return render_template("services/request.html", institutions=institutions, user_name=user_name.name, services_list=services_list)


@auth.login_required
@service_bp.route("/request_creation/<int:serv_id>&<int:user_id>")
@mantenimiento_required
def request_creation(serv_id, user_id):
    """
    Crea una solicitud de servicio y muestra una página de confirmación.
    Args:
        serv_id (int): El ID del servicio para el cual se está creando la solicitud.
        user_id (int): El ID del usuario que está creando la solicitud.
    Returns:
        str: Una representación HTML de la página de confirmación o una redirección a la página de creación de solicitudes.
    Requires:
        - El usuario debe estar autenticado.
        - El usuario debe tener el rol de 'mantenimiento'.
    """
    if not auth.has_permits(["req_new"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    service_request = create_request(service_id=serv_id, user_id=user_id)
    if service_request:
        flash("Se ha creado la solicitud correctamente", "success")
        return render_template("services/request_info.html", request=map_request(service_request))
    flash("No se pudo procesar la solicitud, intente nuevamente", "error")
    return redirect(url_for('services.create_request'))


@auth.login_required
@service_bp.route("/my_requests", methods=['GET'])
@mantenimiento_required
def my_requests():
    """
    Muestra una lista de las solicitudes de servicio realizadas por el usuario autenticado.
    Returns:
        str: Una representación HTML de la lista de solicitudes de servicio.
    Requires:
        El usuario debe estar autenticado y tener el rol de 'mantenimiento'.
    """
    if not auth.has_permits(["req_index"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    request_list = mapper_to_request_data(list_request_by_user_id(session['user']))
    return render_template("services/my_requests.html", request_list = request_list)


@service_bp.route("/api/me/requests", methods=["GET"])
@jwt_required()
def get_user_requests():
    """
    Obtiene el listado de solicitudes de servicio realizadas por el usuario autenticado.
    Args:
        No recibe argumentos directos desde la URL, pero utiliza los parámetros de consulta (query parameters):
            - "page" (int): Número de página actual (por defecto 1).
            - "per_page" (int): Cantidad de solicitudes por página (por defecto 10).
            - "sort" (str): Campo por el cual ordenar las solicitudes (opcional).
            - "order" (str): Orden de clasificación ("asc" para ascendente, "desc" para descendente, por defecto "desc").
    Returns:
        response (dict): Un diccionario con el listado de solicitudes de servicio y detalles de paginación.
            - "data" (list): Una lista de diccionarios, donde cada uno contiene información sobre una solicitud:
                - "service_id" (int): ID del servicio de la solicitud.
                - "creation_date" (str): Fecha de creación en formato "YYYY-MM-DD".
                - "close_date" (str): Fecha de cierre en formato "YYYY-MM-DD" (si está disponible).
                - "status" (int): Estado de la solicitud.
                - "descripcion" (str): Descripción de la solicitud.
            - "page" (int): Número de página actual.
            - "per_page" (int): Cantidad de solicitudes por página.
            - "total" (int): Total de solicitudes de servicio.
    Raises:
        400 (Bad Request): Cuando los parámetros no son válidos.
    """
    try:
        
        page = request.args.get("page", type=int, default=1)
        sort = request.args.get("sort", type=str, default="Fecha de Solicitud")
        order = request.args.get("order", type=str, default="desc")
        fechaInicio = datetime.datetime.strptime(request.args.get("fechaInicio", type=str, default="2020-01-01")+" 23:59:59",  "%Y-%m-%d  %H:%M:%S")
        fechaFin = datetime.datetime.strptime(request.args.get("fechaFin", type=str, default="2029-01-01")+" 23:59:59",  "%Y-%m-%d  %H:%M:%S")
        estado = request.args.get("estado", type=str, default="Todos")

        user_id = get_id_by_user_email(get_jwt_identity())
        
        query = list_request_by_user_id_paginated(user_id)
        
        query = query.filter(db.and_(
            ServiceRequest.inserted_at > fechaInicio,
            ServiceRequest.inserted_at < fechaFin))
        
        if estado != "Todos":
            query = query.filter(ServiceRequest.estado_id == ids_estados[estado])
        
        # Aplicar ordenamiento si se proporciona el parámetro 'sort'
        if sort == "Fecha de Solicitud":
            if order != "desc":
                query = query.order_by(db.asc(ServiceRequest.inserted_at))
            else:
                query = query.order_by(db.desc(ServiceRequest.inserted_at))
        else :
            if order != "desc":
                query = query.order_by(db.asc(ServiceRequest.estado_id))
            else:
                query = query.order_by(db.desc(ServiceRequest.estado_id))
        
            
        # Obtiene la cantidad de elementos por página desde una fuente externa(la base de datos).
        per_page = get_pagination()

        # Pagina los resultados
        pagination = query.paginate(page=page, per_page=per_page)
        
        user_requests = mapper_to_request_data(pagination.items)
        

        response = {
            "data": user_requests,
            "total_pages": pagination.pages,
        }

        return jsonify(response), 200
    
    except Exception as e:
        error_response = {
            "error": f"Error en la indicación de parámetros: {str(e)}"
        }
        return jsonify(error_response), 400



@service_bp.route("/api/me/requests/<int:id>", methods=["GET"])
@jwt_required()
def get_user_request(id):
    """
    Obtiene los detalles de una solicitud de servicio específica realizada por el usuario autenticado.
    Args:
        id (int): El ID de la solicitud de servicio a obtener.
    Returns:
        response (str): Una respuesta JSON que contiene los detalles de la solicitud.
    Raises:
        404 (Not Found): Cuando la solicitud de servicio no se encuentra.
    Requires:
        El usuario debe estar autenticado.
    """
    user_id = get_id_by_user_email(get_jwt_identity())

    service_request = ServiceRequest.query.filter_by(id=id, user_id=user_id).first()

    if service_request:
        response = {
            "creation_date": service_request.inserted_at.strftime("%Y-%m-%d"),
            "update_at": service_request.updated_at.strftime("%Y-%m-%d") if service_request.updated_at else None,
            "status": service_request.estado_id,
            "description": service_request.comment
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Solicitud no encontrada"}), 404
    
@service_bp.route("/api/me/requests", methods=["POST"])
@jwt_required()
def create_user_request():
    """
    Crea una nueva solicitud de servicio realizada por el usuario autenticado.
    Returns:
        response (str): Una respuesta JSON que contiene los detalles de la solicitud creada.
    Raises:
        400 (Bad Request): Cuando los parámetros son inválidos o faltan campos obligatorios.
    Requires:
        El usuario debe estar autenticado.
    """
    try:        
        user_id = get_id_by_user_email(get_jwt_identity())
        request_data = request.get_json()

        required_fields = ["service_id", "user_id","comments"]
        for field in required_fields:
            if field not in request_data:
                return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

        serv_id = request_data["service_id"]
        comments = request_data["comments"]
        service_request = create_request(service_id=serv_id, user_id=user_id,comments=comments)
        

        db.session.add(service_request)
        db.session.commit()

        response = {
            "id": service_request.id,
            "inserted_at": service_request.inserted_at.strftime("%Y-%m-%d"),
            "update_at": service_request.updated_at.strftime("%Y-%m-%d") if service_request.updated_at else None,
            "status": service_request.estado_id,
            "comment": service_request.comment
        }

        return jsonify(response), 201
    except Exception as e:
        error_response = {
            "error": "Faltan campos obligatorios"
        }
        return jsonify(error_response), 400
    
@service_bp.route("/api/me/requests/<int:request_id>/notes", methods=["POST"])
@jwt_required()
def create_request_note(request_id):
    """
    Crea una nota en una solicitud de servicio existente.
    Args:
        request_id (int): El ID de la solicitud de servicio a la cual se agrega la nota.
    Returns:
        response (str): Una respuesta JSON que contiene la nota creada.
    Raises:
        400 (Bad Request): Cuando los parámetros son inválidos o faltan campos obligatorios.
        404 (Not Found): Cuando la solicitud de servicio no se encuentra.
    Requires:
        El usuario debe estar autenticado.
    """
    request_data = request.get_json()
    if "text" not in request_data:
        return jsonify({"error": "El campo 'text' es obligatorio"}), 400
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Solicitud de servicio no encontrada"}), 404
    new_note = request_data["text"]
    if service_request.comment:
        service_request.comment += f"\n{new_note}"
    else:
        service_request.comment = new_note
    db.session.commit()
    response = {
        "id": request_id,
        "text": new_note,
    }
    return jsonify(response), 201
    
@auth.login_required
@service_bp.route("/requested/<int:id>", methods = ['GET'])
@mantenimiento_required
def requested(id):
    """
    Renderiza una página que muestra los servicios disponibles para un usuario con el rol de 'mantenimiento'.

    Args:
        search_services (str, optional): Término de búsqueda para filtrar los servicios. Si no se proporciona,
        se muestran todos los servicios disponibles para las instituciones asociadas al usuario.

    Returns:
        str: Una representación HTML de la página que lista los servicios.

    Requires:
        - El usuario debe tener el rol de 'mantenimiento'.
    """
    if not auth.has_permits(["req_index"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    requested_list = mapper_to_request_data(list_request_by_institution(id))
    requested_list, total_pages, page = pagination(requested_list)
    return render_template("services/requested.html", requested = requested_list, total_pages=total_pages, current_page=page, institution=id)

@auth.login_required
@service_bp.get("/request_info/<int:id>")
@mantenimiento_required
def request_info(id):
    if not auth.has_permits(["req_show"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    a_request = map_request(search_request(id))
    estados = list_estados()
    return render_template("services/request_info.html", request = a_request, estados = estados)

@auth.login_required
@service_bp.post("/request_info/<int:id><int:flag_status>")
@mantenimiento_required
def request_info_update(id, flag_status):
    if not auth.has_permits(["req_show"]):  
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")         
        return redirect(url_for("home.index"))
    
    if flag_status:
        status = request.form.get("status")
        switch_status(id, status)
    else:
        comment = request.form.get('add_comment')
        if comment:
            add_comment(comment, id)
    a_request = map_request(search_request(id))
    estados = list_estados()
    return render_template("services/request_info.html", request = a_request, estados = estados)

@service_bp.route("/api/requests-states", methods=["GET"])
def get_requests_states():
    """
    Obtiene los estados de solicitud disponibles.
    Esta función permite obtener una lista de los estados de solicitud disponibles.
    Returns:
    - Un JSON que contiene una lista de losestados de solicitud disponibles.    
    Example JSON Response:
    {
        "data": ["Pendiente", "Aceptado", "Cancelado"]
    }
    - Si se produce una excepción, como una validación, devuelve un JSON de error con un código de estado 400 (Solicitud Incorrecta).
    """
    estados = [ est.name for est in list_estados()]

    response = {
        "data": estados
    }

    return jsonify(response), 200

@service_bp.route("/api/me/requestsWithFilter", methods=["GET"])
@jwt_required()
def get_user_requests_with_filter():
    """
    Obtiene el listado de solicitudes de servicio realizadas por el usuario autenticado.
    Args:
        No recibe argumentos directos desde la URL, pero utiliza los parámetros de consulta (query parameters):
            - "page" (int): Número de página actual (por defecto 1).
            - "per_page" (int): Cantidad de solicitudes por página (por defecto 10).
            - "estado" (string) : estado de la solicitud,
            - "fechaInicio" (string): fecha de inicio para el filtro,
            - "fechaFin": feecha de fin para el filtro,
    Returns:
        response (dict): Un diccionario con el listado de solicitudes de servicio y detalles de paginación.
            - "data" (list): Una lista de diccionarios, donde cada uno contiene información sobre una solicitud:
                - "service_id" (int): ID del servicio de la solicitud.
                - "creation_date" (str): Fecha de creación en formato "YYYY-MM-DD".
                - "close_date" (str): Fecha de cierre en formato "YYYY-MM-DD" (si está disponible).
                - "status" (int): Estado de la solicitud.
                - "descripcion" (str): Descripción de la solicitud.
            - "page" (int): Número de página actual.
            - "per_page" (int): Cantidad de solicitudes por página.
            - "total" (int): Total de solicitudes de servicio.
    Raises:
        400 (Bad Request): Cuando los parámetros no son válidos.
    """
    try:
        page = request.args.get("page", type=int, default=1)
        per_page = request.args.get("per_page", type=int, default=10)
        sort = request.args.get("sort", type=str)
        order = request.args.get("order", type=str, default="desc")
        fechaInicio = datetime.datetime.strptime(request.args.get("fechaInicio", type=str, default="2020-01-01")+" 23:59:59",  "%Y-%m-%d  %H:%M:%S")
        fechaFin = datetime.datetime.strptime(request.args.get("fechaFin", type=str, default="2029-01-01")+" 23:59:59",  "%Y-%m-%d  %H:%M:%S")
        estado = request.args.get("estado", type=str, default="Todos")
        
        user_id = get_id_by_user_email(get_jwt_identity())
        
        user_requests = mapper_to_request_data(list_request_by_user_id(user_id))
        
        user_requests = list(
            filter( 
                lambda req: fechaInicio <= datetime.datetime.strptime(req["requested"], "%d-%m-%Y %H:%M:%S") <= fechaFin,
                user_requests
            )
        )
        
        if estado != "Todos":
            user_requests = list(
                filter( 
                    lambda req : req["status"] == estado,
                    user_requests
                )
            )
        
        if sort:
            reverse_order = order == "desc"
            user_requests.sort(key=lambda x: getattr(x, sort, ''), reverse=reverse_order)

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        current_page_requests = user_requests[start_index:end_index]

        response_data = []
        
        
        for request_data in current_page_requests:
            response_data.append(request_data)

        response = {
            "data": response_data,
            "page": page,
            "per_page": per_page,
            "total": len(user_requests)
        }

        return jsonify(response), 200
    
    except Exception as e:
        error_response = {
            "error": f"Error en la indicación de parámetros: {str(e)}"
        }
        return jsonify(error_response), 400
    

@service_bp.route("/top-requested-services", methods=["GET"])
def top_requested_services():
    """
    Obtiene los servicios más solicitados.

    Endpoint: /top-requested-services
    Método HTTP: GET

    Devuelve un JSON con los servicios más solicitados y la cantidad de solicitudes para cada uno.

    Formato de respuesta JSON:
    {
        "success": True,
        "data": [
            {
                "name": str,          # Nombre del servicio
                "institution_name": str,  # Nombre de la institución a la que pertenece el servicio
                "request_count": int  # Cantidad de solicitudes para el servicio
            },
            ...
        ]
    }

    Códigos de estado HTTP:
    - 200 OK: La solicitud se completó con éxito.

    Ejemplo de uso:
    GET http://direccion_del_servidor/top-requested-services

    Respuesta JSON:
    {
        "success": True,
        "data": [
            {"name": "Servicio1", "institution_name": "Institución1", "request_count": 10},
            {"name": "Servicio2", "institution_name": "Institución2", "request_count": 8},
            ...
        ]
    }
    """
    top_services = (
        db.session.query(Service, Institution, db.func.count(ServiceRequest.id).label('request_count'))
        .join(ServiceRequest)
        .join(Institution)
        .group_by(Service, Institution)
        .order_by(db.desc('request_count'))
        .limit(10)
        .all()
    )

    result = []
    for service, institution, request_count in top_services:
        result.append({
            "name": service.name,
            "institution_name": institution.name,
            "request_count": request_count
        })

    return jsonify({"success": True, "data": result})

    

@service_bp.route("/request_per_state", methods=["GET"])
def request_per_state():
    """
Obtiene la cantidad de solicitudes de servicio por estado.

Endpoint: /request_per_state
Método HTTP: GET

Devuelve un JSON con la cantidad de solicitudes para cada estado.

Formato de respuesta JSON:
{
    "Estado1": cantidad1,
    "Estado2": cantidad2,
    ...
}

Códigos de estado HTTP:
- 200 OK: La solicitud se completó con éxito.

Ejemplo de uso:
GET http://direccion_del_servidor/request_per_state
"""
    states = Estado.query.all()
    result = {}

    for state in states:
        state_name = state.name
        count = ServiceRequest.query.filter_by(estado_id=state.id).count()
        result[state_name] = count

    return jsonify(result), 200
    
@service_bp.post("/api/request_comment")
@jwt_required()
def request_info_update_api():
    """
    Actualiza la información de una solicitud de servicio, incluyendo la adición de comentarios.

    Endpoint: /api/request_comment
    Método HTTP: POST

    Parámetros de entrada (en el cuerpo de la solicitud):
    {
        "params": {
            "request_id": int,  # ID de la solicitud a actualizar
            "add_comment": str  # Comentario a añadir a la solicitud
        }
    }

    Códigos de estado HTTP:
    - 200 OK: La solicitud se completó con éxito.

    Ejemplo de uso:
    POST http://direccion_del_servidor/api/request_comment
    Cuerpo de la solicitud:
    {
        "params": {
            "request_id": 123,
            "add_comment": "Este es un comentario adicional."
        }
    }

    Respuesta JSON:
    {
        "data": {
            "request_id": int,         # ID de la solicitud actualizada
            "other_request_data": ...  # Otros datos actualizados de la solicitud
        }
    }
    """
    try:        
            user_id = get_id_by_user_email(get_jwt_identity())
            request_data = request.get_json()["params"]
        

            required_fields = ["request_id", "add_comment"]
            for field in required_fields:
                if field not in request_data:
                    return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

            request_id = request_data['request_id']
            comment = request_data['add_comment']
            
            
            if request_id not in [ req.id for req in list_request_by_user_id(user_id)]:
                return jsonify({"error": f"La solicitud no corresponde al usuario autenticado "}), 400
            
            if not search_request(request_id):
                return jsonify({"error": f"El ID de la solicitud no corresponde al una solicitud registrada en la base de datos"}), 400
            
            add_comment(comment, request_id)
            
            a_request = map_request(search_request(request_id))

            response = {
                "data": a_request
            }

            return jsonify(response), 200
    except Exception as e:
        error_response = {
            "error": "Faltan campos obligatorios"
        }
        return jsonify(error_response), 400