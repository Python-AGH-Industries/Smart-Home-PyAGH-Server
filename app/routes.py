from app.endpoints import getAllUsers
from app.endpoints.addUser import addUser
from app.endpoints.getUserData import getUserData
from app.endpoints.getUserSensors import getUserSensors
from app.endpoints.login import login
from app.endpoints.logout import logout
from app.endpoints.getAllUsers import getAllUsers
from app.endpoints.readSensorData import readSensorData
from app.endpoints.changePassword import changePassword
from app.endpoints.deleteAccount import deleteAccount
from app.endpoints.changeSensorName import changeSensorName

def routes(app):
    # CREATE
    app.add_url_rule('/addUser', 'addUser', addUser, methods = ["POST"])
    
    # READ
    app.add_url_rule(
        '/readSensorData',
        'readSensorData',
        readSensorData,
        methods = ["POST"]
    )
    app.add_url_rule(
        '/getUserSensors',
        'getUserSensors',
        getUserSensors,
        methods = ["POST"]
    )
    app.add_url_rule(
        '/getUserData',
        'getUserData',
        getUserData,
        methods = ["POST"]
    )
    app.add_url_rule('/getAllUsers', 'getAllUsers', getAllUsers)

    # UPDATE
    app.add_url_rule(
        '/changePassword',
        'changePassword',
        changePassword,
        methods = ["POST"]
    )
    app.add_url_rule(
        '/changeSensorName',
        'changeSensorName',
        changeSensorName,
        method = ["POST"]
    )
    
    # DELETE
    app.add_url_rule(
        '/deleteAccount',
        'deleteAccount',
        deleteAccount,
        methods = ["POST"]
    )

    # LOGIN
    app.add_url_rule('/login', 'login', login, methods = ["POST"])
    app.add_url_rule('/logout', 'logout', logout, methods = ["POST"])
