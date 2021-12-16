from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.transactions import Transaction
from models.transaction_images import TransactionImage
from main import db
import boto3

transaction_images = Blueprint('transaction_images', __name__)

@transaction_images.route('/transactions/<int:transaction_id>/image/', methods = ['POST'])
def add_image(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if 'image' in request.files:
        image = request.files['image']
        if Path(image.filename).suffix != '.jpg':
            return abort(400, description='Invalid file type')
        image_filename = transaction.new_image_filename
        bucket = boto3.resource('s3').Bucket(current_app.config['AWS_S3_BUCKET'])
        bucket.upload_fileobj(image, image_filename)

        # create image entity and link it to the transaction
        transaction_image = TransactionImage(image_filename)
        transaction_image.transaction = transaction
        db.session.add(transaction_image)
        db.session.commit()
        return redirect(url_for('transactions.get_transaction', id = transaction_id))
    return abort(400, description='No image')

@transaction_images.route('/image/<int:image_id>', methods = ['DELETE'])
def remove_image(image_id):
    image = TransactionImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()

    # delete image from S3
    s3_client=boto3.client('s3')
    s3_client.delete_object(Bucket = current_app.config['AWS_S3_BUCKET'], Key = image.image_file_name)
    return redirect(url_for('transactions.get_transaction', id = image.transaction.id))
