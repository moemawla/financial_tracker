from main import db

class TransactionImage(db.Model):
    __tablename__ = 'transaction-images'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    
    def __init__(self, file_name):
        self.file_name = file_name
