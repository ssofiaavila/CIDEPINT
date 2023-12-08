from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import render_template, jsonify
from src.core.model.servicio.servicio import Service
from src.core.model.request.service_request import ServiceRequest
from src.web.controllers.home import mantenimiento_required
from src.core.model.institucion import update_days,get_institution_by_name, list_institution_by_keywords_or_name, load_dict, list_institutions, delete, update_institution, create_institution, get_institution_by_id
from src.core.model.days_hours import create_days_hour
from src.core.model.institucion.institucion import Institution
from src.core.model.days_hours.days_hours import DiasHorarios, FranjaHoraria, Dias
from src.core.database import db
from src.core.model.servicio import list_services_institution_id
from src.web.helpers import auth
from src.web.helpers.validations import only_numbers, institution_name, is_valid_url, is_valid_email, validate_form
from src.web.helpers.geocodificacion import geocodificacion, get_coord_from_link
from src.core import pagination
from src.web.forms.forms import CreateInstitutionForm
from flask_jwt_extended import jwt_required
from src.core.model.institucion import get_all_services, get_top_institutions


institution_bp = Blueprint("institutions", __name__, url_prefix="/institutions")

@institution_bp.route("/", methods=["GET"])
@mantenimiento_required
def index():
    """
    Muestra una lista de instituciones con opciones de búsqueda y paginación
    Esta vista es accesible solo para usuarios autenticados con permisos de mantenimiento. Muestra una lista de instituciones
    disponibles en el sistema, permitiendo a los usuarios buscar instituciones específicas por nombre o palabra clave y
    paginar a través de los resultados.
    Args:
        None
    Returns:
        render_template: Una plantilla HTML que muestra la lista de instituciones y opciones de búsqueda y paginación.
    Requiere:
        - El usuario debe estar autenticado.
        - El usuario debe tener permisos de mantenimiento para acceder a esta vista.
    """
    
    if not auth.has_permits(["inst_index"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    
    keyword = request.args.get('search_institution')
    if keyword:
        institutions = list(filter(lambda insti : insti.id > 2, list_institution_by_keywords_or_name(keyword)))
    else:
        institutions = list(filter(lambda insti : insti.id > 2, list_institutions()))

    institutions, total_pages, page = pagination(institutions)
    return render_template("institutions/index.html", institutions=institutions, total_pages=total_pages, current_page=page)


@auth.login_required
@institution_bp.route("/modify/<int:id>", methods=['GET', 'POST'])
@mantenimiento_required
def modify_institution(id):
    """
    Modifica una institución existente con la información proporcionada en el formulario.
    Esta vista permite a los usuarios con permisos de mantenimiento modificar una institución existente en el sistema.
    Los usuarios pueden editar detalles como información general, dirección, ubicación, sitio web, palabras clave,
    número de teléfono, información de contacto y horario de atención. Además, los usuarios pueden seleccionar los días
    de atención y franjas horarias para la institución.
    Args:
        id (int): El ID único de la institución que se va a modificar.
    Returns:
        render_template: Una plantilla HTML para modificar la institución.        
    Requiere:
        - El usuario debe estar autenticado.
        - El usuario debe tener permisos de mantenimiento.
    """
        
    institution = Institution.query.get(id)
    form = CreateInstitutionForm(obj=institution)

    if form.validate_on_submit():
        form.populate_obj(institution)
        db.session.commit()
        selected_days = register_days(request.form)
        selected_time_slots = decide_stripe(request.form.get("franja"))

        update_days(institution.id, selected_days, selected_time_slots)
         
        flash('La institución se ha modificado exitosamente', 'success')
        return redirect(url_for('institutions.index'))
    return render_template("institutions/modify.html", form=form, institution=institution)

@institution_bp.route("/info/<int:id>")
@mantenimiento_required
def info_institution(id):
    """
    Muestra información detallada de una institución seleccionada.
    Esta vista muestra detalles completos de una institución seleccionada, incluyendo su información general,
    servicios relacionados, horario de atención y días de servicio.
    Args:
        id (int): El ID único de la institución que se va a mostrar.
    Returns:
        render_template: Una plantilla HTML que muestra la información de la institución.
    Requiere:
        - El usuario debe tener permisos de mantenimiento.
    """
    if not auth.has_permits(["inst_show"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
                        
    institution = Institution.query.get(id)
    services_list = list(filter(lambda serv : serv.enabled, list_services_institution_id(id)))
    selected_day_names = Dias.get_selected_day_names(id)
    selected_time_slots = FranjaHoraria.get_franja_name_by_institution_id(id)
    selected_time_slots = decide_stripe_name(selected_time_slots)
    return render_template("institutions/info.html", inst=institution, 
                           services=services_list, selected_day_names=selected_day_names,
                           selected_time_slots=selected_time_slots)

@auth.login_required
@institution_bp.route("/delete/<int:id>",methods=['GET','POST'])
@mantenimiento_required
def delete_institution(id):
    """
    Elimina una institución y sus dependencias.
    Esta vista permite a los usuarios autorizados eliminar una institución y todas sus dependencias, incluyendo servicios relacionados,
    horarios de atención y días de servicio.
    Args:
        id (int): El ID único de la institución que se va a eliminar.
    Returns:
        render_template: Una plantilla HTML que muestra la confirmación de eliminación.
    Requiere:
        - El usuario debe estar autenticado.
        - El usuario debe tener permisos de mantenimiento.
    Se elimina la institución y todas sus dependencias, incluyendo servicios relacionados, horarios de atención y días de servicio.
    """
    
    if not auth.has_permits(["inst_destroy"]):
        flash("El usuario no cuenta con los permisos para acceder a este recurso","error")
        return redirect(url_for("home.index"))
    
    institution = Institution.query.get(id)
    if request.method == "POST":
        if delete(institution.id):
            flash('La institución se ha eliminado exitosamente', 'success')
            return redirect(url_for('institutions.index'))
        flash('La institucion no se pudo eliminar', 'error')
        return redirect(url_for('institutions.index'))
    return render_template("institutions/delete.html", inst=institution)

@auth.login_required
@mantenimiento_required
@institution_bp.route("/create",methods=['GET','POST'])
def create():
    """
    Crea una institución y valida los datos según las pautas proporcionadas.
    Esta vista permite a los usuarios autorizados crear una nueva institución. Los datos ingresados son validados para
    asegurar que cumplen con los requisitos, como campos obligatorios, formatos de teléfono, dirección web válida, entre otros.
    Args:
        No se requieren argumentos.
    Returns:
        render_template: Una plantilla HTML que muestra el formulario de creación o la confirmación de creación.
    Requiere:
        - El usuario debe estar autenticado.
        - El usuario debe tener permisos de mantenimiento.
    Si se reciben datos del formulario de creación, se validan y se crea la institución. Además, se registran los días y horarios de atención.
    """
    if request.method == 'POST':
        form = CreateInstitutionForm(request.form)
        if form.validate():
            # Obtener los datos del formulario
            name = form.name.data
            info = form.info.data
            address = form.address.data
            web = form.web.data
            keywords = form.keywords.data
            phone = form.phone.data
            contact_info = form.contact_info.data
            enabled = form.enabled.data
            
            # Crea un diccionario con los datos para pasar a create_institution
            institution_data = {
                'name': name,
                'info': info,
                'address': address,
                'web': web,
                'keywords': keywords,
                'phone': phone,
                'contact_info': contact_info,
                'enabled': enabled,
            }

            print(f"Datos: {institution_data}")

            # Llama a la función create_institution para crear la institución
            institution_data['location'] = geocodificacion(institution_data['address'])
            new_institution = create_institution(**institution_data)


            if new_institution:
                kwargs_days = register_days(request.form)
                id_franja   = decide_stripe(request.form.get("franja"))
                institution = get_institution_by_name(institution_data['name'])
                create_days_hour(institution.id,id_franja,**kwargs_days)
                flash('La institución se ha creado exitosamente', 'success')
                return redirect(url_for('institutions.index'))  
            else:
                flash('Hubo un error al crear la institución debido a un nombre duplicado u otro problema.', 'error')
        else:
            flash('Hubo errores en el formulario. Por favor, corrige los errores y vuelve a intentar.', 'error')
    else:
        form = CreateInstitutionForm()

    return render_template('institutions/create.html', form=form)


def register_days(registers):
    """
    Registra los días de la semana en los que una institución proporcionará servicios.
    Esta función toma un objeto `registers` que generalmente proviene de un formulario web y verifica qué días de la semana
    se han seleccionado para la prestación de servicios. Los días se representan como un diccionario de días de la semana con valores
    booleanos que indican si están seleccionados o no.
    Args:
        registers (MultiDict): Un objeto que generalmente contiene datos de un formulario web.
    Returns:
        dict: Un diccionario que representa los días de la semana y sus estados (seleccionados o no).
    Ejemplo:
        Si el formulario web proporciona "lunes" y "miércoles" como días seleccionados, la función devolverá:
        {
            "lunes": True,
            "martes": False,
            "miércoles": True,
            "jueves": False,
            "viernes": False,
            "sábado": False,
            "domingo": False
        }
    """
    dias_semana = {
        "lunes": False,
        "martes": False,
        "miercoles": False,
        "jueves": False,
        "viernes": False,
        "sabado": False,
        "domingo": False
    }
    for dia in dias_semana:
        dias_semana[dia] = True if dia in registers.getlist("days") else False
    return dias_semana

def decide_stripe(valor):
    """
    Decide la franja horaria según el valor proporcionado.
    Esta función toma un valor y determina la franja horaria correspondiente. Los valores pueden ser "manana" para la franja de la mañana,
    "tarde" para la franja de la tarde, "ambos" para ambas franjas o cualquier otro valor. Devuelve un código numérico para representar la franja
    horaria.
    Args:
        valor (str): El valor que indica la franja horaria.
    Returns:
        int: Un valor numérico que representa la franja horaria:
            - 1 para "manana"
            - 2 para "tarde"
            - 3 para "ambos"
            - False si el valor no coincide con ninguna franja horaria conocida.
    Ejemplo:
        Si el valor es "manana", la función devolverá 1 para representar la franja de la mañana.
    """
    if valor == "manana":
        return 1
    elif valor == "tarde":
        return 2
    elif valor == "ambos":
        return 3
    return False

@institution_bp.route('/api/institutions', methods=['GET'])
@jwt_required()
def get_institutions():
    """
    Obtiene la lista de instituciones.

    Esta función implementa el endpoint '/api/institutions' para obtener una lista de todas las instituciones registradas
    en la base de datos.

    Returns:
        JSON: Un objeto JSON que contiene la lista de instituciones con los siguientes campos para cada institución:
            - name: Nombre de la institución.
            - information: Información general sobre la institución.
            - address: Dirección de la institución.
            - location: Ubicación de la institución.
            - web: Sitio web de la institución.
            - keywords: Palabras clave asociadas a la institución.
            - contact_info: Información de contacto de la institución.
            - enabled: Estado de habilitación de la institución (activo o inactivo).

        Ejemplo:
        {
            "data": [
                {
                    "name": "Institución A",
                    "information": "Información sobre la Institución A.",
                    "address": "Dirección de la Institución A",
                    "location": "Ubicación A",
                    "web": "https://www.institucionA.com",
                    "keywords": "educación, investigación, ciencia",
                    "contact_info": "info@institucionA.com",
                    "enabled": true
                },
                {
                    "name": "Institución B",
                    "information": "Información sobre la Institución B.",
                    "address": "Dirección de la Institución B",
                    "location": "Ubicación B",
                    "web": "https://www.institucionB.com",
                    "keywords": "salud, bienestar",
                    "contact_info": "info@institucionB.com",
                    "enabled": true
                }
            ],
            "page": 1,  # Página actual (puede ser ajustada si se implementa la paginación)
            "per_page": 2,  # Número de instituciones por página
            "total": 2  # Total de instituciones en la lista
        }
    """
    institutions = Institution.query.all()

    institutions_list = []
    for institution in institutions:
        institution_data = {
            "name": institution.name,
            "information": institution.info,
            "address": institution.address,
            "location": institution.location,
            "web": institution.web,
            "keywords": institution.keywords,
            "contact_info": institution.contact_info,
            "enabled": institution.enabled,
        }
        institutions_list.append(institution_data)

    response = {
        "data": institutions_list,
        "page": 1,  
        "per_page": len(institutions),  
        "total": len(institutions),  
    }
    return jsonify(response)



@institution_bp.route('/api/servicesList', methods=['GET'])
def services():
    services = get_all_services()
    return jsonify(services)



def decide_stripe_name(valor):
    """
    Convierte un valor numérico de franja horaria en su nombre correspondiente.
    Esta función recibe un valor numérico de franja horaria y lo convierte en su nombre correspondiente. 
    El valor numérico 1 representa la franja de "mañana", el valor numérico 2 representa la franja de "tarde", 
    y el valor numérico 3 representa "ambos".
    Args:
        valor (int): El valor numérico de franja horaria (1, 2 o 3).
    Returns:
        str: El nombre de la franja horaria correspondiente.    
    """
    if '1' in valor:
        valor = FranjaHoraria.get_name(1)
    elif '2' in valor:
        valor = FranjaHoraria.get_name(2)
    elif '3' in valor:
        valor = FranjaHoraria.get_name(3) 
    return valor


@institution_bp.route('/api/institution/<int:id>', methods=['GET'])
def get_institution_details(id):
    """
    Obtiene la información de una institución.

    Esta función implementa el endpoint '/api/institutions/<int:id>' para obtener la información de una institución
    específica.

    Args:
        id (int): El ID único de la institución que se va a obtener.
        Returns: 
            JSON: Un objeto JSON que contiene la información de la institución con los siguientes campos:
                - name: Nombre de la institución.
                - information: Información general sobre la institución.
                - address: Dirección de la institución.
                - location: Ubicación de la institución.
                - web: Sitio web de la institución.
                - keywords: Palabras clave asociadas a la institución.
                - contact_info: Información de contacto de la institución.
        Ejemplo:
        {
            "data": {
                "name": "Institución A",
                "information": "Información sobre la Institución A.",
                "address": "Dirección de la Institución A",
                "location": "Ubicación A",
                "web": "https://www.institucionA.com",
                "keywords": "educación, investigación, ciencia",
                "contact_info": "info@institucionA.com"
    """

    institution = get_institution_by_id(id)
    if institution:
        institution_data = {
            "name": institution.name,
            "information": institution.info,
            "address": institution.address,
            "location": get_coord_from_link(institution.location),
            "web": institution.web,
            "keywords": institution.keywords,
            "contact_info": institution.contact_info
        }

        return jsonify(institution_data), 200
    else:
        return jsonify({"error": "Institución no encontrada"}), 404
    


@institution_bp.route("/top-institutions", methods=["GET"])
def top_institutions():
    """
    Obtiene las 10 instituciones con mayor cantidad de solicitudes de servicio.

    Endpoint: /top-institutions
    Método HTTP: GET

    Devuelve un JSON con las 10 instituciones principales y la cantidad de solicitudes de servicio para cada una.

    Formato de respuesta JSON:
    [
        {
            "name": str,          # Nombre de la institución
            "request_count": int  # Cantidad de solicitudes de servicio para la institución
        },
        ...
    ]

    Códigos de estado HTTP:
    - 200 OK: La solicitud se completó con éxito.

    Ejemplo de uso:
    GET http://direccion_del_servidor/top-institutions

    Respuesta JSON:
    [
        {"name": "Institucion1", "request_count": 15},
        {"name": "Institucion2", "request_count": 12},
        ...
    ]
    """
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

    result = []
    for institution, request_count in top_institutions:
        result.append({
            "name": institution.name,
            "request_count": request_count
        })

    return jsonify(result)