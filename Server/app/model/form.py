from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
import random
import datetime
import string

class RegistraDipendenteForm(FlaskForm):
    nome = StringField("Nome del dipendente", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=30)])
    cognome = StringField("Cognome del dipendente", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=30)])
    cf = StringField("Codice Fiscale", validators=[DataRequired("Campo obbligatorio!"), Length(min= 10, max=16)])
    dataNascita = DateField("Data di nascita", validators=[DataRequired("Campo obbligatorio!")])
    residenza = StringField("Indirizzo residenza", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=120)])
    resEDomUguali = BooleanField("Residenza e domicilio coincidono")
    domicilio = StringField("Indirizzo domicilio", validators=[Length(max=120)])
    telefono = StringField("Telefono", validators=[DataRequired("Campo obbligatorio!"), Length(min= 8, max=12)])
    password = PasswordField("Impostare la password che si usareà all'accesso", validators=[DataRequired("Campo obbligatorio!"), Length(min= 6, max=30)])
    email_aziendale = StringField("Email di lavoro", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=50)])
    email_personale = StringField("Email personale", validators=[Length(max=50)])
    iban = StringField("IBAN", validators=[Length(max=30)])
    partitaIva = StringField("Partita Iva (lasciare vuoto in caso non si posieda)", validators=[Length(max=30)])
    submit = SubmitField('Fatto')
'''
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
'''

class LoginForm(FlaskForm):
    username = StringField("Inserire il proprio username", validators=[DataRequired()])
    password = PasswordField("Inserire la propria password d'accesso", validators=[DataRequired()])
    submit =SubmitField("Login")

class DipFittizioForm(FlaskForm):
    username = StringField("Inserire il proprio username")
    password = PasswordField("Inserire la propria password d'accesso")
    tipo_dip = SelectField("Tipo Dipendente", choices=[("commerciale","Commerciale"), ("tecnico", "Tecnico"),
                                                       ("capo-cantiere", "Capo-cantiere"), ("contabile", "Contabile"), ("esterno", "Esterno")])
    dirigente = BooleanField("Dirigente")

    def assegnaUserEPass(self):
        random.seed(datetime.datetime.today())
        self.username.data = "fittizio"+"".join(random.choice(['_','-','/']))+"".join(random.choice(string.digits) for n in range(5))
        self.password.data = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])