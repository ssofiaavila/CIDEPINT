from src.core.database import db

class Pagination(db.Model):
    __tablename__ = "pagination"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cant = db.Column(db.Integer)
    

    def __init__(self, **kwargs) -> None:
        self.cant = kwargs.get("cant")