from datetime import datetime
from hashlib import md5

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db, lm, my_epp
from .forms import (LoginForm, ContactCheckForm,
                    ContactInfoForm, DomainCheckForm,
                    DomainInfoForm, ContactCreateForm,
                    DomainCreateForm, DomainRenewForm)
from .models import User, Contact, Domain, Host
from config import EPP_SERVER, EPP_LOGIN, EPP_PASS


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.data['username']).first()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        if (form.data['username'] == user.username
            and md5(form.data['password'].encode('utf-8')).hexdigest()
            == user.password):
            flash('Login="{}",remember_me={}'.
            format(form.username.data,str(form.remember_me.data)))
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login'))

    return render_template('login.html',
                            title='Sign In',
                            form=form)


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
#@login_required
def index():
    form = ContactCheckForm()
    registrant = form.data['registrant']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.contact_check(registrant)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['resData']['contact:chkData']\
            ['cd'][0]['id']['@avail'] == '0':
            flash("Об'єкт вже існує | Contact not available")
        elif resp['epp']['response']['resData']['contact:chkData']\
            ['cd'][0]['id']['@avail'] == '1':
            flash("Об'єкт доступний | Contact is available")
        else:
            flash("Shit happens :)")
        return redirect(url_for('index'))

    form1 = DomainCheckForm()
    domain = form1.data['domain']
    if form1.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_check(domain)
        print(resp)
        my_epp.logout()
        if domain[-7:] != '.epp.ua' and domain[-8:] != '.epp2.ua':
            flash("Погане ім'я домена | Wrong Domain Name")
        elif resp['epp']['response']['resData']['domain:chkData']\
            ['cd'][0]['name']['@avail'] == '0':
            flash("Об'єкт вже існує | Domain not available")
        elif resp['epp']['response']['resData']['domain:chkData']\
            ['cd'][0]['name']['@avail'] == '1':
            flash("Об'єкт доступний | Domain is available")
        else:
            flash("Shit happens :)")
        return redirect(url_for('index'))
    return render_template('index.html',
                           title='UI EPP Domain System',
                           form=form,
                           form1=form1,)


@app.route('/contact/contact_info', methods=['GET','POST'])
#@login_required
def contact_info():
    form = ContactInfoForm()
    contact_name = form.data['contact_name']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.contact_info(contact_name)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Object does not exist':
            flash("Об'єкт не існує | Object does not exist")
        else:
            flash(resp)
        return redirect(url_for('contact_info'))
    return render_template('contact_info.html',
                           title='UI EPP Domain System',
                           form=form,)


@app.route('/contact/contact_create', methods=['GET','POST'])
#@login_required
def contact_create():
    form = ContactCreateForm()
    newcontact = form.data['newcontact']
    person = form.data['person']
    org = form.data['org']
    address = form.data['address']
    email = form.data['email']
    phone = form.data['phone']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.contact_create(person,org,address,email,phone,newcontact)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Command completed successfully':
            flash('Command completed successfully')
        else:
            flash("Shit happens :()")
        return redirect(url_for('contact_create'))
    return render_template('contact_create.html',
                           title='UI EPP Domain System',
                           form=form,)


@app.route('/domain/domain_info', methods=['GET','POST'])
#@login_required
def domain_info():
    form = DomainInfoForm()
    domain_name = form.data['domain_name']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_info(domain_name)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Object does not exist':
            flash("Об'єкт не існує | Object does not exist")
        else:
            flash(resp)
        return redirect(url_for('domain_info'))
    return render_template('domain_info.html',
                           title='UI EPP Domain System',
                           form=form,)


@app.route('/domain/domain_create', methods=['GET','POST'])
#@login_required
def domain_create():
    form = DomainCreateForm()
    newdomain = form.data['newdomain']
    contact = form.data['contact']
    hostobj1 = form.data['hostobj1']
    hostobj2 = form.data['hostobj2']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_create(newdomain, contact, hostobj1, hostobj2)
        print(resp)
        my_epp.logout()
        if newdomain[-7:] != '.epp.ua' and newdomain[-8:] != '.epp2.ua':
            flash("Погане ім'я домена | Wrong Domain Name")
        elif resp['epp']['response']['result'][0]['msg']['_text'] \
            == 'Command completed successfully':
            flash('Command completed successfully')
        else:
            flash("Shit happens :(")
        return redirect(url_for('domain_create'))
    return render_template('domain_create.html',
                           title='UI EPP Domain System',
                           form=form,)


@app.route('/domain/domain_renew', methods=['GET','POST'])
#@login_required
def domain_renew():
    form = DomainRenewForm()
    domain_name = form.data['domain_name']
    exdate = form.data['exdate']
    years = form.data['years']
    if form.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_renew(domain_name,exdate,years)
        print(resp)
        newexdate = resp['epp']['response']['resData']['domain:renData']['exDate']
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Command completed successfully':
            flash("Домен поновлено успішно | Successfully renewed")
            flash(resp)
        elif resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Object does not exist':
            flash("Об'єкт не існує | Object does not exist")
        return redirect(url_for('domain_renew'))
    return render_template('domain_renew.html',
                           title='UI EPP Domain System',
                           form=form,)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
