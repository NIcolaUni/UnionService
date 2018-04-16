'''
from app import server, database
from app.model.dipendente import Dipendente
import os

if __name__ == '__main__':
    if os.environ.get("FIRST_DIP") == True:
        database.create_all()
        newDip = Dipendente(cf="nicpnc123", nome="nicola", cognome="pancheri", username="NicoPan", hash_passwd_login="password_forte")
        database.session.add(newDip)
        database.session.commit()
'''
from app import server

server.run(host='0.0.0.0', port=8000)

