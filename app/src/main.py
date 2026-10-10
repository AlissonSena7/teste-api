from datetime import date, datetime, time
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="API de Lista de Tarefas")


class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str = ""
    tags: list[str] = Field(default_factory=list)


class TarefaUpdate(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str = ""
    concluida: bool = False
    tags: list[str] = Field(default_factory=list)


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    concluida: bool
    tags: list[str]
    data_criacao: datetime
    data_atualizacao: datetime


class PaginacaoTarefas(BaseModel):
    pagina: int
    limite: int
    total: int
    tarefas: list[TarefaResponse]


tarefas_db: list[TarefaResponse] = []
proximo_id = 1


def buscar_tarefa(tarefa_id: int) -> TarefaResponse:
    for tarefa in tarefas_db:
        if tarefa.id == tarefa_id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.post("/tarefas", response_model=TarefaResponse, status_code=201)
def criar_tarefa(dados: TarefaCreate):
    global proximo_id
    agora = datetime.now()
    tarefa = TarefaResponse(
        id=proximo_id,
        titulo=dados.titulo,
        descricao=dados.descricao,
        concluida=False,
        tags=list(dados.tags),
        data_criacao=agora,
        data_atualizacao=agora,
    )
    proximo_id += 1
    tarefas_db.append(tarefa)
    return tarefa


@app.get("/tarefas", response_model=PaginacaoTarefas)
def listar_tarefas(
    concluida: Optional[bool] = Query(None),
    tag: Optional[str] = Query(None),
    titulo: Optional[str] = Query(None),
    ordenar_por: Literal[
        "id", "titulo", "data_criacao", "data_atualizacao"
    ] = Query("id"),
    ordem: Literal["asc", "desc"] = Query("asc"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
):
    resultado = list(tarefas_db)

    if concluida is not None:
        resultado = [t for t in resultado if t.concluida == concluida]

    if tag is not None:
        resultado = [t for t in resultado if tag in t.tags]

    if titulo is not None:
        resultado = [
            t for t in resultado if titulo.lower() in t.titulo.lower()
        ]

    if data_inicio is not None:
        inicio = datetime.combine(data_inicio, time.min)
        resultado = [t for t in resultado if t.data_criacao >= inicio]

    if data_fim is not None:
        fim = datetime.combine(data_fim, time.max)
        resultado = [t for t in resultado if t.data_criacao <= fim]

    resultado.sort(
        key=lambda t: getattr(t, ordenar_por),
        reverse=(ordem == "desc"),
    )

    total = len(resultado)
    inicio_indice = (pagina - 1) * limite

    return PaginacaoTarefas(
        pagina=pagina,
        limite=limite,
        total=total,
        tarefas=resultado[inicio_indice : inicio_indice + limite],
    )


@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def obter_tarefa(tarefa_id: int):
    return buscar_tarefa(tarefa_id)


@app.put("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: TarefaUpdate):
    tarefa = buscar_tarefa(tarefa_id)
    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao
    tarefa.concluida = dados.concluida
    tarefa.tags = list(dados.tags)
    tarefa.data_atualizacao = datetime.now()
    return tarefa


@app.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int):
    tarefa = buscar_tarefa(tarefa_id)
    tarefas_db.remove(tarefa)
    return {"mensagem": "Tarefa excluída com sucesso"}
