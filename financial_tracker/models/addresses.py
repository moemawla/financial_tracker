from main import db

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(80), nullable=False)
    suburb_name = db.Column(db.String(30), nullable=False)
    state_name = db.Column(db.String(30), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), nullable=False, unique=True)
    
    def __init__(self, street_address, suburb_name, state_name, country_id):
        self.street_address = street_address
        self.suburb_name = suburb_name
        self.state_name = state_name
        self.country_id = country_id
