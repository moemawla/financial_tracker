from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.transactions import Transaction
import boto3

transaction_images = Blueprint('transaction_images', __name__)

@transaction_images.route("/transactions/<int:id>/image/", methods = ["POST"])
def update_image(id):
    transaction = Transaction.query.get_or_404(id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix != ".jpg":
            return abort(400, description="Invalid file type")
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, transaction.image_filename)

        # note that we have removed this line:
        # image.save(f"static/{course.image_filename}")
        return redirect(url_for("transactions.get_transaction", id = id))
    return abort(400, description="No image")
