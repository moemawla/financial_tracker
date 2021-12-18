from main import ma 
from models.countries import Country
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class CountrySchema(ma.SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    name = auto_field(dump_only=True)
    active = auto_field(dump_only=True)
    
    class Meta:
        model = Country
        load_instance = True
        
country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
