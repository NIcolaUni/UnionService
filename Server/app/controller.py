from flask import render_template, redirect
from flask_login import current_user, login_user
from app import server
from app.model.form import LoginForm
from app.model.dipendente import Dipendente

'''
@server.route('/', methods=["GET", "POST"])
def completaRegistrazione():
    form = CompletaProfilo()

    if form.validate_on_submit():
        return render_template("index.html")

    return render_template("completaProfilo.html", form=form)

@server.route('/index')
def index():
    return render_template("index.html")

@server.route('/regDip')
def regDip():
    return render_template("registraDip.html")
    
'''
@server.route('/regDip')
def regDip():
    return render_template("registraDip.html")

@server.route('/', methods=["GET", "POST"])
def login():
    #if current_user.is_autenticated():
    #    return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        if Dipendente.query.filter_by(username=form.username.data, hash_passwd_login=form.password.data).first() is None:
            return render_template("login.html", form=form, error="Credenziali errate!")
        return render_template("index.html")


    return render_template("login.html", form=form)
