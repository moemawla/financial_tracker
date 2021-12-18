from main import ma 
from models.addresses import Address
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class AddressSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    street_address = auto_field(required=True, validate=Length(min=1))
    suburb_name = auto_field(required=True, validate=Length(min=1))
    state_name = auto_field(required=True, validate=Length(min=1))
    country_id = auto_field(required=True)
    resident_id = auto_field(dump_only=True)
    
    class Meta:
        model = Address
        load_instance = True
        
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
address_update_schema = AddressSchema(partial=True)
