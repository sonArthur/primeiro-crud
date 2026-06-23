from flask import Flask, request, jsonify
from database import conectar, criar_tabela

app = Flask(__name__)

criar_tabela()

# Criar usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')

    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201


# Listar usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conn.close()

    lista = []
    for u in usuarios:
        lista.append({"id": u[0], "nome": u[1], "email": u[2]})

    return jsonify(lista)


# Buscar por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        return jsonify({"id": usuario[0], "nome": usuario[1], "email": usuario[2]})
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404


# Atualizar
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    #dados = request.json 
    dados = request.json or {}
    nome = dados.get('nome')
    email = dados.get('email')

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE usuarios SET nome=?, email=? WHERE id=?", (nome, email, id))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    conn.close()
    return jsonify({"mensagem": "Atualizado com sucesso"})


# Deletar
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    conn.close()
    return jsonify({"mensagem": "Deletado com sucesso"})


if __name__ == '__main__':
    app.run(debug=True)
    
    