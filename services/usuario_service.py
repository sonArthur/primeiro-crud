from models.usuarios import Usuario

class UsuarioService:
    def __init__(self):
        self.usuarios = []
        self.proximo_id = 1

    def criar_usuario(self, nome, email):
        usuario = Usuario(self.proximo_id, nome, email)
        self.usuarios.append(usuario)
        self.proximo_id += 1
        return usuario

    def listar_usuarios(self):
        return self.usuarios

    def buscar_usuario(self, id):
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None

    def atualizar_usuario(self, id, novo_nome, novo_email):
        usuario = self.buscar_usuario(id)
        if usuario:
            usuario.nome = novo_nome
            usuario.email = novo_email
            return usuario
        return None

    def deletar_usuario(self, id):
        usuario = self.buscar_usuario(id)
        if usuario:
            self.usuarios.remove(usuario)
            return True
        return False
    