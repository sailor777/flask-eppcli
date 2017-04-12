from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class ContactCheckForm(Form):
    registrant = StringField('Contact_Check', validators=[Length(min=3, max=16)])

class ContactInfoForm(Form):
    registrantinfo = StringField('Contact_Info', validators=[Length(min=3, max=16)])

class DomainCheckForm(Form):
    domain = StringField('Domain_Check', validators=[Length(min=2, max=255)])

class DomainInfoForm(Form):
    domaininfo = StringField('Domain_info', validators=[Length(min=2, max=255)])

class ContactCreateForm(Form):
    registrant = StringField('Contact ID', validators=[Length(min=3, max=16)])
    person = StringField('First Last', validators=[Length(min=4, max=25)])
    org = StringField('Company', validators=[Length(min=4, max=255)])
    address = StringField('Address', validators=[Length(min=4, max=255)])
    city = StringField('City', validators=[Length(min=4, max=25)])
    cc = StringField('Counry Code', validators=[Length(min=2, max=2)])
    email = StringField('Email Address', validators=[Length(min=6, max=240)])
    phone = StringField('Phone number', validators=[DataRequired()])

class DomainCreateForm(Form):
    newdomain = StringField('New_Domain', validators=[Length(min=2, max=255)])
    contact = StringField('Contact_ID', validators=[Length(min=3, max=16)])
    hostobj1 = StringField('NS1', validators=[Length(min=2, max=255)])
    hostobj2 = StringField('NS2', validators=[Length(min=2, max=255)])

class DomainRenewForm(Form):
    renewdomain = StringField('Domain_Name', validators=[Length(min=2, max=255)])
    exdate = StringField('exDate', validators=[Length(min=10, max=10)])
    years = StringField('Years', validators=[Length(min=1, max=2)])
