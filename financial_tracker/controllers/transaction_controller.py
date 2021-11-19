from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from main import db
from models.transactions import Transaction
from schemas.transaction_schema import transactions_schema, transaction_schema
import boto3

transactions = Blueprint('transactions', __name__)

@transactions.route("/transactions/", methods=["GET"])
def get_transactions():
    data = {
        "page_title": "Transaction Index",
        "transactions": transactions_schema.dump(Transaction.query.all())
    }
    return render_template("transaction_index.html", page_data = data)

@transactions.route("/transactions/<int:id>/", methods = ["GET"])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': transaction.image_filename
        },
        ExpiresIn=100
    )
    
    data = {
        "page_title": "Transaction Detail",
        "transaction": transaction_schema.dump(transaction),
        "image": image_url
    }
    return render_template("transaction_detail.html", page_data = data)

@transactions.route("/transactions/", methods=["POST"])
def create_transaction():
    new_transaction = transaction_schema.load(request.form)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(f"{url_for('transactions.get_transactions')}/{new_transaction.transaction_id}")

@transactions.route("/transactions/<int:id>/", methods=["PUT", "PATCH"])
def update_transaction(id):
    transaction = Transaction.query.filter_by(transaction_id=id)
    updated_fields = transaction_schema.dump(request.json)
    if updated_fields:
        transaction.update(updated_fields)
        db.session.commit()
    return jsonify(transaction_schema.dump(transaction.first()))

@transactions.route("/transactions/<int:id>/", methods = ["DELETE"])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify(transaction_schema.dump(transaction))
