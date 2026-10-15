# UserFlow — Sistema de Gerenciamento de Usuários

Aplicação web desenvolvida em Python para gerenciamento de usuários, utilizando Flask e SQLite.

O projeto tem como objetivo aplicar conceitos de desenvolvimento web, operações CRUD, organização de código, persistência de dados, validação de informações, segurança e testes automatizados.

## Funcionalidades

- **Cadastro:** registro de novos usuários.
- **Consulta:** visualização dos usuários cadastrados.
- **Pesquisa:** busca de usuários pelo nome.
- **Edição:** atualização dos dados de um usuário.
- **Exclusão:** remoção de usuários cadastrados.
- **Validação de dados:** tratamento de informações inválidas e prevenção de e-mails duplicados.
- **Proteção CSRF:** proteção dos formulários contra requisições que não apresentam o token esperado.
- **Tratamento de erros:** página personalizada para recursos não encontrados.

## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem utilizada no desenvolvimento. |
| Flask | Framework responsável pela aplicação web. |
| SQLite | Banco de dados relacional para persistência dos usuários. |
| HTML | Estrutura das páginas da interface. |
| CSS | Estilização da interface. |
| Flask-WTF | Proteção CSRF dos formulários. |
| python-dotenv | Carregamento de variáveis de ambiente a partir do arquivo `.env`. |
| pytest | Execução dos testes automatizados. |


## Estrutura do projeto

```text
primeiro-crud/
├── app.py
├── database.py
├── models/
│   └── usuarios.py
├── repositories/
│   └── usuario_repository.py
├── services/
│   └── usuario_service.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── 404.html
│   ├── base.html
│   ├── csrf_error.html
│   ├── formulario.html
│   └── index.html
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   └── test_usuario_service.py
├── .gitignore
├── requirements.txt
└── README.md
```

> **Observação:** o arquivo `.env` é utilizado localmente e não deve ser enviado ao repositório público. A estrutura acima representa os principais arquivos do projeto; arquivos auxiliares podem existir no ambiente de desenvolvimento.

### Organização do código

- **`app.py`:** inicialização e configuração da aplicação Flask, além das rotas da interface.
- **`database.py`:** configuração da conexão e criação da tabela do banco de dados.
- **`models/`:** representação dos dados dos usuários.
- **`repositories/`:** operações de acesso e persistência dos dados.
- **`services/`:** regras de negócio e validações.
- **`templates/`:** páginas HTML renderizadas pela aplicação.
- **`static/css/`:** estilos da interface.
- **`tests/`:** testes automatizados da aplicação e das regras de negócio.

## Pré-requisitos

Antes de executar o projeto, instale:

- Python 3.11 ou compatível com as dependências.
- Git, caso queira clonar o repositório.
- Um editor de código, como o Visual Studio Code.

## Como executar o projeto

### 1. Clone o repositório

git clone https://github.com/sonArthur/primeiro-crud.git

Entre na pasta do projeto:

cd primeiro-crud

### 2. Crie um ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto.

Adicione a seguinte configuração:

```env
FLASK_SECRET_KEY=SUBSTITUA_POR_UMA_CHAVE_SECRETA
FLASK_DEBUG=true
```

Substitua `SUBSTITUA_POR_UMA_CHAVE_SECRETA` por uma chave secreta própria e segura.

**Importante:**
- Não compartilhe sua chave secreta.
- Não publique o arquivo `.env` no GitHub.
- O modo de depuração deve ser utilizado apenas no ambiente de desenvolvimento.

### 5. Inicie a aplicação

Execute:

```powershell
python app.py
```

Abra o endereço abaixo no navegador:

```text
http://127.0.0.1:5000
```

O endereço é local: a aplicação estará acessível na máquina em que estiver sendo executada.

## Testes automatizados

O projeto possui testes automatizados para verificar o comportamento das funcionalidades e das regras de negócio.

Para executar a suíte completa:

```powershell
python -m pytest -v
```

Os testes cobrem cenários como:

- Cadastro e consulta de usuários.
- Pesquisa pelo nome.
- Edição e exclusão de registros.
- Validação de dados.
- Prevenção de e-mails duplicados.
- Tratamento de usuários inexistentes.
- Proteção CSRF nos formulários.

**Última verificação registrada durante o desenvolvimento:** 19 testes passaram.

Esse resultado corresponde à execução realizada durante o desenvolvimento e pode mudar caso o código seja alterado.

## Segurança e boas práticas

Durante o desenvolvimento, foram aplicadas práticas como:

- Proteção CSRF nos formulários.
- Uso de variável de ambiente para a chave secreta.
- Exclusão de arquivos sensíveis e artefatos locais por meio do `.gitignore`.
- Separação entre interface, regras de negócio e acesso aos dados.
- Testes automatizados para verificar comportamentos esperados.

O projeto é destinado a fins educacionais e de portfólio. Antes de utilizá-lo em produção, seria necessário avaliar requisitos adicionais de segurança, configuração e implantação.

## Objetivos de aprendizagem

Este projeto foi desenvolvido para praticar conceitos relacionados a:

- Desenvolvimento de aplicações web com Python.
- Operações CRUD (*Create, Read, Update, Delete*).
- Persistência de dados com SQLite.
- Organização em camadas.
- Validação de informações.
- Segurança de formulários.
- Testes automatizados.
- Controle de versão com Git e GitHub.

## Autor

Desenvolvido por **Arthur Santana Santos**.

[Visite meu perfil no GitHub](https://github.com/sonArthur)



