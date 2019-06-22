from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='template')


@app.route('/')
def index():
    plain = "lucasl"
    key = "7|-|353(.-37|<3`/15847474"
    cipher = ""
    aux = 0
    lim = len(plain) - 1
    for l in key:
        base = ord(l) + ord(plain[aux])
        while (base > 126):
            ex = base - 126
            base = 33 + ex
        cipher += chr(base)
        if aux < lim:
            aux += 1
        else:
            aux = 0
    return cipher





def main():
    app.env = 'development'
    app.secret_key = 'A chave secreta e: batata'
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    main()