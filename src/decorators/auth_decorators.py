from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role", "").upper() != "ADMIN":
            return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_or_self_required(utilisateur_id_param="utilisateur_id"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get('role')
            sub = claims.get('sub')
            utilisateur_id = str(kwargs.get(utilisateur_id_param))
            if role != "ADMIN" and sub != utilisateur_id:
                return jsonify({"msg": "Accès refusé"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
