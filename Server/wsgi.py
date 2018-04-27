from app import server as application, database, socketio

if __name__ == '__main__':
    database.create_all()
    socketio.run(application)

