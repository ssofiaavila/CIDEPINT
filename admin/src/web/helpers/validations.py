from src.core.model.institucion import get_institution_by_name
import re
from src.core.model.servicio.servicio import TipoServicio

def only_numbers(cadena):
    """
    Comprueba si una cadena contiene solo dígitos.

    Args:
    cadena (str): La cadena que se va a verificar.

    Returns:
    bool: True si la cadena contiene solo dígitos, False en caso contrario.
    """
    return cadena.isdigit()

def institution_name(cadena):
    """
    Comprueba si una cadena es un nombre de institución válido que puede contener letras, espacios, comas, puntos, guiones, signos de exclamación y signos de interrogación.

    Esta función verifica si la cadena cumple con un patrón que permite letras, espacios, comas, puntos, guiones, signos de exclamación y signos de interrogación en un nombre de institución.

    Args:
    cadena (str): La cadena que se va a verificar.

    Returns:
    bool: True si la cadena es un nombre de institución válido, False en caso contrario.
    """
    patron = r'^[a-zA-Z0-9\s.,\-!?]*$'
    return re.match(patron, cadena) is not None


def is_valid_url(url):
    """
    Comprueba si una cadena es una URL válida.

    Esta función verifica si la cadena comienza con "http://" o "https://", lo que indica una URL válida.

    Args:
    url (str): La cadena que se va a verificar como URL.

    Returns:
    bool: True si la cadena es una URL válida, False en caso contrario.
    """
    return re.match(r'^(http|https)://', url) is not None

def is_valid_email(email):
    """
    Comprueba si una cadena es una dirección de correo electrónico válida.

    Esta función verifica si la cadena cumple con un patrón que corresponde a una dirección de correo electrónico válida.

    Args:
    email (str): La cadena que se va a verificar como dirección de correo electrónico.

    Returns:
    bool: True si la cadena es una dirección de correo electrónico válida, False en caso contrario.
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def is_gmail_domain(email):
    """
    Comprueba si una cadena es una dirección de correo electrónico pertenece al dominio de @gmail.com 

    Esta función verifica si la cadena cumple con un patrón que corresponde a una dirección de correo electrónico válida.

    Args:
    email (str): La cadena que se va a verificar como dirección de correo electrónico.

    Returns:
    bool: True si la cadena es una dirección de correo electrónico válida, False en caso contrario.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@gmail\.com$"
    return re.match(pattern, email) is not None

def is_valid_name(cadena):
    """
    Comprueba si una cadena contiene solo letras (mayúsculas o minúsculas) y espacios.

    Esta función verifica si la cadena contiene solo caracteres alfabéticos y espacios. Los números, comas, puntos, guiones u otros caracteres no son permitidos.

    Args:
    cadena (str): La cadena que se va a verificar.

    Returns:
    bool: True si la cadena contiene solo letras y espacios, False en caso contrario.
    """
    patron = r'^[a-zA-Z\s]*$'
    return re.match(patron, cadena) is not None



def validate_form(request, kwargs_result, is_update=False):
    errors = []
    required_fields = ["name", "info", "address", "web", "keywords", "phone", "contact_info"]

    for field in required_fields:
        if field in request.form and not request.form.get(field).strip() :
            errors.append(f"El campo {field} no puede ser un blanco.")
        elif not request.form.get(field):
            errors.append(f"El campo {field} es obligatorio.")

    if not only_numbers(kwargs_result["phone"]):
        errors.append('Número de teléfono no válido')       

    if not is_valid_url(kwargs_result["web"]):
        errors.append('Direccion web no valida')

    if not institution_name(kwargs_result["name"]):
        errors.append('Nombre de institución no válido')
    else:
        if not is_update and get_institution_by_name(kwargs_result["name"]):
            errors.append('Nombre de institucion repetido')
            

    if not any(request.form.getlist("days")):
        errors.append('Debe seleccionar al menos un día de atención.')

    if "franja" not in request.form:
        errors.append('Debe seleccionar una franja horaria.')

    if not is_valid_email(request.form['contact_info']):
        errors.append('El E-MAIL ingresado en información de contacto es invalido.')
    
    return errors


def validate_maintence(request):
    errors = []
    required_fields = ["message_info","contact"]
    for field in required_fields:
        if field in request.form and not request.form.get(field).strip() :
            errors.append(f"El campo {field} no puede ser un blanco.")
        elif not request.form.get(field):
            errors.append(f"El campo {field} es obligatorio.")
    return errors
    
def is_valid_service_type(service_type):
    """
    Comprueba si una cadena es un tipo de servicio válido que puede contener letras, espacios, comas, puntos, guiones, signos de exclamación y signos de interrogación.

    Esta función verifica si la cadena cumple con un patrón que permite letras, espacios, comas, puntos, guiones, signos de exclamación y signos de interrogación en un tipo de servicio.

    Args:
    service_type (str): La cadena que se va a verificar.

    Returns:
    bool: True si la cadena es un tipo de servicio válido, False en caso contrario.
    """
    return service_type in TipoServicio.__members__

def is_valid_search_term(search_term):
    """
    Esta función verifica si la cadena contiene solo caracteres alfabéticos, numéricos, guiones medios, guiones bajos, p
    arentesis, espacios, comas y puntos. 

    Args:
    desc (str): La cadena que se va a verificar.

    Returns:
    bool: True si la cadena contiene solo caracteres alfabéticos, numéricos, guiones medios, guiones bajos, parentesis, espacios, comas y puntos. 
    """
    patron = r'^[a-zA-Z0-9 _(),.-]+$'
    return re.match(patron, search_term)