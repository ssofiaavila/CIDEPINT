from datetime import datetime
from src.core.database import db
from enum import Enum


class NombreEstado(Enum):
    Pendiente = "Pendiente"
    Aceptada = "Aceptada"
    Rechazada = "Rechazada"
    En_Proceso = "En Proceso"
    Finalizada = "Finalizada"
    Cancelada = "Cancelada"


class Estado(db.Model):
    __tablename__ = "estado"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20), default="Pendiente")
    note = db.Column(db.String(255))
    service_requests = db.relationship("ServiceRequest", back_populates="estados")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name")        