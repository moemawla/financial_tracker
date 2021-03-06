from main import db
from models.addresses import Address

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    addresses = db.relationship('Address', backref='country')
    
    def __init__(self, name, active):
        self.name = name
        self.active = bool(active)
