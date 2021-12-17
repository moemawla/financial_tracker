from main import db
from models.transaction_images import TransactionImage

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_name = db.Column(db.String(80), nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime(), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), nullable=False)
    images = db.relationship('TransactionImage', cascade="all, delete", backref='transaction', lazy='joined')
    
    def __init__(self, transaction_name, transaction_amount, transaction_date):
        self.transaction_name = transaction_name
        self.transaction_amount = transaction_amount
        self.transaction_date = transaction_date

    @property
    def new_image_file_name(self):
        new_id = 1
        for image in self.images:
            if image.image_id >= new_id:
                new_id = image.image_id + 1

        return f'transaction_images/{self.transaction_id}_{new_id}.jpg'
