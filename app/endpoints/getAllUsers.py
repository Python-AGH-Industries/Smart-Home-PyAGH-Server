from flask_login import login_required
from app.models import User

@login_required
def getAllUsers():
    users = User.query.all()
    print(users)
    return str(users)
