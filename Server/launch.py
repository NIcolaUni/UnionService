from app import server, database
from app.model.db.dipendenteDBmodel import Dipendente
import os

if __name__ == '__main__':
    database.create_all()
    if bool(os.environ.get("FIRST_DIP")):
        newDip = Dipendente(cf="nicpnc123", nome="nicola", cognome="pancheri", username="NicoPan", hash_passwd_login="password_forte")
        database.session.add(newDip)
        database.session.commit()

    server.run(host='0.0.0.0', port=8000)

