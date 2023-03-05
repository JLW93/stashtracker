from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Stash, StashItem, stash_schema, stashes_schema, stash_item_schema, stash_items_schema
from datetime import datetime

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'hello': 'world'}

@api.route('/stashes', methods = ['GET'])
@token_required
def get_stashes(current_user_token):
    user = current_user_token.token
    stashes = Stash.query.filter_by(user_token = user).all()
    response = stashes_schema.dump(stashes)
    return jsonify(response)

@api.route('/stashes/<stash_id>', methods = ['GET'])
@token_required
def get_single_stash(current_user_token, stash_id):
    stash = Stash.query.get(stash_id)
    response = stash_schema.dump(stash)
    return jsonify(response)

@api.route('/stashes', methods = ['POST'])
@token_required
def create_stash(current_user_token):
    # print('test')
    # print(request.data)
    stash_name = request.json['stash_name']
    user_token = current_user_token.token

    stash = Stash(stash_name, user_token = user_token)

    db.session.add(stash)
    db.session.commit()

    response = stash_schema.dump(stash)
    return jsonify(response)

@api.route('/stashes/<stash_id>', methods = ['POST', 'PUT'])
@token_required
def update_stash(current_user_token, stash_id):
    stash = Stash.query.get(stash_id)
    stash.stash_name = request.json['stash_name']
    stash.modified_date = datetime.utcnow()
    stash.user_token = current_user_token.token

    db.session.commit()
    response = stash_schema.dump(stash)
    return jsonify(response)

@api.route('/stashes/<stash_id>', methods = ['DELETE'])
@token_required
def delete_stash(current_user_token, stash_id):
    stash = Stash.query.get(stash_id)
    db.session.delete(stash)
    db.session.commit()
    response = stash_schema.dump(stash)
    return jsonify(response)

@api.route('/stashes/<stash_id>/items', methods = ['GET'])
@token_required
def get_stash_items(current_user_token, stash_id):
    items = StashItem.query.filter_by(stash_id = stash_id).all()
    print(items)

    response = stash_items_schema.dump(items)
    return jsonify(response)

@api.route('/stashes/<stash_id>/items/<item_id>', methods = ['GET'])
@token_required
def get_single_item(current_user_token, stash_id, item_id):
    item = StashItem.query.get(item_id)

    response = stash_item_schema.dump(item)
    return jsonify(response)

@api.route('/stashes/<stash_id>/items/<item_id>', methods = ['POST', 'PUT'])
@token_required
def edit_item(current_user_token, stash_id, item_id):
    stash = Stash.query.get(stash_id)
    item = StashItem.query.get(item_id)
    item.item_name = request.json['item_name']
    item.item_type = request.json['item_type']
    item.item_value = request.json['item_value']
    item.purchase_date = request.json['purchase_date']
    item.serial_number = request.json['serial_number']
    item.quantity = request.json['quantity']
    item.user_token = current_user_token.token

    db.session.commit()
    response = stash_item_schema.dump(item)
    return jsonify(response)

@api.route('/stashes/<stash_id>/items/<item_id>', methods = ['DELETE'])
@token_required
def delete_stash_item(current_user_token, stash_id, item_id):
    stash = Stash.query.get(stash_id)
    item = StashItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()

    response = stash_item_schema.dump(item)
    return jsonify(response)

@api.route('/stashes/<stash_id>/items', methods = ['POST'])
@token_required
def create_stash_item(current_user_token, stash_id):
    item_name = request.json['item_name']
    item_type = request.json['item_type']
    item_value = request.json['item_value']
    purchase_date = request.json['purchase_date']
    serial_number = request.json['serial_number']
    quantity = request.json['quantity']

    item = StashItem(item_name, stash_id, quantity, item_type, item_value, purchase_date, serial_number)

    db.session.add(item)
    db.session.commit()

    response = stash_item_schema.dump(item)
    return jsonify(response)

# @api.route('/token', methods = ['GET'])
# @token_required
# def get_token(current_user_token):
#     token = current_user_token.token

#     return token

