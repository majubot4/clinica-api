from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario, Paciente, Medico, Consulta

from werkzeug.security import generate_password_hash, check_password_hash

@app.post("/pacientes")
def criar_paciente():
    """
    Cadastrar um novo paciente
    ---
    tags:
      - Pacientes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "João Silva"
            idade:
              type: integer
              example: 30
            telefone:
              type: string
              example: "912345678"
    responses:
      200:
        description: Paciente cadastrado com sucesso!
    """
    dados = request.json
    paciente = Paciente(
        nome=dados["nome"],
        idade=dados["idade"],
        telefone=dados["telefone"]
    )
    banco.session.add(paciente)
    banco.session.commit()

    return {
        "mensagem": "Paciente cadastrado!"
    }


@app.get("/pacientes")
def listar_pacientes():
    """
    Listar todos os pacientes cadastrados
    ---
    tags:
      - Pacientes
    responses:
      200:
        description: Lista de pacientes retornada com sucesso
    """
    pacientes = Paciente.query.all()
    resultado = []
    for p in pacientes:
        resultado.append(
            {
                "id": p.id,
                "nome": p.nome,
                "idade": p.idade,
                "telefone": p.telefone
            }
        )

    return jsonify(resultado)


@app.put("/pacientes/<int:id>")
def atualizar_paciente(id):
    """
    Atualizar os dados de um paciente existente
    ---
    tags:
      - Pacientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do paciente a ser atualizado
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "João Silva"
            idade:
              type: integer
              example: 31
            telefone:
              type: string
              example: "988888888"
    responses:
      200:
        description: Paciente atualizado com sucesso!
      404:
        description: Paciente não encontrado
    """
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
    """
    Remover um paciente pelo ID
    ---
    tags:
      - Pacientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do paciente a ser removido
    responses:
      200:
        description: Paciente removido com sucesso
      404:
        description: Paciente não encontrado
    """
    paciente = Paciente.query.get(id)
    
    if not paciente:
        return jsonify({"mensagem": "Paciente não encontrado"}), 404

    banco.session.delete(paciente)
    banco.session.commit()

    return {
        "mensagem": "Paciente removido"
    }