from datetime import datetime
from src.core.database import db


class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    token = db.Column(db.String(255))
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.token = kwargs.get("token")



