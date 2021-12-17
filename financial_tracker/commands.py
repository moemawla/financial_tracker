from flask import Blueprint
from main import db
from models.countries import Country
from countries import country_names

db_commands = Blueprint("db-custom", __name__)

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
