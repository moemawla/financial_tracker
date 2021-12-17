from controllers.user_controller import users
from controllers.address_controller import addresses
from controllers.transaction_controller import transactions
from controllers.image_controller import transaction_images

registerable_controllers = [users, addresses, transactions, transaction_images]
