from flask import Flask
from banco import banco

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

banco.init_app(app)

import modelos  
from rotas import *

with app.app_context():
    banco.create_all()

@app.route("/")
def inicio():
    return {
        "mensagem": "API Clínica Médica funcionando!"
    }