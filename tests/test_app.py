import re

import pytest

import app as flask_app


def obter_token_csrf(response):
    """Extrai o token CSRF de uma página HTML."""

    html = response.get_data(as_text=True)

    correspondencia = re.search(
        r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"',
        html,
    )

    assert correspondencia is not None, (
        "Token CSRF não encontrado no formulário."
    )

    return correspondencia.group(1)


@pytest.fixture
def client(service, monkeypatch):
    """Cria um cliente de testes com banco isolado."""

    monkeypatch.setattr(
        flask_app,
        "service",
        service,
    )

    flask_app.app.config.update(
        TESTING=True,
        SECRET_KEY="chave-secreta-exclusiva-dos-testes",
        WTF_CSRF_ENABLED=True,
    )

    with flask_app.app.test_client() as test_client:
        yield test_client


def test_pagina_inicial(client):
    response = client.get("/")

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Lista de usuários" in conteudo
    assert "Nenhum usuário cadastrado" in conteudo


def test_cadastrar_usuario_pela_interface(client, service):
    formulario = client.get("/usuarios/novo")

    token = obter_token_csrf(formulario)

    response = client.post(
        "/usuarios/novo",
        data={
            "nome": "Arthur Santos",
            "email": "arthur@example.com",
            "csrf_token": token,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Arthur Santos" in conteudo
    assert "arthur@example.com" in conteudo

    assert len(service.listar_usuarios()) == 1


def test_rejeitar_email_duplicado_pela_interface(
    client,
    service,
):
    service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    formulario = client.get("/usuarios/novo")

    token = obter_token_csrf(formulario)

    response = client.post(
        "/usuarios/novo",
        data={
            "nome": "Outro Usuário",
            "email": "ARTHUR@EXAMPLE.COM",
            "csrf_token": token,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Este e-mail já está cadastrado." in conteudo
    assert len(service.listar_usuarios()) == 1


def test_pesquisar_usuario_por_nome(client, service):
    service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    service.criar_usuario(
        "Maria Silva",
        "maria@example.com",
    )

    response = client.get("/?q=Maria")

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Maria Silva" in conteudo
    assert "Arthur Santos" not in conteudo


def test_editar_usuario_pela_interface(client, service):
    usuario = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    formulario = client.get(
        f"/usuarios/{usuario.id}/editar"
    )

    token = obter_token_csrf(formulario)

    response = client.post(
        f"/usuarios/{usuario.id}/editar",
        data={
            "nome": "Arthur Atualizado",
            "email": "novo@example.com",
            "csrf_token": token,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Arthur Atualizado" in conteudo
    assert "novo@example.com" in conteudo

    atualizado = service.buscar_usuario(usuario.id)

    assert atualizado.nome == "Arthur Atualizado"
    assert atualizado.email == "novo@example.com"


def test_excluir_usuario_pela_interface(client, service):
    usuario = service.criar_usuario(
        "Arthur Santos",
        "arthur@example.com",
    )

    pagina = client.get("/")

    token = obter_token_csrf(pagina)

    response = client.post(
        f"/usuarios/{usuario.id}/excluir",
        data={"csrf_token": token},
        follow_redirects=True,
    )

    assert response.status_code == 200

    conteudo = response.get_data(as_text=True)

    assert "Usuário excluído com sucesso!" in conteudo
    assert service.buscar_usuario(usuario.id) is None


def test_editar_usuario_inexistente_retorna_404(client):
    response = client.get("/usuarios/9999/editar")

    assert response.status_code == 404

    conteudo = response.get_data(as_text=True)

    assert "Não encontramos essa página." in conteudo


def test_rejeitar_post_sem_token_csrf(client):
    response = client.post(
        "/usuarios/novo",
        data={
            "nome": "Usuário Teste",
            "email": "teste@example.com",
        },
    )

    assert response.status_code == 400

    conteudo = response.get_data(as_text=True)

    assert "Não foi possível validar o formulário." in conteudo
