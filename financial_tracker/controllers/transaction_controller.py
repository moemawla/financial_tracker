from flask import Blueprint, request, render_template, redirect, abort, url_for, current_app
from flask_login import login_required, current_user
from main import db
from models.transactions import Transaction
from schemas.transaction_schema import transactions_schema, transaction_schema, transaction_update_schema
from sqlalchemy import func
import boto3
import datetime
from marshmallow import ValidationError

transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions/', methods=['GET'])
@login_required
def get_transactions():
    balance = db.session.query(func.sum(Transaction.amount)).filter(Transaction.creator_id==current_user.id).scalar()
    data = {
        'page_title': 'Transaction Index',
        'balance' : balance if balance else 0.0,
        'transactions': transactions_schema.dump(Transaction.query.filter_by(creator_id=current_user.id).order_by(Transaction.date))
    }
    return render_template('transaction_index.html', page_data = data)

@transactions.route('/', methods=['GET'])
@login_required
def index():
    return redirect(f"{url_for('transactions.get_transactions')}")

@transactions.route('/transactions/<int:id>/', methods = ['GET'])
@login_required
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if transaction.creator != current_user:
        return abort(401, description='Unauthorized')

    images = []

    for image in transaction.images:
        s3_client=boto3.client('s3')
        bucket_name=current_app.config['AWS_S3_BUCKET']
        image_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': image.file_name
            },
            ExpiresIn=100
        )
        images.append({'id': image.id, 'link': image_url})

    data = {
        'page_title': 'Transaction Detail',
        'transaction': transaction_schema.dump(transaction),
        'images': images
    }
    return render_template('transaction_detail.html', page_data = data)

@transactions.route('/transactions/', methods=['POST'])
@login_required
def create_transaction():
    new_transaction = transaction_schema.load(request.form)
    new_transaction.creator = current_user
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(f"{url_for('transactions.get_transactions')}/{new_transaction.id}")

# we are using a POST method for updating because HTML forms do not support PUT/PATCH methods
@transactions.route('/transactions/<int:id>/update/', methods=['POST'])
@login_required
def update_transaction(id):
    transaction = Transaction.query.filter_by(id=id)
    
    if transaction.first().creator != current_user:
        return abort(401, description='Unauthorized')

    updated_fields = transaction_update_schema.dump(
        transaction_schema.load(request.form)
        )

    if updated_fields:
        transaction.update(updated_fields)
        db.session.commit()
    return redirect(f"{url_for('transactions.get_transactions')}/{id}")

# we are using a POST method for deleting because HTML forms do not support DELETE method
@transactions.route('/transactions/<int:id>/delete/', methods = ['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if transaction.creator != current_user:
        return abort(401, description='Unauthorized')

    db.session.delete(transaction)
    db.session.commit()

    # delete images from S3
    for image in transaction.images:
        s3_client=boto3.client('s3')
        s3_client.delete_object(Bucket = current_app.config['AWS_S3_BUCKET'], Key = image.file_name)

    return redirect(url_for('transactions.get_transactions'))
