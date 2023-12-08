from src.core.model import auth
from src.core.model import institucion
from src.core.model import pagination
from src.core.model.auth import rol
from src.core.model import combined_tables
from src.core.model.auth import permiso
from src.core.model import servicio
from src.core.model.request import estados
from src.core.model import maintence
from src.core.model import days_hours
  

def run():
    """
    Este script se utiliza para inicializar y poblar la base de datos con datos de prueba. Proporciona ejemplos de cómo crear instituciones, usuarios, roles, permisos, servicios y estados, y cómo asignar permisos a roles. Además, crea relaciones entre usuarios, roles e instituciones.
    """
    print("Creando mantenimiento")
    maintence.create_maintence(
        estado=False,
        message="Mantenimiento de prueba",
        contact="grupo19@gmail.com"
    )

    print("Creando franja horarias")
    manana  = days_hours.create_franja_horaria(name='Mañana')
    tarde    = days_hours.create_franja_horaria(name='Tarde')
    completo = days_hours.create_franja_horaria(name='Mañana y tarde')

    pagination.create_pagination(5)

    print("Populando la Base de datos con 3 instituciones")
    institution0 = institucion.create_institution(
        name = 'SUPER ADMIN', 
        info = 'SUPER ADMIN TO ACCESS ROLES',
        address = '', 
        location = '',
        web = '',
        keywords = 'SUPER ADMIN',
        contact_info = 'SUPERADMIN@gmail.com',
        enabled = False,
        phone = '',
    )
    institution_default = institucion.create_institution(
        name = 'SIN INSTITUCION', 
        info = 'SIN INSTITUCION ASIGNADA',
        address = 'SIN INSTITUCION ASIGNADA', 
        location = 'SIN INSTITUCION ASIGNADA',
        web = 'SIN INSTITUCION ASIGNADA',
        keywords = 'SIN INSTITUCION ASIGNADA',
        contact_info = 'SIN INSTITUCION ASIGNADA',
        enabled = False,
        phone = 'SIN INSTITUCION ASIGNADA',
    )
    institution1 = institucion.create_institution(
        name = 'Pintureria Faranda', 
        info = 'Es grande',
        address = 'calle 5, 1345, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://pintureriasfaranda.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'faranda@gmail.com',
        enabled = True,
        phone = '2212313531',
    )
    institution2 = institucion.create_institution(
        name = 'Rex pintureria', 
        info = 'Es de la B',
        address = 'calle 8, 1345, La Plata', 
        location = '1000202320 220000000',
        web = 'https://somosrex.com/',
        keywords = 'analisis tecnologia rodillo pintura',
        contact_info = 'rex@gmail.com',
        enabled = True,
        phone = '112225055',
    )
    institution3 = institucion.create_institution(
        name = 'Colorplast', 
        info = 'Mas de 50 años ayudandote a diseñar tus espacios',
        address = 'calle 25, 1345, La Plata', 
        location = '1000002200 18800000000',
        keywords = 'macilla, color, durabilidad, pintura, sintetico',
        web = 'https://www.colorshop.com.ar',
        contact_info = 'ensuciantes_de_la_plata@gmail.com',
        enabled = True,
        phone = '3333333333',
    )
    institution4 = institucion.create_institution(
        name = 'Institucion Test 1', 
        info = 'Institucion pre cargada de test 1',
        address = 'calle 15, 1550, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinsti1@gmail.com',
        enabled = True,
        phone = '11111111',
    )
    institution5 = institucion.create_institution(
        name = 'Institucion Test 2', 
        info = 'Institucion pre cargada de test 2',
        address = 'calle 1, 1000, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinsti2@gmail.com',
        enabled = True,
        phone = '22222222',
    )
    institution6 = institucion.create_institution(
        name = 'Institucion Test 3', 
        info = 'Institucion pre cargada de test 3',
        address = 'calle 3, 845, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinst3@gmail.com',
        enabled = True,
        phone = '333333333',
    )
    institution7 = institucion.create_institution(
        name = 'Institucion Test 4', 
        info = 'Institucion pre cargada de test 4',
        address = 'calle 12, 1345, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinst4@gmail.com',
        enabled = True,
        phone = '44444444444',
    )
    institution8 = institucion.create_institution(
        name = 'Institucion Test 5', 
        info = 'Institucion pre cargada de test 5',
        address = 'calle 17, 1345, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinsti5@gmail.com',
        enabled = True,
        phone = '555555555',
    )
    institution9 = institucion.create_institution(
        name = 'Institucion Test 6', 
        info = 'Institucion pre cargada de test 6',
        address = 'calle 22, 1345, La Plata', 
        location = '100000023022 2221000002',
        web = 'https://www.google.com.ar/',
        keywords = 'pintura, color, sintetico, agua',
        contact_info = 'testinst6@gmail.com',
        enabled = True,
        phone = '66666666666',
    )

    print("Creacion de instituciones completada")

    days_hours.create_days_hour(institution1.id, manana.id, **{"lunes":True, "martes":True, "miercoles":True,"jueves":True, "viernes":True})
    days_hours.create_days_hour(institution2.id, tarde.id, **{"lunes":True, "martes":True, "miercoles":True,"jueves":True, "viernes":True})
    days_hours.create_days_hour(institution3.id, completo.id, **{"lunes":True, "martes":True, "miercoles":True,"jueves":True, "viernes":True})

    
    print("Populando la Base de datos con 9 users")
    user1 = auth.create_user(
        name = 'SUPER ADMIN', 
        lastname = 'SUPER ADMIN', 
        username = "SUPERADMIN",
        email = 'super@admin.com',
        password = '123456',
        activo = True, 
        date_of_birth = '1995-02-15'
    )
    user2 = auth.create_user(
        name = 'Pedro', 
        lastname = 'Gonzalez',
        username = "pedrogon", 
        email = 'email2@example.com', 
        password = '123456',
        date_of_birth = '1985-02-15'
    )
    user3 = auth.create_user(
        name = 'Mariano', 
        lastname = 'Rodriguez',
        username = "marianRo", 
        email = 'email3@example.com', 
        password = '123456',
        activo = True,
        date_of_birth = '1999-02-15'
    )
    user4 = auth.create_user(
        name = 'Lucas', 
        lastname = 'Paniagua',
        username = "lucaspa", 
        email = 'email4@example.com', 
        password = '123456',
        activo = True,
        date_of_birth = '1990-02-15'
    )
    user5 = auth.create_user(
        name = 'Lionel', 
        lastname = 'Messi',
        username = "liome", 
        email = 'email5@example.com', 
        password = '123456',
        date_of_birth = '1986-04-16'
    )
    user6 = auth.create_user(
        name = 'Matias', 
        lastname = 'Aruse',
        username = "matiaru", 
        email = 'email6@example.com', 
        password = '123456',
        activo = True,
        date_of_birth = '2000-02-15'
    )
    user7 = auth.create_user(
        name = 'Mateo', 
        lastname = 'Retegui',
        username = "retegol", 
        email = 'email7@example.com', 
        password = '123456',
        activo = True,
        date_of_birth = '1993-05-15'
    )
    user8 = auth.create_user(
        name = 'Juan Sebastian', 
        lastname = 'Veron',
        username = "brujita", 
        email = 'email8@example.com', 
        password = '123456',
        activo = True,
        date_of_birth = '1978-11-11'
    )
    user9 = auth.create_user(
        name = 'Perrito', 
        lastname = 'Prediguer',
        username = "perritope", 
        email = 'email9@example.com', 
        password = '123456',
        date_of_birth = '1980-02-15'
    )
    
    print("Creacion de users completada")
    
    
    print("Populando base de datos con 4 roles")
    
    super_administrador = rol.create_role(name = "Super Administrador")
    usuario_sin_rol = rol.create_role(name = "Usuario sin rol")
    administrador = rol.create_role(name = "Administrador")
    duenio = rol.create_role(name = "Dueño")
    operador = rol.create_role(name = "Operador")
    
    print("creacion de roles completada")
    
    
    print("Populando base de datos con relaciones user role institution")
    
    combined_tables.assign_relation_user_role_institution(
            user_id = user1.id,
            institution_id = institution0.id,
            role_id = super_administrador.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user2.id,
            institution_id = institution_default.id,
            role_id = usuario_sin_rol.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user3.id,
            institution_id = institution1.id,
            role_id = administrador.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user4.id,
            institution_id = institution1.id,
            role_id = duenio.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user5.id,
            institution_id = institution1.id,
            role_id = operador.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user6.id,
            institution_id = institution2.id,
            role_id = duenio.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user7.id,
            institution_id = institution2.id,
            role_id = operador.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user8.id,
            institution_id = institution1.id,
            role_id = operador.id)
    combined_tables.assign_relation_user_role_institution(
            user_id = user9.id,
            institution_id = institution_default.id,
            role_id = usuario_sin_rol.id)
    
    
    print("Creacion de relaciones completada")

    print("Populando base de datos con permisos")
    index_u = permiso.create_permit(name = "user_index")
    create_u = permiso.create_permit(name = "user_new")
    modify_u = permiso.create_permit(name = "user_update")
    delete_u = permiso.create_permit(name = "user_destroy")
    readonly_u = permiso.create_permit(name = "user_show")
    
    index_i = permiso.create_permit(name = "inst_index")
    create_i = permiso.create_permit(name = "inst_new")
    modify_i = permiso.create_permit(name = "inst_update")
    delete_i = permiso.create_permit(name = "inst_destroy")
    readonly_i = permiso.create_permit(name = "inst_show")
    
    index_s = permiso.create_permit(name = "serv_index")
    create_s = permiso.create_permit(name = "serv_new")
    modify_s = permiso.create_permit(name = "serv_update")
    delete_s = permiso.create_permit(name = "serv_destroy")
    readonly_s = permiso.create_permit(name = "serv_show")
    
    index_r = permiso.create_permit(name = "req_index")
    create_r = permiso.create_permit(name = "req_new")
    modify_r = permiso.create_permit(name = "req_update")
    delete_r = permiso.create_permit(name = "req_destroy")
    readonly_r = permiso.create_permit(name = "req_show")
    
    print("Creacion de permisos completada")
    
    print("Creando relaciones de roles y permisos")
    print("usuario sin registro ni rol asignado")
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = readonly_i.id
    )
    # combined_tables.assign_permit_to_rol(
    #     role_id = usuario_sin_rol.id,
    #     permit_id = index_i.id
    # )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = readonly_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = index_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = readonly_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = create_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = readonly_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = usuario_sin_rol.id,
        permit_id = index_r.id
    )
    
    print("usuario operador asignado")
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = readonly_i.id
    )
    # combined_tables.assign_permit_to_rol(
    #     role_id = operador.id,
    #     permit_id = index_i.id
    # )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = readonly_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = index_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = readonly_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = create_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = readonly_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = index_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = operador.id,
        permit_id = modify_r.id
    )
    print("Permisos de operador OK")
    print("usuario administrador")
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = readonly_i.id
    )
    # combined_tables.assign_permit_to_rol(
    #     role_id = administrador.id,
    #     permit_id = index_i.id
    # )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = create_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = modify_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = delete_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = readonly_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = index_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = readonly_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = index_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = create_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = readonly_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = index_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = modify_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = administrador.id,
        permit_id = delete_r.id
    )
    print("Permisos de administrador OK")
    print("usuario dueño")
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = readonly_i.id
    )
    # combined_tables.assign_permit_to_rol(
    #     role_id = duenio.id,
    #     permit_id = index_i.id
    # )
    # combined_tables.assign_permit_to_rol(
    #     role_id = duenio.id,
    #     permit_id = modify_i.id
    # )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = create_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = modify_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = delete_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = readonly_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = index_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = readonly_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = index_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = modify_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = create_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = readonly_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = index_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = modify_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = duenio.id,
        permit_id = delete_r.id
    )
    print("Permisos de Dueño OK")
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = readonly_i.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = index_i.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = modify_i.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = create_i.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = delete_i.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = create_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = modify_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = delete_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = readonly_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = index_s.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = readonly_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = modify_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = create_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = delete_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = index_u.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = create_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = readonly_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = index_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = modify_r.id
    )
    combined_tables.assign_permit_to_rol(
        role_id = super_administrador.id,
        permit_id = delete_r.id
    )
    print("Permisos de SuperAdmin OK")

    print("Populando base de datos con servicios")
    service_1 = servicio.create_service(
       name = "Ensayo de corrosion",
       description = "Una descripcion",
       keywords = "Etiqueta1, Etiqueta2, Etiqueta3",
       institution = institution3.id,
       service_type = "Analisis",
       enabled = True
    )

    service_2 = servicio.create_service(
       name = "Prueba de tintas",
       description = "Una descripcion más larga",
       keywords = "Etiqueta1, Etiqueta2, Etiqueta3",
       institution = institution1.id,
       service_type = "Desarrollo",
       enabled = True
    )

    service_3 = servicio.create_service(
       name = "Analisis de aislantes",
       description = "Una descripcion un poco más larga",
       keywords = "Etiqueta1, Etiqueta2, Etiqueta3",
       institution = institution2.id,
       service_type = "Consultoria",
       enabled = True
    )
    print("Creacion de servicios completado")

    print("Creando los posibles estados default")
    pending = estados.create_estado()
    aceptado = estados.create_estado(name = "Aceptado")
    rechazada = estados.create_estado(name = "Rechazado")
    en_proceso = estados.create_estado(name = "En Proceso")
    finalizada = estados.create_estado(name = "Finalizada")
    cancelada = estados.create_estado(name = "Cancelada")

    
    
    print("Relaciones completadas")
    
