from flask import request, jsonify
from .database import db 
from .models import User

def deleteAccount():
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username = username).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if not user.check_password(password):
        return jsonify({"error": "Incorrect password"}), 400

    # Cascades to sensors and measurements
    db.session.delete(user)
    db.session.commit()

    return jsonify({"response": "User and related data deleted"}), 200
