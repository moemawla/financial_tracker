from flask import Blueprint
from main import db
from models.users import User
from schemas.user_schema import users_schema
from models.addresses import Address
from schemas.address_schema import addresses_schema
from models.countries import Country
from schemas.country_schema import countries_schema
from models.transactions import Transaction
from schemas.transaction_schema import transactions_schema
from models.transaction_images import TransactionImage
from schemas.transaction_image_schema import transaction_images_schema
from countries import country_names
import os, json

db_commands = Blueprint("db-custom", __name__)

USERS_DUMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "database_dumps/users.json")
ADDRESSES_DUMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "database_dumps/addresses.json")
COUTRIES_DUMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "database_dumps/countries_dump.json")
TRANSACTIONS_DUMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "database_dumps/transactions.json")
IMAGES_DUMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "database_dumps/transaction_images.json")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("init")
def init_db():
    for country_name in country_names:
        country = Country(country_name)
        db.session.add(country)
    db.session.commit()
    print("Table countries populated")

@db_commands.cli.command("dump")
def dump_db():
    dump_data = [
        [User, users_schema, USERS_DUMP_FILE_PATH],
        [Address, addresses_schema, ADDRESSES_DUMP_FILE_PATH],
        [Country, countries_schema, COUTRIES_DUMP_FILE_PATH],
        [Transaction, transactions_schema, TRANSACTIONS_DUMP_FILE_PATH],
        [TransactionImage, transaction_images_schema, IMAGES_DUMP_FILE_PATH]
    ]

    for data in dump_data:
        dump(*data)

def dump(model, schema, file_path):
    entities = db.session.query(model).all()
    data = schema.dump(entities)
    try:
        file = open(file_path, "w")
        contents = json.dumps(data)
        file.write(contents)
    finally:
        file.close()
    print(f'Dumped the data for model { model.__name__ }')
