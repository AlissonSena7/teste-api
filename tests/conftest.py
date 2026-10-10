from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

import app.src.main as main
from app.src.main import TarefaResponse, app


@pytest.fixture(autouse=True)
def banco_limpo():
    main.tarefas_db.clear()
    main.proximo_id = 1
    yield
    main.tarefas_db.clear()
    main.proximo_id = 1


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def tarefas_base():
    base = datetime(2024, 1, 1, 10, 0, 0)
    tarefas = [
        TarefaResponse(
            id=1,
            titulo="Estudar Python",
            descricao="Revisar FastAPI",
            concluida=False,
            tags=["python", "estudo"],
            data_criacao=base,
            data_atualizacao=base,
        ),
        TarefaResponse(
            id=2,
            titulo="Fazer exercícios",
            descricao="Academia",
            concluida=True,
            tags=["saude"],
            data_criacao=base + timedelta(hours=1),
            data_atualizacao=base + timedelta(hours=2),
        ),
        TarefaResponse(
            id=3,
            titulo="Projeto Python",
            descricao="API REST",
            concluida=False,
            tags=["python", "projeto"],
            data_criacao=base + timedelta(hours=2),
            data_atualizacao=base + timedelta(hours=3),
        ),
        TarefaResponse(
            id=4,
            titulo="Ler livro",
            descricao="Clean Code",
            concluida=True,
            tags=["estudo"],
            data_criacao=base + timedelta(hours=3),
            data_atualizacao=base + timedelta(hours=4),
        ),
    ]
    main.tarefas_db.extend(tarefas)
    main.proximo_id = 5
    return tarefas
