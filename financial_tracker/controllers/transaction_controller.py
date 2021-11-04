from flask import Blueprint, jsonify, request
from main import db
from models.transactions import Transaction

transactions = Blueprint('transactions', __name__)

@transactions.route('/')
def hello_world():
    return 'Hello, World!'

@transactions.route('/students/')
def view_students():
    return 'This page will display a list of all students.'
