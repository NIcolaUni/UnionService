from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CompletaProfilo(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    sesso = SelectField("Sesso", choices=[("m","Maschio"), ("f", "Femmina")])
    citta = StringField("Città", validators=[DataRequired()])
    via = StringField("Via residenza", validators=[DataRequired()])
    civico = StringField("Civico residenza", validators=[DataRequired()])
    cap = IntegerField("CAP residenza", validators=[DataRequired()])
    telefono = IntegerField("Telefono", validators=[DataRequired()])
    email = StringField("Email di lavoro", validators=[DataRequired()])
    pass_email = PasswordField("Password email", validators=[DataRequired()])
    iban = StringField("IBAN", validators=[DataRequired()])
    submit = SubmitField('Fatto!')

class RegistraDipendente(FlaskForm):
    nome = StringField("Nome del dipendente", validators=[DataRequired()])
    cognome = StringField("Cognome del dipendente", validators=[DataRequired()])
    cf = StringField("Codice Fiscale", validators=[DataRequired()])
    tipo_dip = SelectField("Tipo Dipendente", choices=[("commerciale","Commerciale"), ("tecnico", "Tecnico"),
                                                       ("capo-cantiere", "Capo-cantiere"), ("contabile", "Contabile"), ("esterno", "Esterno")])
    dirigente = BooleanField("Dirigente")
    costo = IntegerField("Costo orario del dipendente", validators=[DataRequired()])
    contract_expire = DateField("Giorno scadenza contratto")
    tipo_orario =SelectField("Tipo Dipendente", choices=[("full", "Full Time"), ("part", "Part Time")])
   # disponibilita =

class LoginForm(FlaskForm):
    username = StringField("Inserire il proprio username", validators=[DataRequired()])
    password = PasswordField("Inserire la propria password d'accesso", validators=[DataRequired()])
    submit =SubmitField("Login")

class DipFittizioForm(FlaskForm):
    tipo_dip = SelectField("Tipo Dipendente", choices=[("commerciale","Commerciale"), ("tecnico", "Tecnico"),
                                                       ("capo-cantiere", "Capo-cantiere"), ("contabile", "Contabile"), ("esterno", "Esterno")])
    dirigente = BooleanField("Dirigente")
    submit = SubmitField("Genera")