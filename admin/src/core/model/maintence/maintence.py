from datetime import datetime
from src.core.database import db


class Maintence(db.Model):
    __tablename__ = "Maintence"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    estado = db.Column(db.Boolean, default=False)
    message = db.Column(db.String(255))
    contact = db.Column(db.String(255))

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.estado = kwargs.get("estado")
        self.message = kwargs.get("message")
        self.contact = kwargs.get("contact")
    