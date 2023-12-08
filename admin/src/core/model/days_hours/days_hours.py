
from datetime import datetime
from src.core.database import db

class DiasHorarios(db.Model):
    __tablename__ = "dias_horarios"
    id = db.Column(db.Integer, primary_key=True)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    dia_id = db.Column(db.Integer, db.ForeignKey("dias.id"))
    franja_horaria_id = db.Column(db.Integer, db.ForeignKey("franjas_horarias.id"))

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.institution_id = kwargs.get("institution_id",False)
        self.dia_id = kwargs.get("dia_id",False)
        self.franja_horaria_id = kwargs.get("franja_horaria_id",False)

    def get_selected_days(institution_id):
        # Obtén los IDs de los días seleccionados para la institución
        selected_days = db.session.query(DiasHorarios.dia_id).filter_by(
            institution_id=institution_id).all()
        selected_days = [day[0] for day in selected_days]

        return selected_days

class Dias(db.Model):
    __tablename__ = "dias"
    id = db.Column(db.Integer, primary_key=True)
    lunes = db.Column(db.Boolean, default=False)
    martes = db.Column(db.Boolean, default=False)
    miercoles= db.Column(db.Boolean, default=False)
    jueves = db.Column(db.Boolean, default=False)
    viernes = db.Column(db.Boolean, default=False)
    sabado = db.Column(db.Boolean, default=False)
    domingo = db.Column(db.Boolean, default=False)

    DAYS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    def __init__(self, **kwargs) -> None:
        super().__init__()
        for day in self.DAYS:
            setattr(self, day, kwargs.get(day))

    @classmethod
    def get_selected_day_names(cls, institution_id):
        # Obtén los IDs de los días seleccionados
        selected_day_ids = DiasHorarios.get_selected_days(institution_id)

        # Consulta los nombres de los días correspondientes a los IDs seleccionados
        selected_day_names = []
        for day_id in selected_day_ids:
            day = cls.query.get(day_id)
            if day:
                for day_name in cls.DAYS:
                    if getattr(day, day_name):
                        selected_day_names.append(day_name)

        return selected_day_names
      
class FranjaHoraria(db.Model):
    __tablename__ = "franjas_horarias"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name")

    @staticmethod
    def get_franja_id_by_institution_id(institution_id):
        # Obtén el ID de la franja horaria para la institución dada
        dia_horario = DiasHorarios.query.filter_by(institution_id=institution_id).first()

        if dia_horario:
            # Si se encuentra el registro, obtén el nombre de la franja horaria
            franja_id = dia_horario.franja_horaria_id
            franja_horaria = FranjaHoraria.query.get(franja_id)
            franja_horaria = f"{franja_horaria.id}"
            return franja_horaria

        # Si no se encuentra un registro, puedes devolver un valor predeterminado o None según lo desees
        return None
    
    def get_name(id):
        franja_horaria = FranjaHoraria.query.get(id)
        return franja_horaria.name

        return []
    
    @staticmethod
    def get_franja_name_by_institution_id(institution_id):
        # Obtén el ID de la franja horaria para la institución dada
        dia_horario = DiasHorarios.query.filter_by(institution_id=institution_id).first()

        if dia_horario:
            # Si se encuentra el registro, obtén el nombre de la franja horaria
            franja_id = dia_horario.franja_horaria_id
            franja_horaria = FranjaHoraria.query.get(franja_id)
            return franja_horaria.name

        # Si no se encuentra un registro, puedes devolver un valor predeterminado o None según lo desees
        return []
    