from app import getAllUsers
from app.addUser import addUser
from app.getUserSensors import getUserSensors
from app.login import login
from app.logout import logout
from app.getAllUsers import getAllUsers
from app.readSensorData import readSensorData


def routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/addUser', 'addUser', addUser, methods=["POST"])
    app.add_url_rule('/logout', 'logout', logout, methods=["POST"])

    app.add_url_rule('/readSensorData', 'readSensorData', readSensorData, methods=["POST"])
    app.add_url_rule('/getUserSensors', 'getUserSensors', getUserSensors, methods=["POST"])
    app.add_url_rule('/getAllUsers', 'getAllUsers', getAllUsers)
