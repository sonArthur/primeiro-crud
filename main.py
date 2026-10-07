from services.usuario_service import UsuarioService

def menu():
    service = UsuarioService()

    while True:
        print("\n=== CRUD DE USUÁRIOS ===")
        print("1. Criar usuário")
        print("2. Listar usuários")
        print("3. Atualizar usuário")
        print("4. Deletar usuário")
        print("0. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            usuario = service.criar_usuario(nome, email)
            print("Usuário criado:", usuario)

        elif opcao == "2":
            usuarios = service.listar_usuarios()
            for u in usuarios:
                print(u)

        elif opcao == "3":
            id = int(input("ID do usuário: "))
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            usuario = service.atualizar_usuario(id, nome, email)
            if usuario:
                print("Atualizado:", usuario)
            else:
                print("Usuário não encontrado")

        elif opcao == "4":
            id = int(input("ID do usuário: "))
            if service.deletar_usuario(id):
                print("Usuário deletado")
            else:
                print("Usuário não encontrado")

        elif opcao == "0":
            break

        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu()
    