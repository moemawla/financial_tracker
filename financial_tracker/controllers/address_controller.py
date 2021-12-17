from flask import Blueprint, request, redirect, abort, url_for
from flask_login import login_required, current_user
from models.countries import Country
from main import db
from models.addresses import Address
from schemas.address_schema import address_schema, address_update_schema
from marshmallow import ValidationError

addresses = Blueprint('addresses', __name__)

@addresses.route('/addresses/', methods=['POST'])
@login_required
def create_or_update_address():
    if not current_user.address:
        new_address = address_schema.load(request.form)
        new_address.resident = current_user
        db.session.add(new_address)
    else:
        address = Address.query.filter_by(resident_id = current_user.id)
        updated_fields = address_schema.dump(request.form)
        errors = address_update_schema.validate(updated_fields)
        if errors:
            raise ValidationError(message = errors)
        if updated_fields:
            address.update(updated_fields)
    db.session.commit()
    return redirect(f"{url_for('users.user_detail')}/")
