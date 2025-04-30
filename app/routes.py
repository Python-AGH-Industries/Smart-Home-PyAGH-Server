from app import getAllUsers
from app.addUser import addUser
from app.getUserData import getUserData
from app.getUserSensors import getUserSensors
from app.login import login
from app.logout import logout
from app.getAllUsers import getAllUsers
from app.readSensorData import readSensorData
from app.changePassword import changePassword
from app.deleteAccount import deleteAccount

def routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/addUser', 'addUser', addUser, methods=["POST"])
    app.add_url_rule('/logout', 'logout', logout, methods=["POST"])
    app.add_url_rule('/changePassword', 'changePassword', changePassword, methods=["POST"])
    app.add_url_rule('/deleteAccount', 'deleteAccount', deleteAccount, methods=["POST"])

    app.add_url_rule('/readSensorData', 'readSensorData', readSensorData, methods=["POST"])
    app.add_url_rule('/getUserSensors', 'getUserSensors', getUserSensors, methods=["POST"])
    app.add_url_rule('/getUserData', 'getUserData', getUserData, methods=["POST"])

    app.add_url_rule('/getAllUsers', 'getAllUsers', getAllUsers)
