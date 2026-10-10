import os

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from services.usuario_service import UsuarioService
from database import criar_tabela


# ============================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================

app = Flask(__name__)

# Necessário para o funcionamento das mensagens flash.
# A chave padrão serve apenas para desenvolvimento local.
# Em produção, configure a variável de ambiente FLASK_SECRET_KEY.
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "chave-local-apenas-desenvolvimento",
)


# Garante que a tabela exista antes de utilizar o serviço.
#criar_tabela()

# Instância do serviço responsável pelas regras de negócio.
service = UsuarioService()


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/")
def index():
    """
    Exibe o painel principal e a lista de usuários.

    A pesquisa é realizada pelo nome ou pelo e-mail.
    """

    termo = request.args.get("q", "").strip()

    # Recupera os usuários por meio da camada de serviço.
    todos_usuarios = service.listar_usuarios()

    # Mantém o total geral, mesmo quando existe uma pesquisa.
    total_usuarios = len(todos_usuarios)

    # Filtra a lista sem alterar os registros armazenados.
    if termo:
        termo_normalizado = termo.casefold()

        usuarios = [
            usuario
            for usuario in todos_usuarios
            if termo_normalizado in usuario.nome.casefold()
            or termo_normalizado in usuario.email.casefold()
        ]
    else:
        usuarios = todos_usuarios

    return render_template(
        "index.html",
        usuarios=usuarios,
        total_usuarios=total_usuarios,
        termo=termo,
    )


# ============================================================
# CADASTRO DE USUÁRIOS
# ============================================================

@app.route("/usuarios/novo", methods=["GET", "POST"])
def criar_usuario():
    """
    Exibe o formulário de cadastro e processa seu envio.
    """

    dados = {
        "nome": "",
        "email": "",
    }

    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
        }

        try:
            service.criar_usuario(
                dados["nome"],
                dados["email"],
            )

            flash(
                "Usuário cadastrado com sucesso!",
                "success",
            )

            return redirect(url_for("index"))

        except ValueError as erro:
            flash(str(erro), "error")

    return render_template(
        "formulario.html",
        titulo="Novo usuário",
        dados=dados,
        modo="criar",
    )


# ============================================================
# EDIÇÃO DE USUÁRIOS
# ============================================================

@app.route(
    "/usuarios/<int:usuario_id>/editar",
    methods=["GET", "POST"],
)
def editar_usuario(usuario_id):
    """
    Carrega os dados existentes e processa a atualização.
    """

    usuario = service.buscar_usuario(usuario_id)

    if usuario is None:
        abort(404)

    dados = {
        "nome": usuario.nome,
        "email": usuario.email,
    }

    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome", "").strip(),
            "email": request.form.get("email", "").strip(),
        }

        try:
            service.atualizar_usuario(
                usuario_id,
                dados["nome"],
                dados["email"],
            )

            flash(
                "Usuário atualizado com sucesso!",
                "success",
            )

            return redirect(url_for("index"))

        except (ValueError, LookupError) as erro:
            flash(str(erro), "error")

    return render_template(
        "formulario.html",
        titulo="Editar usuário",
        dados=dados,
        modo="editar",
        usuario_id=usuario_id,
    )


# ============================================================
# EXCLUSÃO DE USUÁRIOS
# ============================================================

@app.post("/usuarios/<int:usuario_id>/excluir")
def excluir_usuario(usuario_id):
    """
    Exclui um usuário mediante uma requisição POST.
    """

    excluido = service.deletar_usuario(usuario_id)

    if excluido:
        flash(
            "Usuário excluído com sucesso!",
            "success",
        )
    else:
        flash(
            "O usuário informado não foi encontrado.",
            "error",
        )

    return redirect(url_for("index"))


# ============================================================
# PÁGINA DE ERRO 404
# ============================================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """
    Exibe uma página personalizada para recursos inexistentes.
    """

    return render_template("404.html"), 404


# ============================================================
# EXECUÇÃO LOCAL
# ============================================================

if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
