from hashlib import md5
from flask import render_template,flash,redirect,session,url_for,request,g
from flask_login import login_user,logout_user,current_user,login_required
from datetime import datetime
from app import app,db,lm,my_epp
from .forms import (LoginForm,ContactCheckForm,ContactInfoForm,DomainCheckForm,
                    DomainInfoForm,ContactCreateForm,DomainCreateForm,DomainRenewForm)
from .models import User,Contact,Domain,Host
from config import EPP_SERVER,EPP_LOGIN,EPP_PASS


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


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

    form3 = ContactInfoForm()
    registrantinfo = form3.data['registrantinfo']
    if form3.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.contact_info(registrantinfo)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Object does not exist':
            flash("Об'єкт не існує | Object does not exist")
        else:
            flash(resp)
        return redirect(url_for('index'))

    form6 = ContactCreateForm()
    newcontact = form6.data['newcontact']
    person = form6.data['person']
    org = form6.data['org']
    address = form6.data['address']
    email = form6.data['email']
    phone = form6.data['phone']
    if form6.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.contact_create(person,org,address,city,email,phone,newcontact)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Command completed successfully':
            flash('Command completed successfully')
        else:
            flash("Shit happens :()")
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

    form4 = DomainInfoForm()
    domaininfo = form4.data['domaininfo']
    if form4.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_info(domaininfo)
        print(resp)
        my_epp.logout()
        if resp['epp']['response']['result'][0]['msg']['_text']\
            == 'Object does not exist':
            flash("Об'єкт не існує | Object does not exist")
        else:
            flash(resp)
        return redirect(url_for('index'))

    form2 = DomainCreateForm()
    newdomain = form2.data['newdomain']
    contact = form2.data['contact']
    hostobj1 = form2.data['hostobj1']
    hostobj2 = form2.data['hostobj2']
    if form2.validate_on_submit():
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
            flash("Shit happens :()")
        return redirect(url_for('index'))

    form5 = DomainRenewForm()
    renewdomain = form5.data['renewdomain']
    exdate = form5.data['exdate']
    years = form5.data['years']
    if form5.validate_on_submit():
        my_epp.connect(EPP_SERVER)
        resp = my_epp.login(EPP_LOGIN,EPP_PASS)
        resp = my_epp.domain_renew(renewdomain,exdate,years)
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
        return redirect(url_for('index'))

    return render_template('index.html',
                           title='UI EPP Domain System',
                           form=form,
                           form3=form3,
                           form6=form6,
                           form1=form1,
                           form4=form4,
                           form2=form2,
                           form5=form5)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.data['username']).first()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        if form.data['username'] == user.username \
            and md5(form.data['password'].encode('utf-8')).hexdigest() == user.password:
            flash('Login="{}",remember_me={}'.
            format(form.username.data,str(form.remember_me.data)))
            return redirect(url_for('index'))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login'))
    return render_template('login.html',
                            title='Sign In',
                            form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
