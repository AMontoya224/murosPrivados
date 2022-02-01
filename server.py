from usuarios_app import app
from usuarios_app.controladores import controlador_users, controlador_messages

if __name__ == "__main__":
    app.run( debug = True )