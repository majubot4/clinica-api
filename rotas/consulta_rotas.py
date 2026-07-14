from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario, Paciente, Medico, Consulta

@app.post("/consultas")
def criar_consulta():
    dados = request.json

    consulta = Consulta(
        data=dados["data"],
        horario=dados["horario"],
        paciente_id=dados["paciente_id"],
        medico_id=dados["medico_id"],
        usuario_id=dados["usuario_id"]
    )

    banco.session.add(consulta)
    banco.session.commit()

    return {
        "mensagem": "Consulta cadastrada!"
    }

@app.get("/consultas")
def listar_consultas():

    consultas = Consulta.query.all()

    resultado = []

    for c in consultas:
        resultado.append({
            "id": c.id,
            "data": c.data,
            "horario": c.horario,
            "paciente_id": c.paciente_id,
            "medico_id": c.medico_id,
            "usuario_id": c.usuario_id
        })

    return jsonify(resultado)

@app.put("/consultas/<int:id>")
def atualizar_consulta(id):

    dados = request.json

    consulta = Consulta.query.get(id)

    if not consulta:
        return {
            "mensagem": "Consulta não encontrada"
        }, 404

    consulta.data = dados.get("data", consulta.data)
    consulta.horario = dados.get("horario", consulta.horario)
    consulta.paciente_id = dados.get("paciente_id", consulta.paciente_id)
    consulta.medico_id = dados.get("medico_id", consulta.medico_id)
    consulta.usuario_id = dados.get("usuario_id", consulta.usuario_id)

    banco.session.commit()

    return {
        "mensagem": "Consulta atualizada!"
    }

@app.delete("/consultas/<int:id>")
def deletar_consulta(id):

    consulta = Consulta.query.get(id)

    if not consulta:
        return {
            "mensagem": "Consulta não encontrada"
        }, 404

    banco.session.delete(consulta)
    banco.session.commit()

    return {
        "mensagem": "Consulta removida!"
    }