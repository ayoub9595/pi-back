from functools import wraps
from flask import jsonify
from sqlalchemy.exc import IntegrityError

def handle_value_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"msg": str(e)}), 404
    return decorated

def handle_integrity_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except IntegrityError:
            return jsonify({'error': 'Le numéro de série existe déjà.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated