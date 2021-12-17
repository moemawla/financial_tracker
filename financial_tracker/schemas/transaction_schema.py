from marshmallow import fields
from main import ma 
from models.transactions import Transaction
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    transaction_id = auto_field(dump_only=True)
    transaction_name = auto_field(required=True, validate=Length(min=1))
    transaction_amount = fields.Number(required=True)
    transaction_date = fields.Date(required=True)
    creator = ma.Nested('UserSchema', only=('id', 'name', 'email'))
    
    class Meta:
        model = Transaction
        load_instance = True
        
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
