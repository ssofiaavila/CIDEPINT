from datetime import datetime
from src.core.database import db
from flask_bcrypt import Bcrypt
from src.core.model.request import ServiceRequest

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=False)
    user_has_role = db.relationship("User_has_role", back_populates="users")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    service_requests = db.relationship("ServiceRequest", back_populates="users")
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name")
        self.lastname = kwargs.get("lastname")
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.activo = kwargs.get("activo")
