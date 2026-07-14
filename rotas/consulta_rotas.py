from flask import request, jsonify
from app import app
from banco import banco
from modelos import Consulta

@app.post("/consultas")
def agendar_consulta():
    """
    Agendar uma nova consulta
    ---
    tags:
      - Consultas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            data:
              type: string
              example: "2026-07-20"
            horario:
              type: string
              example: "14:30"
            paciente_id:
              type: integer
              example: 1
            medico_id:
              type: integer
              example: 1
            usuario_id:
              type: integer
              example: 1
    responses:
      200:
        description: Consulta agendada com sucesso!
    """
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
    return {"mensagem": "Consulta agendada!"}


@app.get("/consultas")
def listar_consultas():
    """
    Listar todas as consultas agendadas
    ---
    tags:
      - Consultas
    responses:
      200:
        description: Lista de consultas retornada
    """
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
    """
    Reagendar ou modificar uma consulta
    ---
    tags:
      - Consultas
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
            data:
              type: string
              example: "2026-07-25"
            horario:
              type: string
              example: "16:00"
            paciente_id:
              type: integer
              example: 1
            medico_id:
              type: integer
              example: 1
            usuario_id:
              type: integer
              example: 1
    responses:
      200:
        description: Consulta reagendada com sucesso!
    """
    dados = request.json
    consulta = Consulta.query.get(id)
    
    if not consulta:
        return jsonify({"mensagem": "Consulta não encontrada"}), 404
        
    consulta.data = dados.get("data", consulta.data)
    consulta.horario = dados.get("horario", consulta.horario)
    consulta.paciente_id = dados.get("paciente_id", consulta.paciente_id)
    consulta.medico_id = dados.get("medico_id", consulta.medico_id)
    consulta.usuario_id = dados.get("usuario_id", consulta.usuario_id)
    
    banco.session.commit()
    return jsonify({"mensagem": "Consulta atualizada com sucesso!"})


@app.delete("/consultas/<int:id>")
def deletar_consulta(id):
    """
    Cancelar uma consulta pelo ID
    ---
    tags:
      - Consultas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Consulta cancelada com sucesso
    """
    consulta = Consulta.query.get(id)
    if not consulta:
        return jsonify({"mensagem": "Consulta não encontrada"}), 404

    banco.session.delete(consulta)
    banco.session.commit()
    return {"mensagem": "Consulta cancelada"}