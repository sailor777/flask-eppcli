from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(64))
    role = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(240), nullable=False)
    active = db.Column(db.Integer, nullable=False, default='1')
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        #return '<User %r>' % self.username
        return '%r' % self.username


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registrant = db.Column(db.String(16), unique=True, nullable=False)
    person = db.Column(db.String(255), nullable=False)
    org = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(32), nullable=False)
    cc = db.Column(db.String(2), nullable=False)
    email = db.Column(db.String(240), nullable=False)
    phone = db.Column(db.String(17), nullable=False)
    crDate = db.Column(db.DateTime)
    status = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', backref='registrant',
                            uselist=False, lazy=True)
    domain = db.relationship('Domain', backref='registrant', lazy=True)


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    #hostobj = db.Column(db.String(255), nullable=False)
    crDate = db.Column(db.DateTime)
    exDate = db.Column(db.DateTime)
    status = db.Column(db.String(255), nullable=False)
    host = db.relationship('Host', backref='domain', lazy=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(60), nullable=False)
    crDate = db.Column(db.DateTime)
    status = db.Column(db.String(255), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
