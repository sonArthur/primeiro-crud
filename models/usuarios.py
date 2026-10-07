class Usuario:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | Email: {self.email}"

    