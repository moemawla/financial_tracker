from flask import Blueprint
from main import db

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.transactions import Transaction
    from faker import Faker
    faker = Faker()

    for i in range(20):
        transaction = Transaction(faker.catch_phrase())
        db.session.add(transaction)
    
    db.session.commit()
    print("Tables seeded")
