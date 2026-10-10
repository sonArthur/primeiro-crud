import sqlite3
from pathlib import Path


# Caminho absoluto para o banco de dados.
# Isso evita que a localização do arquivo dependa
# da pasta em que o programa foi iniciado.
DB_PATH = Path(__file__).resolve().parent / "usuarios.db"


def conectar():
    """Cria uma conexão com o banco SQLite."""

    conn = sqlite3.connect(DB_PATH)

    # Permite acessar os resultados pelo nome da coluna.
    conn.row_factory = sqlite3.Row

    return conn


def criar_tabela():
    """Cria a tabela de usuários caso ela não exista."""

    conn = conectar()

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
