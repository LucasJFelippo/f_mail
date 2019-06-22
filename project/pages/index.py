from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import Mail, Message
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash
import sys


app = Flask(__name__, template_folder='template')
app.secret_key = "7|-|353(.-37|<3`/15847474"


sys.path.append('../database/')
from model.user import User
from dao.userdao import UserDao


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'genicandogenerico@gmail.com'
app.config['MAIL_PASSWORD'] = 'adm@123abc'
app.config['MAIL_DEFAULT_SENDER'] = 'genicandogenerico@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





@app.route('/')
def index():
    if not 'login' in session:
        session['login'] = False
    if session['login']:
        return render_template('main.html', verify=session['verify'])
    else:
        return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('register.html')

@app.route('/forgot')
def forgot():
    return "A fazer"


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.form['name'] == '' or request.form['nickname'] == '' or request.form['password'] == '' or request.form['mail'] == '':
            flash('Please complete the entire request')
            return redirect(url_for('signin'))
        verify = verifyregister(request.form['nickname'], request.form['password'], request.form['mail'])
        if not verify:
            if doregister(request.form['name'], request.form['nickname'], request.form['password'], request.form['mail']):
                return redirect(url_for('index'))
            else:
                return redirect(url_for('signin'))
        else:
            if 1 in verify:
                flash('Nickname already existing')
            if 2 in verify:
                flash('Nickname must be between 6 and 16 characters')
            if 3 in verify:
                flash('Password must be between 6 and 16 characters')
            if 4 in verify:
                flash('Email already registred')
            return redirect(url_for('signin'))
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form['nickname'] == '' or request.form['password'] == '':
            flash('Please complete the entire request')
            return redirect(url_for('index'))
        if verifylogin(request.form['nickname'], request.form['password']):
            return redirect(url_for('index'))
        else:
            flash('Nickname or password typed is wrong')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['login'] = False
    del session['name']
    del session['nickname']
    del session['cod']
    del session['mail']
    del session['verify']
    del session['admin']
    return redirect(url_for('index'))

@app.route('/token/<t>')
def token(t):
    if not session['login']:
        flash('You need to be logged in to validate a token')
        return redirect(url_for('index'))
    else:
        if validatetoken(t):
            flash('Account successfully verified')
            return redirect(url_for('index'))
        else:
            flash('Account verification denied')
            return redirect(url_for('index'))


def verifylogin(nickname, password):
    dao = UserDao()
    user = User(nickname = nickname)
    result = dao.login(user)
    if result:
        numbers = cc(result.nickname)
        pw = result.password.split('$')
        if check_password_hash("pbkdf2:sha256:"+str(numbers['x'])+"$"+pw[1]+"$"+pw[0], password):
            session['login'] = True
            session['name'] = result.name
            session['nickname'] = result.nickname
            session['cod'] = result.cod
            session['mail'] = result.mail
            session['verify'] = result.verify
            session['admin'] = result.admin
            return True
        else:
            return False
    else:
        return False

def verifyregister(nickname, password, mail):
    dao = UserDao()
    error = []
    user = User(nickname = nickname, mail = mail)
    result = dao.verifyuser(user)
    if result:
        for e in result:
            error.append(e)
    if len(nickname) < 6 or len(nickname) > 16:
        error.append(2)
    if len(password) < 6 or len(nickname) > 16:
        error.append(3)
    if len(error) == 0:
        return False
    else:
        return error

def doregister(name, nickname, password, mail):
    dao = UserDao()
    number = cc(nickname)
    ctext = generate_password_hash(password, method='pbkdf2:sha256:'+str(number['x']), salt_length=number['y'])
    cpassword = ctext.split('$')[-1]+"$"+ctext.split('$')[-2]
    user = User(name = name, nickname = nickname, password = cpassword, mail = mail)
    token = "http://127.0.0.1:8000/token/"+ctoken(nickname)
    verifymail(user.mail, token)
    return dao.register(user)

def validatetoken(token):
    if token == ctoken(session['nickname']):
        dao = UserDao()
        user = User(cod = session['cod'])
        user.doverify()
        dao.doverify(user)
        session['verify'] = True
        return True
    else:
        return False

def cc(nickname):
    number = 1
    for l in nickname:
        number = number * ord(l)
    while (len(str(number)) != 5):
        string = str(number)
        number = int(string[:-1]) + int(string[len(string)-1])
    x = number
    while (len(str(number)) != 1):
        string = str(number)
        number = int(string[:-1]) + int(string[len(string)-1])
    y = number
    return {"x": x, "y": y}

def ctoken(nickname):
    plain = nickname
    key = app.secret_key
    cipher = ""
    aux = 0
    lim = len(plain) - 1
    for l in key:
        base = ord(l) + ord(plain[aux])
        while (base > 126):
            ex = base - 126
            base = 33 + ex
        if base == 47:
            base += 1
        cipher += chr(base)
        if aux < lim:
            aux += 1
        else:
            aux = 0
    return cipher

def verifymail(mail, token):
    msg = Message()
    msg.subject = 'Confirmação de e-mail'
    msg.recipients = [mail]
    msg.html = render_template('message.html', token = token)
    thr = Thread(target=send_mail, args=[app, msg])
    thr.start()

def send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))


def main():
    app.env = 'development'
    app.secret_key = 'A chave secreta e: batata'
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    main()