import pytest


def test_criar_e_buscar_usuario(service):
    usuario = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    assert usuario.id is not None
    assert usuario.nome == "Arthur Santos"
    assert usuario.email == "arthur@example.com"

    encontrado = service.buscar_usuario(usuario.id)

    assert encontrado is not None
    assert encontrado.nome == "Arthur Santos"
    assert encontrado.email == "arthur@example.com"


def test_normalizar_nome_e_email(service):
    usuario = service.criar_usuario(
        "  Arthur Santos  ",
        "ARTHUR@EXAMPLE.COM",
    )

    assert usuario.nome == "Arthur Santos"
    assert usuario.email == "arthur@example.com"


def test_rejeitar_nome_vazio(service):
    with pytest.raises(ValueError):
        service.criar_usuario(
            "   ",
            "arthur@example.com",
        )


def test_rejeitar_email_invalido(service):
    with pytest.raises(ValueError):
        service.criar_usuario(
            "Arthur Santos",
            "email-invalido",
        )


def test_rejeitar_email_duplicado(service):
    service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    with pytest.raises(ValueError, match="já está cadastrado"):
        service.criar_usuario(
            "Outro Usuário",
            "ARTHUR@EXAMPLE.COM",
        )


def test_listar_usuarios(service):
    service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    service.criar_usuario(
        "Maria Silva",
        "maria@example.com",
    )

    usuarios = service.listar_usuarios()

    assert len(usuarios) == 2
    assert usuarios[0].nome == "Arthur Santos"
    assert usuarios[1].nome == "Maria Silva"


def test_atualizar_usuario(service):
    usuario = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    atualizado = service.atualizar_usuario(
        usuario.id,
        "Arthur Atualizado",
        "novo@example.com",
    )

    assert atualizado.nome == "Arthur Atualizado"
    assert atualizado.email == "novo@example.com"

    # Confirma que a alteração foi persistida no SQLite.
    encontrado = service.buscar_usuario(usuario.id)

    assert encontrado.nome == "Arthur Atualizado"
    assert encontrado.email == "novo@example.com"


def test_impedir_email_duplicado_na_atualizacao(service):
    primeiro = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    service.criar_usuario(
        "Maria Silva",
        "maria@example.com",
    )

    with pytest.raises(ValueError, match="já utiliza este e-mail"):
        service.atualizar_usuario(
            primeiro.id,
            "Arthur Santos",
            "maria@example.com",
        )


def test_deletar_usuario(service):
    usuario = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    resultado = service.deletar_usuario(usuario.id)

    assert resultado is True
    assert service.buscar_usuario(usuario.id) is None


def test_deletar_usuario_inexistente(service):
    resultado = service.deletar_usuario(9999)

    assert resultado is False


def test_buscar_usuario_inexistente(service):
    usuario = service.buscar_usuario(9999)

    assert usuario is None
