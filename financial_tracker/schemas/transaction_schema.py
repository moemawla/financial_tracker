from marshmallow import fields
from main import ma 
from models.transactions import Transaction
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=Length(min=1))
    amount = fields.Number(required=True)
    date = fields.Date(required=True)
    creator_id = auto_field(dump_only=True)
    
    class Meta:
        model = Transaction
        load_instance = True
        
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
