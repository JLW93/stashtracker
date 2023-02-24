from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Stash, StashItem, stash_schema, stashes_schema, stash_item_schema, stash_items_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def getdata():
    return {'hello': 'world'}

@api.route('/stashes', methods = ['POST'])
@token_required
def create_stash(current_user_token):
    stash_name = request.json['stash_name']
    user_token = current_user_token.token

    stash = Stash(stash_name, user_token = user_token)

    db.session.add(stash)
    db.session.commit()

    response = stash_schema.dump(stash)
    return jsonify(response)

