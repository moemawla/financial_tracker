from main import ma 
from models.transaction_images import TransactionImage
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class TransactionImageSchema(ma.SQLAlchemyAutoSchema):
    image_id = auto_field(dump_only=True)
    image_file_name = auto_field(required=True, validate=Length(min=1))
    transaction_id = auto_field(required=True)
    
    class Meta:
        model = TransactionImage
        load_instance = True
        
transaction_image_schema = TransactionImageSchema()
transaction_images_schema = TransactionImageSchema(many=True)
