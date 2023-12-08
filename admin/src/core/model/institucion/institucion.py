from datetime import datetime
from src.core.database import db


class Institution(db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True)
    info = db.Column(db.String(255))
    address = db.Column(db.String(255))
    location = db.Column(db.String(255))
    web = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    services = db.relationship("Service", back_populates="institution")
    contact_info = db.Column(db.String(500))
    enabled = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(255))
    user_has_role = db.relationship("User_has_role", back_populates="institutions")
    
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.name = kwargs.get("name",)
        self.info = kwargs.get("info")
        self.address = kwargs.get("address",)
        self.location = kwargs.get("location")
        self.web = kwargs.get("web")
        self.keywords = kwargs.get("keywords")
        self.contact_info = kwargs.get("contact_info")
        self.enabled = kwargs.get("enabled")
        self.phone = kwargs.get("phone",)


