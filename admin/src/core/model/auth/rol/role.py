from datetime import datetime
from src.core.database import db



class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    user_has_role = db.relationship("User_has_role", back_populates="roles")
    role_has_permit = db.relationship("Role_has_permit", back_populates="roles")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name")

