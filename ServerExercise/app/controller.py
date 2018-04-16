from flask import render_template
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
    if current_user.is_authenticated:
        return render_template("homepage.html")

    form = LoginForm()

    if form.validate_on_submit():
        dip=Dipendente.query.filter_by(username=form.username.data, hash_passwd_login=form.password.data).first()
        if dip is None:
            return render_template("homepage.html", form=form, error="Credenziali errate!")

        login_user(dip)
        return render_template("homepage.html")


    return render_template("login.html", form=form)
