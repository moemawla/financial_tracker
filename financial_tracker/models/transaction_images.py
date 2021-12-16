from main import db

class TransactionImage(db.Model):
    __tablename__ = 'transaction-images'
    image_id = db.Column(db.Integer, primary_key=True)
    image_file_name = db.Column(db.String(80), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'))
    
    def __init__(self, image_file_name):
        self.image_file_name = image_file_name
