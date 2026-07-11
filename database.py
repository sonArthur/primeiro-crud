import sqlite3
import datetime

data = datetime.datetime.now().isoformat()

def conectar():
    return sqlite3.connect("usuarios.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    