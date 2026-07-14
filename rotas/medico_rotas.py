from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario, Paciente, Medico, Consulta

from werkzeug.security import generate_password_hash, check_password_hash

@app.post("/medicos")
def criar_medico():

    dados = request.json

    medico = Medico(
        nome=dados["nome"],
        especialidade=dados["especialidade"]
    )

    banco.session.add(medico)
    banco.session.commit()

    return {
        "mensagem": "Médico cadastrado!"
    }


@app.get("/medicos")
def listar_medicos():

    medicos = Medico.query.all()

    resultado = []

    for m in medicos:
        resultado.append(
            {
                "id": m.id,
                "nome": m.nome,
                "especialidade": m.especialidade
            }
        )

    return jsonify(resultado)


@app.put("/medicos/<int:id>")
def atualizar_medico(id):

    dados = request.json

    medico = Medico.query.get(id)

    if not medico:
        return jsonify({
            "mensagem": "Médico não encontrado"
        }), 404

    medico.nome = dados.get("nome", medico.nome)
    medico.especialidade = dados.get("especialidade", medico.especialidade)

    banco.session.commit()

    return jsonify({
        "mensagem": "Médico atualizado com sucesso!"
    })


@app.delete("/medicos/<int:id>")
def deletar_medico(id):

    medico = Medico.query.get(id)

    if not medico:
        return jsonify({
            "mensagem": "Médico não encontrado"
        }), 404

    banco.session.delete(medico)
    banco.session.commit()

    return jsonify({
        "mensagem": "Médico removido com sucesso!"
    })