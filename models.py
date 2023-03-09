from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(100), nullable = True, default = '')
    last_name = db.Column(db.String(100), nullable = True, default = '')
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name = '', last_name = '', password = '', token = '', g_auth_verify = False):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f'User { self.email } has been added to the Database.'

class UserSchema(ma.Schema):
    class Meta:
        fields = ['first_name', 'last_name', 'email']

user_schema = UserSchema()

class Stash(db.Model):
    stash_id = db.Column(db.String, primary_key = True)
    stash_name = db.Column(db.String(100), nullable = False)
    modified_date = db.Column(db.DateTime, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, stash_name, user_token, stash_id = '', modified_date = datetime.utcnow()):
        self.stash_id = self.set_id()
        self.stash_name = stash_name
        self.modified_date = modified_date
        self.user_token = user_token

    def __repr__(self):
        return f'The following Stash was created: {self.stash_name}.'

    def set_id(self):
        return (secrets.token_urlsafe())

class StashSchema(ma.Schema):
    class Meta:
        fields = ['stash_id', 'stash_name', 'modified_date']

stash_schema = StashSchema()
stashes_schema = StashSchema(many = True)

class StashItem(db.Model):
    item_id = db.Column(db.String, primary_key = True)
    item_name = db.Column(db.String(100), nullable = False)
    item_type = db.Column(db.String(100), nullable = True, default = '')
    item_value = db.Column(db.Numeric(8,2), nullable = True, default = '')
    purchase_date = db.Column(db.String(50), nullable = True, default = '')
    serial_number = db.Column(db.String(100), nullable = True, default = '')
    quantity = db.Column(db.Numeric(4,0), nullable = False, default = 1)
    stash_id = db.Column(db.String, db.ForeignKey('stash.stash_id'), nullable = False)
    # user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, item_name, stash_id, quantity = 1, item_type = '', item_value = '', purchase_date = '', serial_number = '', item_id = ''):
        self.item_id = self.set_id()
        self.item_name = item_name
        self.stash_id = stash_id
        self.item_type = item_type
        self.item_value = item_value
        self.purchase_date = purchase_date
        self.serial_number = serial_number
        self.quantity = quantity


    def __repr__(self):
        return f'The following item has been added to a Stash: {self.item_name}.'

    def set_id(self):
        return (secrets.token_urlsafe())

class StashItemSchema(ma.Schema):
    class Meta:
        fields = ['item_id', 'item_name', 'item_type', 'item_value', 'purchase_date', 'serial_number', 'quantity']

stash_item_schema = StashItemSchema()
stash_items_schema = StashItemSchema(many = True)