from main import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_name = db.Column(db.String(80), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))
    
    def __init__(self, transaction_name):
        self.transaction_name = transaction_name

    @property
    def image_filename(self):
        return f"transaction_images/{self.transaction_id}.jpg"
