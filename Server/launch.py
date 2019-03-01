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
from app import server, database
import app

if __name__ == '__main__':

    use_debugger = False

    database.create_all()


    if server.config.get('DEBUG'):
        use_debugger = True

        try:
            # Disable Flask's debugger if external debugger is requested
            use_debugger = not (server.config.get('DEBUG_WITH_APTANA'))
        except:
            pass
        server.run(use_debugger=use_debugger, debug=server.config.get('DEBUG'),
                use_reloader=use_debugger, host='0.0.0.0', port=8000)

    else:
        server.run(host='0.0.0.0', port=8000)