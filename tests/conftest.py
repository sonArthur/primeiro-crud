import sqlite3

import pytest

from services.usuario_service import UsuarioService


@pytest.fixture
def banco_teste(tmp_path, monkeypatch):
    """
    Cria um banco SQLite temporário para cada teste.

    Os testes não utilizam o usuarios.db real.
    """

    caminho_db = tmp_path / "usuarios_teste.db"

    def conectar_teste():
        conn = sqlite3.connect(caminho_db)
        conn.row_factory = sqlite3.Row
        return conn

    # Redireciona o repositório para o banco temporário.
    monkeypatch.setattr(
        "repositories.usuario_repository.conectar",
        conectar_teste,
    )

    # Cria a tabela no banco de teste.
    conn = conectar_teste()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        conn.commit()

    finally:
        conn.close()

    return caminho_db


@pytest.fixture
def service(banco_teste):
    """
    Fornece uma instância do serviço para cada teste.
    """

    return UsuarioService()
