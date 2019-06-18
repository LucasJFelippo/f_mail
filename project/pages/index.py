from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__, template_folder='template')
app.secret_key = {"pw": {"port": "6565", "salt": 8}}


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
    if 'login' in session:
        return render_template('select.html')
    else:
        return render_template('login.html')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))


def main():
    app.env = 'development'
    app.secret_key = 'A chave secreta e: batata'
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    main()