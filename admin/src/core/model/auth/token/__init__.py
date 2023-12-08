from src.core.model.auth.token.token import Token
from src.core.database import db


def create_token(**kwargs):
    """
    Crea un nuevo objeto Token y lo guarda en la base de datos.
    Args:
    **kwargs: Argumentos clave-valor que representan los atributos del objeto Token.
    Returns:
    Token: El objeto Token recién creado y guardado en la base de datos.
    """
    token = Token(**kwargs)
    db.session.add(token)
    db.session.commit()
    return token

def find_unique_token(token):
    """
    Busca un token único en la base de datos.
    Args:
    token (str): El token que se va a buscar en la base de datos.
    Returns:
    Token: El objeto Token correspondiente al token buscado, o None si no se encuentra.
    Example:
    token = find_unique_token("random_token")
    if token:
        print(f"Token encontrado: {token.token}")
    else:
        print("Token no encontrado.")
    """
    return Token.query.filter_by(token=token).first()