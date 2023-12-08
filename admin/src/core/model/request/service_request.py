from datetime import datetime
from src.core.database import db

class ServiceRequest(db.Model):
    __tablename__ = "service_requests"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("User", back_populates="service_requests")
    comment = db.Column(db.Text)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    services = db.relationship("Service", back_populates="service_requests")
    estado_id = db.Column(db.Integer, db.ForeignKey("estado.id"), default=1)
    estados = db.relationship("Estado", back_populates="service_requests")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.user_id = kwargs.get("user_id")
        self.service_id = kwargs.get("service_id")
        self.comment = kwargs.get("comment")
