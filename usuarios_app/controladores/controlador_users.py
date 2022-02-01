from flask import render_template, request, redirect, session, flash
from usuarios_app import app
from usuarios_app.modelos.modelo_users import Users


from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route( '/', methods=['GET'] )
def paginaInicio():
    return render_template( "index.html")


@app.route( '/dashboard/', methods=["GET"] )
def despliegaDashboard():
    if "id" not in session:
        return redirect('/')

    dataUser = {
        "id" : session["id"]
    }
    listaUsers = Users.obtenerListaUsersSinUser(dataUser)
    user = Users.obtenerUser(dataUser)
    listaMessages, send_count = Users.obtenerListaMessages(dataUser)
    #for i in range(0, len(listaMessages)-1):
    #    aux = datetime.today() - listaMessages[i]["messages.created_at"]
    #    listaMessages[i]["messages.update_at"] = aux.seconds
    variables = [user["first_name"], len(listaMessages), send_count, "bienvenido"]
    if user["gender"] == "female":
        variables[3] = "bienvenida"
    return render_template( "dashboard.html", listaUsers=listaUsers, listaMessages=listaMessages, variables=variables)


@app.route( '/registrar', methods=["POST"] )
def registrarUser_P():
    if not Users.verificarRegistro(request.form):
        return redirect( '/' )

    nuevoUser = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"]),
        "gender" : request.form["gender"],
        "created_at" : datetime.today(),
        "update_at" : datetime.today()
    }
    idUser = Users.agregarUser( nuevoUser )
    if idUser == False:
        flash("Problemas con el database", "register")
        return redirect('/')

    session["id"] = idUser
    session["email"] = request.form["email"]
    return redirect('/dashboard')


@app.route( '/ingresar', methods=["POST"] )
def ingresarUser_P():
    data = { 
        "email" : request.form["emailUsuario"] 
        }
    user_in_db = Users.conseguirEmail(data)
    if not user_in_db:
        flash("E-mail no registrado", "login")
        return redirect( '/' )

    if not bcrypt.check_password_hash(user_in_db["password"], request.form['passwordUsuario']):
        flash("Contraseña incorrecta", "login")
        return redirect( '/' )

    session["id"] = user_in_db["id"]
    session["email"] = request.form["emailUsuario"]
    return redirect('/dashboard')


@app.route( '/logout', methods=["POST"] )
def borrarSession():
    session.clear()
    return redirect( '/' )


@app.errorhandler(404)
def paginaNoEncontrada(error):
    return "¡Lo siento! No hay respuesta. Inténtalo mas tarde"