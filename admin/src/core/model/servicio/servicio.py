from datetime import datetime
from src.core.database import db
from enum import Enum

class TipoServicio(Enum):
    Analisis = "Analisis"
    Consultoria = "Consultoria"
    Desarrollo = "Desarrollo"


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"))
    institution = db.relationship("Institution", back_populates="services")
    service_requests = db.relationship("ServiceRequest", back_populates="services")
    service_type = db.Column(db.String(25))
    enabled = db.Column(db.Boolean)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("name", "institution_id"),)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.keywords = kwargs.get("keywords")
        self.institution_id = kwargs.get("institution")
        self.service_type = TipoServicio[kwargs.get("service_type")].value
        self.enabled = kwargs.get("enabled", False)