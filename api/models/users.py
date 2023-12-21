from datetime import datetime
from api.database import db

class User(db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer, primary_key=True)
    firstName=db.Column(db.String(50), nullable=False)
    lastName=db.Column(db.String(50), nullable=False)
    username=db.Column(db.String(25), nullable=False, unique=True)
    email=db.Column(db.String(80), nullable=False, unique=True)
    password=db.Column(db.Text, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
