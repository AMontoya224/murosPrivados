from flask import request, redirect, session, flash
from usuarios_app import app
from usuarios_app.modelos.modelo_messages import Messages
from datetime import datetime


@app.route( '/send/<idFriend>', methods=['POST'] )
def send_P(idFriend):
    if len(request.form["content"]) < 5:
            flash("El mensaje debe contener al menos 5 caracteres", "dashboard")
            return redirect( '/dashboard' )

    data = {
        "id" : session["id"],
        "content" : request.form["content"],
        "send" : request.form["send"],
        "send_id" : session["id"], 
        "received_id" : int(idFriend), 
        "created_at" : datetime.today(),
        "update_at" : datetime.today()
    }
    idMessage = Messages.agregarMessage(data)
    if idMessage == False:
        flash("Problemas con el database", "dashboard")
        return redirect('/dashboard')

    return redirect( "/dashboard")


@app.route( '/delete/<idMessage>', methods=['POST'] )
def deleteMessage_P(idMessage):
    data = {
        "id" : idMessage
    }
    Messages.deleteMessage(data)
    return redirect( "/dashboard")