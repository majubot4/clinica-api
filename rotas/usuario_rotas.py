from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario, Paciente, Medico, Consulta

from werkzeug.security import generate_password_hash, check_password_hash

@app.post("/usuarios")
def criar_usuario():

    dados = request.json

    senha_hash = generate_password_hash(
        dados["password"]
    )


    usuario = Usuario(
        username=dados["username"],
        email=dados["email"],
        password=senha_hash
    )


    banco.session.add(usuario)
    banco.session.commit()


    return jsonify(
        {
            "mensagem": "Usuário criado!"
        }
    )



@app.post("/login")
def login():

    dados = request.json


    usuario = Usuario.query.filter_by(
        username=dados["username"]
    ).first()


    if usuario and check_password_hash(
        usuario.password,
        dados["password"]
    ):

        return {
            "mensagem": "Login realizado com sucesso"
        }


    return {
        "mensagem": "Usuário ou senha incorretos"
    },401