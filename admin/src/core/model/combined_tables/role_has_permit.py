from datetime import datetime
from src.core.database import db

class Role_has_permit(db.Model):
    __tablename__ = "role_has_permit"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
    roles = db.relationship("Role",  back_populates="role_has_permit")
    permit_id = db.Column( db.Integer, db.ForeignKey("permits.id"), primary_key=True)
    permits = db.relationship("Permit",  back_populates="role_has_permit")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.role_id = kwargs.get("role_id")
        self.permit_id = kwargs.get("permit_id")
        
