from src.core.database import db
from .days_hours import DiasHorarios, Dias, FranjaHoraria

def create_days_hour(id_institution,id_franja,**kwargs):
    """Crea en la tabla DiaH una nueva columna con los **kwargs pasados por parametros, luego la añade y posteriormente se crea una nueva columna de la tabla
    DiasHorarios, con la institucion_id pasada por parametro en id_institution, luego la franja horaria tambien pasada por parametro id_franja, y el dias.id se obtiene
    de los Dias creado anteriormente."""
    dias = Dias(**kwargs) 
    db.session.add(dias)
    db.session.commit()
    dias_horarios = DiasHorarios(institution_id=id_institution,dia_id=dias.id,franja_horaria_id=id_franja)
    db.session.add(dias_horarios)
    db.session.commit()
    return True

def create_franja_horaria(**kwargs):
    """Crea una FranjaHoraria con los **kwargs pasados por parametros"""
    franja_horaria = FranjaHoraria(**kwargs)
    db.session.add(franja_horaria)
    db.session.commit()
    return franja_horaria