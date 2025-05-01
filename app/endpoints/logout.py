from flask import jsonify
from flask_login import logout_user

def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200