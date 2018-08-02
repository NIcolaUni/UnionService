from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, BooleanField, PasswordField, SelectField, SubmitField, RadioField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.html5 import NumberInput
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


class LoginForm(FlaskForm):
    username = StringField("Inserire il proprio username", validators=[DataRequired()])
    password = PasswordField("Inserire la propria password d'accesso", validators=[DataRequired()])
    submit =SubmitField("Login")

class DipFittizioForm(FlaskForm):
    username = StringField("Inserire il proprio username")
    password = PasswordField("Inserire la propria password d'accesso")
    tipo_dip = SelectField("Tipo Dipendente", choices=[("commerciale","Commerciale"), ("tecnico", "Tecnico"),
                                                       ("capo-cantiere", "Capo-cantiere"), ("contabile", "Contabile"), ("esterno", "Esterno")])
    email_dip = StringField("email", validators=[Length(max=60)])
    dirigente = BooleanField("Dirigente")

    def assegnaUserEPass(self):
        random.seed(datetime.datetime.today())
        self.username.data = "fittizio"+"".join(random.choice(['_','-','/']))+"".join(random.choice(string.digits) for n in range(5))
        self.password.data = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])

class ClienteAccoltoForm(FlaskForm):
    nome = StringField("Nome del cliente", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=30)])
    cognome = StringField("Cognome del cliente", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=30)])
    indirizzo = StringField("Indirizzo residenza", validators=[DataRequired("Campo obbligatorio!"), Length(min= 3, max=120)])
    telefono = StringField("Telefono", validators=[DataRequired("Campo obbligatorio!"), Length(min= 8, max=12)])
    email = StringField("Email")
    difficolta = RadioField("Difficoltà cliente", choices=[("facile","Facile"), ("media", "Media"), ("alta", "Alta")])
    tipologia = RadioField("Tipologia cliente", choices=[("immobiliare","Immobiliare"), ("privato", "Privato"), ("azienda", "Azienda")])
    referenza = RadioField("Tipologia cliente", choices=[("passaparola","Passaparola"), ("fiera", "Fiera"), ("ufficio", "Ufficio"), ("internet", "Internet"), ("altro", "Altro")])
    sopraluogo = BooleanField("Sopraluogo")

    lavorazione = TextAreaField("Lavorazione", validators=[DataRequired("Campo obbligatorio!"), Length( max=500)])

    #luogo_sopraluogo = StringField("luogo_sopraluogo")
    #data_sopraluogo = DateField("Data sopraluogo")
    #orario_inizio_sopraluogo = StringField("orario_inizio_sopraluogo")
    #orario_fine_sopraluogo = StringField("orario_fine_sopraluogo")
    #accompagnatore_sopraluogo = SelectField("Tipo accompagnatore_sopraluogo", choices=[("commerciale","Commerciale"), ("tecnico", "Tecnico"),
    #                                                   ("capo-cantiere", "Capo-cantiere"), ("contabile", "Contabile"), ("esterno", "Esterno")])

    submit = SubmitField('Registra cliente')

class ApriPaginaClienteForm(FlaskForm):
    nome_cognome_indirizzo = StringField("Nome cognome indirizzo")


class AggiungiFornitoreForm(FlaskForm):
    nomeFornitore = StringField("Sottogruppo fornitore")
    gruppo_azienda = StringField("Primo gruppo")
    settoreMerceologico = StringField("Settore merceologico")
    stato = SelectField("Stato fornitore", choices=[("collabora", "Collabora"), ("potenziale", "Potenziale")] )
    tempiDiConsegna = StringField("Tempi di consegna")
    prezziNetti = RadioField("Unità misura costo trasporto", choices=[(True,"Sì"), (False, "No")] )
    scontoStandard = IntegerField(widget=NumberInput())
    scontoExtra1 = IntegerField(widget=NumberInput())
    scontroExtra2 = IntegerField(widget=NumberInput())
    trasporto = FloatField(widget=NumberInput())
    imballo = FloatField(widget=NumberInput())
    montaggio = FloatField(widget=NumberInput())
    imballoUnitaMisura = SelectField("Unità misura costo imballo", choices=[("euro", "\u20ac"), ("percentuale", "%")] )
    montaggioUnitaMisura = SelectField("Unità misura costo posa", choices=[("euro", "\u20ac"), ("percentuale", "%")] )
    trasportoUnitaMisura = SelectField("Unità misura costo trasporto", choices=[("euro", "\u20ac"), ("percentuale", "%")] )
    giorniPagamenti = StringField("Giorni pagamenti")
    modalitaPagamenti = StringField("Modalità pagamento")
    tipologiaPagamenti = StringField("Tipologia pagamento")
    provincia = StringField("Provincia fornitore")
    indirizzo = StringField("Via, civico, cap, città")
    telefono = StringField(widget=NumberInput())
    sito = StringField("Sito")
    nomeRappresentante =  StringField("Nome e cognome rappresentante")
    telefonoRappresentante =  StringField(widget=NumberInput())
    emailRappresentante =  StringField("Email rappresentante")

