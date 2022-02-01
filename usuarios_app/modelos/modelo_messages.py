from usuarios_app.config.mysqlconnection import connectToMySQL

class Messages:
    def __init__( self, id, content, send, send_id, received_id, created_at, update_at ):
        self.id = id
        self.content = content
        self.send = send
        self.send_id = send_id
        self.received_id = received_id
        self.created_at = created_at
        self.update_at = update_at
    
    @classmethod
    def agregarMessage( cls, data ):
        query1 = "ALTER TABLE messages AUTO_INCREMENT = 1;"
        connectToMySQL( "muro_privado" ).query_db( query1 )
        query2 = "INSERT INTO messages(content, send, send_id, received_id, created_at, update_at) VALUES(%(content)s, %(send)s, %(send_id)s, %(received_id)s, %(created_at)s, %(update_at)s);"
        resultado = connectToMySQL( "muro_privado" ).query_db( query2, data )
        return resultado
    
    @classmethod
    def deleteMessage( cls, data ):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        connectToMySQL( "muro_privado" ).query_db( query, data )