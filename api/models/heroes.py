from datetime import datetime
from api.database import db
from api.database import ma

#This is the hero model
class Hero(db.Model):
    __tablename__ = 'hero'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    firstName=db.Column(db.String(50), nullable=False)
    lastName=db.Column(db.String(50), nullable=False)
    service_number=db.Column(db.String, unique=True)
    year_of_birth=db.Column(db.Integer, nullable=False)
    education=db.Column(db.Text(1000), nullable=False)
    achievements=db.Column(db.Text(1000), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Hero>>> {self.firstName}'
    
class HeroSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields=('id', 'firstName', 'lastName', 'service_number', 'year_of_birth', 'education', 'achievements')

#Initializing our hero's schema
#Initializing schema when fetching a single hero
hero_schema = HeroSchema()

#Initializing schema when fetching many heroes
heroes_schema=HeroSchema(many=True)
        