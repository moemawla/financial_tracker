from flask import Blueprint, request, redirect, abort, url_for, current_app
from flask_login import login_required, current_user
from pathlib import Path
from models.transactions import Transaction
from models.transaction_images import TransactionImage
from main import db
import boto3

transaction_images = Blueprint('transaction_images', __name__)

@transaction_images.route('/images/', methods = ['POST'])
@login_required
def add_image():
    transaction_id = request.form['transaction_id']
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        abort(400, description='Invalid transaction id')
    if transaction.creator != current_user:
        return abort(403, description='Unauthorized')
    if 'image' in request.files:
        image = request.files['image']
        if Path(image.filename).suffix != '.jpg':
            return abort(400, description='Invalid file type')
        image_file_name = transaction.new_image_file_name
        bucket = boto3.resource('s3').Bucket(current_app.config['AWS_S3_BUCKET'])
        bucket.upload_fileobj(image, image_file_name)

        # create image entity and link it to the transaction
        transaction_image = TransactionImage(image_file_name)
        transaction_image.transaction = transaction
        db.session.add(transaction_image)
        db.session.commit()
        return redirect(url_for('transactions.get_transaction', id = transaction_id))
    return abort(400, description='No image')

@transaction_images.route('/images/<int:image_id>/delete/', methods = ['DELETE', 'POST'])
@login_required
def remove_image(image_id):
    image = TransactionImage.query.get_or_404(image_id)

    if image.transaction.creator != current_user:
        return abort(403, description='Unauthorized')

    transaction_id = image.transaction.transaction_id

    db.session.delete(image)
    db.session.commit()

    # delete image from S3
    s3_client=boto3.client('s3')
    s3_client.delete_object(Bucket = current_app.config['AWS_S3_BUCKET'], Key = image.image_file_name)
    return redirect(url_for('transactions.get_transaction', id = transaction_id))
