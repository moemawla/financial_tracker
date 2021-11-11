from flask import Blueprint, jsonify, request, render_template
from main import db
from models.transactions import Transaction
from schemas.transaction_schema import transactions_schema, transaction_schema

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
    return jsonify(transaction_schema.dump(transaction))

@transactions.route("/transactions/", methods=["POST"])
def create_transaction():
    new_transaction = transaction_schema.load(request.form)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(transaction_schema.dump(new_transaction))

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
