from flask import Flask, render_template, redirect, url_for
from app import server
from app.model.form import DipFittizioForm

@server.route('/homeheader')
def homeheader():
    return render_template('header_homepage.html')

@server.route('/gestioneDip', methods=['GET','POST'])
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():
        return redirect('/')
    else:
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
def paginaProfilo():
    return render_template('paginaProfilo.html')

@server.route('/')
def index():
    return render_template('homepage.html')

if __name__ == '__main__':
    	app.run(host='0.0.0.0', port=8000)
