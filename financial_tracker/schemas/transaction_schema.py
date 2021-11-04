from main import ma 
from models.transactions import Transaction
from marshmallow_sqlalchemy import auto_field

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    transaction_id = auto_field(dump_only=True)
    
    class Meta:
        model = Transaction
        load_instance = True
        
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
