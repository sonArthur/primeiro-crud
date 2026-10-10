from models.usuarios import Usuario
from database import conectar


class UsuarioRepository:
    """Responsável pelo acesso aos dados dos usuários."""

    def criar(self, usuario):
        """Insere um usuário no banco de dados."""

        conn = conectar()

        try:
            cursor = conn.execute(
                """
                INSERT INTO usuarios (nome, email)
                VALUES (?, ?)
                """,
                (usuario.nome, usuario.email),
            )

            conn.commit()

            return Usuario(
                cursor.lastrowid,
                usuario.nome,
                usuario.email,
            )

        finally:
            conn.close()

    def listar_todos(self):
        """Retorna todos os usuários cadastrados."""

        conn = conectar()

        try:
            registros = conn.execute(
                """
                SELECT id, nome, email
                FROM usuarios
                ORDER BY id
                """
            ).fetchall()

            return [
                Usuario(
                    registro["id"],
                    registro["nome"],
                    registro["email"],
                )
                for registro in registros
            ]

        finally:
            conn.close()

    def buscar_por_id(self, usuario_id):
        """Busca um usuário pelo identificador."""

        conn = conectar()

        try:
            registro = conn.execute(
                """
                SELECT id, nome, email
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            ).fetchone()

            if registro is None:
                return None

            return Usuario(
                registro["id"],
                registro["nome"],
                registro["email"],
            )

        finally:
            conn.close()

    def buscar_por_email(self, email):
        """Busca um usuário pelo endereço de e-mail."""

        conn = conectar()

        try:
            registro = conn.execute(
                """
                SELECT id, nome, email
                FROM usuarios
                WHERE LOWER(TRIM(email)) = ?
                LIMIT 1
                """,
                (email.strip().lower(),),
            ).fetchone()

            if registro is None:
                return None

            return Usuario(
                registro["id"],
                registro["nome"],
                registro["email"],
            )

        finally:
            conn.close()

    def atualizar(self, usuario):
        """Atualiza o nome e o e-mail de um usuário."""

        conn = conectar()

        try:
            cursor = conn.execute(
                """
                UPDATE usuarios
                SET nome = ?, email = ?
                WHERE id = ?
                """,
                (
                    usuario.nome,
                    usuario.email,
                    usuario.id,
                ),
            )

            conn.commit()

            return cursor.rowcount > 0

        finally:
            conn.close()

    def deletar(self, usuario_id):
        """Exclui um usuário pelo identificador."""

        conn = conectar()

        try:
            cursor = conn.execute(
                """
                DELETE FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )

            conn.commit()

            return cursor.rowcount > 0

        finally:
            conn.close()
            