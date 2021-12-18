from main import db
from models.transaction_images import TransactionImage

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'), nullable=False)
    images = db.relationship('TransactionImage', cascade="all, delete", backref='transaction', lazy='joined')
    
    def __init__(self, name, amount, date):
        self.name = name
        self.amount = amount
        self.date = date

    @property
    def new_image_file_name(self):
        new_id = 1
        for image in self.images:
            if image.id >= new_id:
                new_id = image.id + 1

        return f'transaction_images/{self.id}_{new_id}.jpg'
