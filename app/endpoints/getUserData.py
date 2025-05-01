from flask import jsonify
from flask_login import current_user, login_required

@login_required
def getUserData():
    return jsonify({
        "user_id": current_user.id,
        "username": current_user.username, 
        "userplan": current_user.userplan_id
    }), 200
