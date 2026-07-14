from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario, Paciente, Medico, Consulta

from werkzeug.security import generate_password_hash, check_password_hash

@app.post("/pacientes")
def criar_paciente():
    dados=request.json
    paciente=Paciente(
        nome=dados["nome"],
        idade=dados["idade"],
        telefone=dados["telefone"]
    )
    banco.session.add(paciente)
    banco.session.commit()

    return {
        "mensagem":"Paciente cadastrado!"
    }


@app.get("/pacientes")
def listar_pacientes():

    pacientes=Paciente.query.all()
    resultado=[]
    for p in pacientes:
        resultado.append(
            {
                "id":p.id,
                "nome":p.nome,
                "idade":p.idade,
                "telefone":p.telefone
            }
        )

    return jsonify(resultado)

@app.put("/pacientes/<int:id>")
def atualizar_paciente(id):
    dados = request.json
    paciente = Paciente.query.get(id)
    
    if not paciente:
        return jsonify({"mensagem": "Paciente não encontrado"}), 404
        
    paciente.nome = dados.get("nome", paciente.nome)
    paciente.idade = dados.get("idade", paciente.idade)
    paciente.telefone = dados.get("telefone", paciente.telefone)
    
    banco.session.commit()
    return jsonify({"mensagem": "Paciente atualizado com sucesso!"})


@app.delete("/pacientes/<int:id>")
def deletar_paciente(id):

    paciente=Paciente.query.get(id)
    banco.session.delete(paciente)
    banco.session.commit()

    return {
        
        "mensagem":"Paciente removido"
    }
    
