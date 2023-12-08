from datetime import datetime
from src.core.database import db

class FileRecord(db.Model):
    __tablename__="files"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    service_requests = db.relationship("ServiceRequest", back_populates="files")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.filename = kwargs.get("filename")