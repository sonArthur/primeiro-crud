import re

from models.usuarios import Usuario
from repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    """Contém as regras de negócio dos usuários."""

    def __init__(self, repository=None):
        # Permite utilizar um repositório alternativo nos testes.
        self.repository = (
            repository
            if repository is not None
            else UsuarioRepository()
        )

    def _validar_dados(self, nome, email):
        """Valida e normaliza os dados recebidos."""

        if not isinstance(nome, str):
            raise ValueError("Nome inválido.")

        if not isinstance(email, str):
            raise ValueError("E-mail inválido.")

        nome = nome.strip()
        email = email.strip().lower()

        if len(nome) < 2:
            raise ValueError(
                "O nome deve possuir pelo menos 2 caracteres."
            )

        if len(nome) > 100:
            raise ValueError(
                "O nome deve possuir no máximo 100 caracteres."
            )

        if len(email) > 254:
            raise ValueError("O e-mail informado é muito longo.")

        formato_email = r"[^@\s]+@[^@\s]+\.[^@\s]+"

        if not re.fullmatch(formato_email, email):
            raise ValueError("Informe um e-mail válido.")

        return nome, email

    def criar_usuario(self, nome, email):
        """Valida e cadastra um usuário."""

        nome, email = self._validar_dados(nome, email)

        existente = self.repository.buscar_por_email(email)

        if existente is not None:
            raise ValueError("Este e-mail já está cadastrado.")

        usuario = Usuario(
            id=None,
            nome=nome,
            email=email,
        )

        return self.repository.criar(usuario)

    def listar_usuarios(self):
        """Retorna os usuários cadastrados."""

        return self.repository.listar_todos()

    def buscar_usuario(self, usuario_id):
        """Busca um usuário pelo ID."""

        return self.repository.buscar_por_id(usuario_id)

    def atualizar_usuario(
        self,
        usuario_id,
        novo_nome,
        novo_email,
    ):
        """Valida e atualiza um usuário existente."""

        nome, email = self._validar_dados(
            novo_nome,
            novo_email,
        )

        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise LookupError("Usuário não encontrado.")

        outro_usuario = self.repository.buscar_por_email(email)

        if (
            outro_usuario is not None
            and outro_usuario.id != usuario_id
        ):
            raise ValueError(
                "Outro usuário já utiliza este e-mail."
            )

        usuario.nome = nome
        usuario.email = email

        atualizado = self.repository.atualizar(usuario)

        if not atualizado:
            raise LookupError(
                "Não foi possível atualizar o usuário."
            )

        return usuario

    def deletar_usuario(self, usuario_id):
        """Exclui um usuário existente."""

        return self.repository.deletar(usuario_id)
