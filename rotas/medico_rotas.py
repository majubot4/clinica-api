from flask import request, jsonify
from app import app
from banco import banco
from modelos import Medico

@app.post("/medicos")
def criar_medico():
    """
    Cadastrar um novo médico
    ---
    tags:
      - Médicos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Dr. Carlos Eduardo"
            especialidade:
              type: string
              example: "Cardiologia"
    responses:
      200:
        description: Médico cadastrado!
    """
    dados = request.json
    medico = Medico(
        nome=dados["nome"],
        especialidade=dados["especialidade"]
    )
    banco.session.add(medico)
    banco.session.commit()
    return {"mensagem": "Médico cadastrado!"}


@app.get("/medicos")
def listar_medicos():
    """
    Listar todos os médicos
    ---
    tags:
      - Médicos
    responses:
      200:
        description: Lista de médicos retornada
    """
    medicos = Medico.query.all()
    resultado = []
    for m in medicos:
        resultado.append({
            "id": m.id,
            "nome": m.nome,
            "especialidade": m.especialidade
        })
    return jsonify(resultado)


@app.put("/medicos/<int:id>")
def atualizar_medico(id):
    """
    Atualizar dados de um médico existente
    ---
    tags:
      - Médicos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Dr. Carlos Silva"
            especialidade:
              type: string
              example: "Pediatria"
    responses:
      200:
        description: Médico atualizado com sucesso!
    """
    dados = request.json
    medico = Medico.query.get(id)
    
    if not medico:
        return jsonify({"mensagem": "Médico não encontrado"}), 404
        
    medico.nome = dados.get("nome", medico.nome)
    medico.especialidade = dados.get("especialidade", medico.especialidade)
    
    banco.session.commit()
    return jsonify({"mensagem": "Médico atualizado com sucesso!"})


@app.delete("/medicos/<int:id>")
def deletar_medico(id):
    """
    Deletar um médico pelo ID
    ---
    tags:
      - Médicos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Médico removido com sucesso
    """
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"mensagem": "Médico não encontrado"}), 404

    banco.session.delete(medico)
    banco.session.commit()
    return {"mensagem": "Médico removido"}