from datetime import datetime
from src.core.database import db

class User_has_role(db.Model):
    __tablename__ = "user_has_role"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = db.relationship("User",  back_populates="user_has_role")
    institution_id = db.Column( db.Integer, db.ForeignKey("institutions.id"))
    institutions = db.relationship("Institution",  back_populates="user_has_role")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    roles = db.relationship("Role",  back_populates="user_has_role")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.user_id = kwargs.get("user_id")
        self.institution_id = kwargs.get("institution_id")
        self.role_id = kwargs.get("role_id")
