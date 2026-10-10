import pytest

CAMPOS_TAREFA = {
    "id",
    "titulo",
    "descricao",
    "concluida",
    "tags",
    "data_criacao",
    "data_atualizacao",
}


def ids_da_resposta(response):
    return [tarefa["id"] for tarefa in response.json()["tarefas"]]


# ---------------------------------------------------------------------------
# 5.1 Criacao - POST /tarefas
# ---------------------------------------------------------------------------


def test_criar_tarefa_valida_retorna_201_com_todos_os_campos(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "Estudar FastAPI",
            "descricao": "Revisar rotas",
            "tags": ["python"],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert CAMPOS_TAREFA.issubset(data.keys())


def test_criar_tarefa_gera_identificador_automaticamente(client):
    primeira = client.post("/tarefas", json={"titulo": "Primeira"}).json()
    segunda = client.post("/tarefas", json={"titulo": "Segunda"}).json()

    assert primeira["id"] == 1
    assert segunda["id"] == 2


def test_criar_tarefa_inicia_como_nao_concluida(client):
    response = client.post("/tarefas", json={"titulo": "Pendente"})

    assert response.status_code == 201
    assert response.json()["concluida"] is False


def test_criar_tarefa_preenche_datas_automaticamente(client):
    data = client.post("/tarefas", json={"titulo": "Com datas"}).json()

    assert data["data_criacao"]
    assert data["data_atualizacao"]
    assert data["data_criacao"] == data["data_atualizacao"]


def test_criar_tarefa_com_multiplas_tags(client):
    tags = ["python", "fastapi", "testes"]
    response = client.post(
        "/tarefas", json={"titulo": "Multitags", "tags": tags}
    )

    assert response.status_code == 201
    assert response.json()["tags"] == tags


def test_criar_tarefa_aplica_valores_padrao(client):
    data = client.post("/tarefas", json={"titulo": "Somente titulo"}).json()

    assert data["descricao"] == ""
    assert data["tags"] == []


def test_criar_tarefa_sem_titulo_retorna_422(client):
    response = client.post("/tarefas", json={"descricao": "sem titulo"})

    assert response.status_code == 422


def test_criar_tarefa_com_titulo_vazio_retorna_422(client):
    response = client.post("/tarefas", json={"titulo": ""})

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 5.2 Consulta da lista - GET /tarefas
# ---------------------------------------------------------------------------


def test_listar_tarefas_vazio(client):
    response = client.get("/tarefas")

    assert response.status_code == 200
    data = response.json()
    assert data["tarefas"] == []
    assert data["total"] == 0


def test_listar_tarefas_retorna_todas(client, tarefas_base):
    response = client.get("/tarefas", params={"limite": 100})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == len(tarefas_base)
    assert len(data["tarefas"]) == len(tarefas_base)
    assert ids_da_resposta(response) == [1, 2, 3, 4]


def test_listar_tarefas_cada_item_tem_os_campos_esperados(client, tarefas_base):
    response = client.get("/tarefas", params={"limite": 100})

    for tarefa in response.json()["tarefas"]:
        assert CAMPOS_TAREFA.issubset(tarefa.keys())


def test_listar_tarefas_total_corresponde_a_quantidade(client):
    for indice in range(3):
        client.post("/tarefas", json={"titulo": f"Tarefa {indice}"})

    data = client.get("/tarefas").json()

    assert data["total"] == 3
    assert len(data["tarefas"]) == 3


# ---------------------------------------------------------------------------
# 5.3 Consulta por identificador - GET /tarefas/{id}
# ---------------------------------------------------------------------------


def test_obter_tarefa_existente(client, tarefas_base):
    response = client.get("/tarefas/2")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["titulo"] == "Fazer exercícios"
    assert data["descricao"] == "Academia"
    assert data["concluida"] is True
    assert data["tags"] == ["saude"]


def test_obter_tarefa_inexistente_retorna_404(client):
    response = client.get("/tarefas/999999")

    assert response.status_code == 404
    assert "detail" in response.json()


# ---------------------------------------------------------------------------
# 5.4 Atualizacao - PUT /tarefas/{id}
# ---------------------------------------------------------------------------


def test_atualizar_titulo_e_descricao(client, tarefas_base):
    response = client.put(
        "/tarefas/1",
        json={
            "titulo": "Titulo novo",
            "descricao": "Descricao nova",
            "concluida": False,
            "tags": ["python", "estudo"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Titulo novo"
    assert data["descricao"] == "Descricao nova"


def test_atualizar_concluida_para_true(client, tarefas_base):
    response = client.put(
        "/tarefas/1",
        json={"titulo": "Estudar Python", "descricao": "Revisar", "concluida": True},
    )

    assert response.status_code == 200
    assert response.json()["concluida"] is True


def test_atualizar_tags(client, tarefas_base):
    response = client.put(
        "/tarefas/1",
        json={"titulo": "Estudar Python", "tags": ["python", "novo"]},
    )

    assert response.status_code == 200
    assert response.json()["tags"] == ["python", "novo"]


def test_atualizar_muda_data_atualizacao_e_mantem_criacao(client, tarefas_base):
    original = client.get("/tarefas/1").json()

    atualizado = client.put(
        "/tarefas/1",
        json={"titulo": "Estudar Python", "concluida": True},
    ).json()

    assert atualizado["data_criacao"] == original["data_criacao"]
    assert atualizado["data_atualizacao"] != original["data_atualizacao"]


def test_atualizar_tarefa_inexistente_retorna_404(client):
    response = client.put("/tarefas/999999", json={"titulo": "Nao existe"})

    assert response.status_code == 404
    assert "detail" in response.json()


def test_atualizar_sem_titulo_retorna_422(client, tarefas_base):
    response = client.put("/tarefas/1", json={"descricao": "sem titulo"})

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# 5.5 Exclusao - DELETE /tarefas/{id}
# ---------------------------------------------------------------------------


def test_excluir_tarefa_existente(client, tarefas_base):
    response = client.delete("/tarefas/1")

    assert response.status_code == 200
    assert "mensagem" in response.json()


def test_excluir_tarefa_remove_da_listagem(client, tarefas_base):
    client.delete("/tarefas/1")

    ids = ids_da_resposta(client.get("/tarefas", params={"limite": 100}))
    assert 1 not in ids
    assert ids == [2, 3, 4]


def test_excluir_tarefa_depois_consulta_retorna_404(client, tarefas_base):
    client.delete("/tarefas/1")

    assert client.get("/tarefas/1").status_code == 404


def test_excluir_tarefa_inexistente_retorna_404(client):
    response = client.delete("/tarefas/999999")

    assert response.status_code == 404
    assert "detail" in response.json()


# ---------------------------------------------------------------------------
# 5.6 Filtros - GET /tarefas
# ---------------------------------------------------------------------------


def test_filtro_concluida_true(client, tarefas_base):
    response = client.get(
        "/tarefas", params={"concluida": True, "limite": 100}
    )

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [2, 4]
    assert all(t["concluida"] is True for t in tarefas)


def test_filtro_concluida_false(client, tarefas_base):
    response = client.get(
        "/tarefas", params={"concluida": False, "limite": 100}
    )

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [1, 3]
    assert all(t["concluida"] is False for t in tarefas)


def test_filtro_concluida_sem_resultados(client):
    client.post("/tarefas", json={"titulo": "Pendente"})

    data = client.get("/tarefas", params={"concluida": True}).json()

    assert data["total"] == 0
    assert data["tarefas"] == []


def test_filtro_tag(client, tarefas_base):
    response = client.get("/tarefas", params={"tag": "python", "limite": 100})

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [1, 3]
    assert all("python" in t["tags"] for t in tarefas)


def test_filtro_tag_sem_resultados(client, tarefas_base):
    data = client.get("/tarefas", params={"tag": "inexistente"}).json()

    assert data["total"] == 0
    assert data["tarefas"] == []


def test_filtro_titulo_contem_texto(client, tarefas_base):
    response = client.get(
        "/tarefas", params={"titulo": "python", "limite": 100}
    )

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [1, 3]
    assert all("python" in t["titulo"].lower() for t in tarefas)


def test_filtro_titulo_sem_resultados(client, tarefas_base):
    data = client.get("/tarefas", params={"titulo": "inexistente"}).json()

    assert data["total"] == 0
    assert data["tarefas"] == []


# ---------------------------------------------------------------------------
# 5.7 Combinacao de filtros
# ---------------------------------------------------------------------------


def test_combinacao_concluida_false_e_tag(client, tarefas_base):
    response = client.get(
        "/tarefas",
        params={"concluida": False, "tag": "python", "limite": 100},
    )

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [1, 3]
    assert all(t["concluida"] is False for t in tarefas)
    assert all("python" in t["tags"] for t in tarefas)


def test_combinacao_filtros_com_ordenacao(client, tarefas_base):
    response = client.get(
        "/tarefas",
        params={
            "concluida": False,
            "tag": "python",
            "ordenar_por": "data_criacao",
            "ordem": "desc",
            "limite": 100,
        },
    )

    tarefas = response.json()["tarefas"]
    assert [t["id"] for t in tarefas] == [3, 1]
    assert all(t["concluida"] is False for t in tarefas)
    assert all("python" in t["tags"] for t in tarefas)


# ---------------------------------------------------------------------------
# 5.8 Ordenacao
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "campo, ordem, esperado",
    [
        ("data_criacao", "asc", [1, 2, 3, 4]),
        ("data_criacao", "desc", [4, 3, 2, 1]),
        ("data_atualizacao", "asc", [1, 2, 3, 4]),
        ("data_atualizacao", "desc", [4, 3, 2, 1]),
        ("titulo", "asc", [1, 2, 4, 3]),
        ("titulo", "desc", [3, 4, 2, 1]),
        ("id", "asc", [1, 2, 3, 4]),
        ("id", "desc", [4, 3, 2, 1]),
    ],
)
def test_ordenacao(client, tarefas_base, campo, ordem, esperado):
    response = client.get(
        "/tarefas",
        params={"ordenar_por": campo, "ordem": ordem, "limite": 100},
    )

    assert response.status_code == 200
    assert ids_da_resposta(response) == esperado


# ---------------------------------------------------------------------------
# 5.9 Validacao e tratamento de erros
# ---------------------------------------------------------------------------


def test_concluida_com_tipo_invalido_retorna_422(client, tarefas_base):
    response = client.put(
        "/tarefas/1",
        json={"titulo": "Estudar Python", "concluida": "texto"},
    )

    assert response.status_code == 422


def test_ordenar_por_invalido_retorna_422(client):
    response = client.get("/tarefas", params={"ordenar_por": "invalido"})

    assert response.status_code == 422


def test_ordem_invalida_retorna_422(client):
    response = client.get("/tarefas", params={"ordem": "crescente"})

    assert response.status_code == 422


def test_limite_invalido_retorna_422(client):
    response = client.get("/tarefas", params={"limite": 0})

    assert response.status_code == 422


def test_pagina_invalida_retorna_422(client):
    response = client.get("/tarefas", params={"pagina": 0})

    assert response.status_code == 422


def test_erro_de_validacao_tem_estrutura_padrao(client):
    response = client.post("/tarefas", json={})

    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)
