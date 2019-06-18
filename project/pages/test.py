from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='template')
app.secret_key = {"pw" = {"port": "6565", "salt": 8}}


@app.route('/')
def index():
    password = generate_password_hash("teste", method='pbkdf2:sha256:6565', salt_length=8)
    print(len(password))
    return password+"  --  "+str(check_password_hash("pbkdf2:sha256:150000$EjgAp0g4$ba5c4b4773ff901b0819286967b4855284e0078813d28be64a04d965fa64ce93", "teste"))


def main():
    app.env = 'development'
    app.secret_key = 'A chave secreta e: batata'
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    main()