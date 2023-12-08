from src.core.model.auth.rol.role import Role
from src.core.database import db
from src.core.model.combined_tables.user_has_role import User_has_role
from src.core.model.combined_tables.role_has_permit import Role_has_permit
from src.core.model.auth import permiso
from src.core.model.institucion import get_institution_by_id
from src.core.model.auth.rol import get_rol_by_id


def list_relationships():
    """
    Obtiene una lista de relaciones entre usuarios, instituciones y roles.
    Returns:
    list: Una lista de objetos de relación entre usuarios, instituciones y roles.
    """
    user_institution_role_relation_list = User_has_role.query.all() 
    return user_institution_role_relation_list

def assign_relation_user_role_institution(**kwargs):
    """
    Asigna una relación entre un usuario, una institución y un rol.
    Args:
    **kwargs: Diccionario de argumentos que incluyen user_id, institution_id y role_id.
    Returns:
    User_has_role: El objeto de relación entre usuario, institución y rol creado.
    """
    
    user_has_role = User_has_role(**kwargs)
    db.session.add(user_has_role)
    db.session.commit()
    return user_has_role

def assign_permit_to_rol(**kwargs):
    """
    Asigna un permiso a un rol específico.
    Args:
    **kwargs: Diccionario de argumentos que incluyen role_id y permit_id.
    Returns:
    Role_has_permit: El objeto de relación entre rol y permiso creado.
    """
    role_has_permit = Role_has_permit(**kwargs)
    db.session.add(role_has_permit)
    db.session.commit()
    return role_has_permit


def list_permits_by_user_id(id):
    """
    Obtiene una lista de nombres de permisos asignados a un usuario por su ID.
    Args:
    id (int): El ID del usuario.
    Returns:
    list: Una lista de nombres de permisos asignados al usuario o None si no se encontraron permisos.
    """
    user_has_role = User_has_role.query.filter_by(user_id=id).first()
    # print(user_has_role)
    if user_has_role:
        role_has_permit_list = Role_has_permit.query.filter_by(role_id=user_has_role.role_id).all()
        if role_has_permit_list:
            permit_names_list = [ permiso.list_permits_by_id(permit.permit_id).name for permit in role_has_permit_list]
            return permit_names_list
    else:
        return None
    
def get_institutions_by_user_id(user_id):
    """
    Obtiene una lista de instituciones asignadas a un usuario por su ID.
    Args:
    user_id (int): El ID del usuario.
    Returns:
    list: Una lista de instituciones asignadas al usuario o None si no se encontraron instituciones.
    """
    user_has_role = User_has_role.query.filter_by(user_id=user_id)
    if user_has_role:
        institutions = [get_institution_by_id(row.institution_id) for row in user_has_role]
        return institutions
    else:
        return None
    
def get_user_rol(id):
    """
    Obtiene el rol de un usuario por su ID.
    Args:
    id (int): El ID del usuario.
    Returns:
    Role or None: El rol del usuario o None si no se encontró ningún rol asignado.
    """
     # Realiza una consulta para obtener el rol de un usuario por su ID
    user_has_role = (
        db.session.query(User_has_role)
        .filter(User_has_role.user_id == id)
        .first()  # Usamos .first() en lugar de .all() para obtener solo un registro
    )
    # Ahora puedes acceder al rol del usuario desde user_role
    if user_has_role:
        rol = get_rol_by_id(user_has_role.role_id)
        return rol
    else:
        return None  # Si el usuario no tiene roles asignados, devolvemos None
    
def update_role(user_id, new_role_id, selected_institutions_ids):
    """
    Actualiza el rol de un usuario en una o varias instituciones.
    Args:
    user_id (int): El ID del usuario cuyo rol se actualizará.
    new_role_id (int): El nuevo ID de rol que se asignará al usuario.
    selected_institutions_ids (list): Una lista de IDs de instituciones a las que se asignará el nuevo rol.
    Returns:
    bool: True si la actualización fue exitosa, False si ocurrió un error.
    """
    try:
        
        for inst_id in selected_institutions_ids:
            tupla = get_relation_user_institution(user_id, inst_id)
            if tupla:
                tupla.role_id = new_role_id
            else:
                assign_relation_user_role_institution(user_id=user_id, institution_id=inst_id, role_id=new_role_id )
            db.session.commit()
        eliminar_relacion_institucion_default(user_id)
   
        return  True
    except Exception as e:
        db.session.rollback()
        return False  # Ocurrió un error al actualizar el rol
    
def list_roles():
    """
    Obtiene una lista de todos los roles disponibles en la base de datos.
    Returns:
    list: Una lista de objetos de tipo Role que representan los roles disponibles.
    """
    return Role.query.all()

def delete_rol(user_id):
    """
    Elimina la relación entre un usuario y su rol en la base de datos.
    Args:
    user_id (int): El ID del usuario para el cual se eliminará el rol.
    Returns:
    bool: True si la eliminación fue exitosa, False en caso de error o si no se encontró la relación.
    """
    try:
        # Obtener la fila existente en user_has_role para el usuario
        user_role = User_has_role.query.filter_by(user_id=id).first()
        
        if user_role:
            # Eliminar la fila de la base de datos
            db.session.delete(user_role)
            # Guardar los cambios en la base de datos
            db.session.commit()
        return True  # No se encontró la fila en user_has_role para el usuario
    except Exception as e:
        db.session.rollback()
        return False  # Ocurrió un error al eliminar el rol
    
def validar_institucion(usuarios, list_institution_ids ):
    """
    Crea un nuevo listado de usuarios, tomando por parametro un listado de usuarios inicial y valida que cada
    usuario pertenezca a almenos una de las instituciones que se reciben por parametro

    Args:
        usuarios (list<User>): listado de usuarios a filtrar
        list_institution_ids (list<int>): listado de ids de insittuciones del usuario en session

    Returns:
        listado de usuarios, o lista vacia si no se encuentra ninguno
    """
    lista = list()
    for usu in usuarios:
        usu_institutions = [inst.id for inst in get_institutions_by_user_id(usu.id)]
        if any(inst_id in list_institution_ids for inst_id in usu_institutions):
            lista.append(usu)
    return lista

def eliminar_relacion_institucion_default(id_usuario):
    """
    elimina la relacion de intitucion default "SIN INSTITUCION" una vez se modifica el usuario y se le asigna otra relacion institucion rol

    Args:
        id_usuario (int): id del usuario a modificar
 
    """
    try:
        user_role_institution = User_has_role.query.filter_by(user_id = id_usuario, institution_id = 2).first()
        if (user_role_institution):
            db.session.delete(user_role_institution)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False  
    
def get_relation_user_institution(user_id, inst_id):
    """valida que la tupla no exista ya en la base de datos

    Args:
        user_id (int): 
        inst_id (int): 
        new_role_id (int):
    Returns
     tupla user_has_role or None 
    """
    return User_has_role.query.filter_by(user_id = user_id, institution_id = inst_id).first()
     
     
def institutions_and_roles_per_user(users):
    """recibe un listado de usuarios y devuelve dos diccionarios clave valor {usuario_id , institutions names}
    y {usuario_id ,  rol} para luego ser mostrado desde el index

    Args:
        users (list<User>): 
        
    Return:
        dict{user_id, list<institutions>} , dict{user_id, role}
    """
    if users:
        if len(users) > 0 :
            dict_institutions = {}
            dict_roles = {}
            for user in users:
                dict_institutions[user.id] = [inst.name for inst in get_institutions_by_user_id(user.id)]
                role = get_user_rol(user.id)
                if role:
                    dict_roles[user.id] = role.name
            
            return dict_institutions, dict_roles
    return None,None


def get_super_admin_ids():
    super_admin = Role.query.filter_by(name = "Super Administrador").first()
    return [tupla.user_id for tupla in User_has_role.query.filter_by(role_id = super_admin.id).all()]