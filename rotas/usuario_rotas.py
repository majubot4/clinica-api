from flask import request, jsonify
from app import app
from banco import banco
from modelos import Usuario
from werkzeug.security import generate_password_hash

@app.post("/usuarios")
def criar_usuario():
    """
    Criar um novo usuário do sistema
    ---
    tags:
      - Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "maria_admin"
            email:
              type: string
              example: "maria@clinica.com"
            password:
              type: string
              example: "senha_secreta"
    responses:
      200:
        description: Usuário criado!
    """
    dados = request.json
    senha_hash = generate_password_hash(dados["password"])
    
    usuario = Usuario(
        username=dados["username"],
        email=dados["email"],
        senha=senha_hash
    )
    banco.session.add(usuario)
    banco.session.commit()
    return {"mensagem": "Usuário criado!"}


@app.get("/usuarios")
def listar_usuarios():
    """
    Listar todos os usuários do sistema
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários retornada com sucesso
    """
    usuarios = Usuario.query.all()
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "username": u.username,
            "email": u.email
        })
    return jsonify(resultado)


@app.put("/usuarios/<int:id>")
def atualizar_usuario(id):
    """
    Atualizar os dados de um usuário
    ---
    tags:
      - Usuários
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
            username:
              type: string
              example: "maria_novo_nome"
            email:
              type: string
              example: "novo_email@clinica.com"
            password:
              type: string
              example: "nova_senha_secreta"
    responses:
      200:
        description: Usuário atualizado com sucesso!
    """
    dados = request.json
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404
        
    usuario.username = dados.get("username", usuario.username)
    usuario.email = dados.get("email", usuario.email)
    
    if "password" in dados:
        usuario.senha = generate_password_hash(dados["password"])
        
    banco.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"})


@app.delete("/usuarios/<int:id>")
def deletar_usuario(id):
    """
    Deletar um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Usuário removido com sucesso
    """
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

    banco.session.delete(usuario)
    banco.session.commit()
    return {"mensagem": "Usuário removido"}