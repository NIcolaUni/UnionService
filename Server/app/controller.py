from flask import Flask, render_template
from app import server

@server.route('/homeheader')
def homeheader():
    return render_template('header_homepage.html')

@server.route('/gestioneDip')
def gestioneDip():
    return render_template('gestioneDip.html')

@server.route('/paginaProfilo')
def paginaProfilo():
    return render_template('paginaProfilo.html')

@server.route('/')
def index():
    return render_template('homepage.html')

if __name__ == '__main__':
    	app.run(host='0.0.0.0', port=8000)
