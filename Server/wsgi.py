from app import server as application, database

if __name__ == '__main__':
    database.create_all()
    application.run()

