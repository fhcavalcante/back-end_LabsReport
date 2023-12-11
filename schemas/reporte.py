from pydantic import BaseModel
from typing import Optional, List
from model.reporte import Reporte

from schemas import ComentarioSchema


class ReporteSchema(BaseModel):
    """ Representação de novo reporte
    """
    id: int = "1"
    item: str = "Reporte"
    local: str = "Local"
    autor: str = "Autor"


class ReporteBuscaSchema(BaseModel):
    """ Representação da estrutura de busca feita com base no nome do reporte.
    """
    item: str = "teste"

class ReporteBuscaIdSchema(BaseModel):
    """ Representação da estrutura de busca feita com base no ID do reporte.
    """
    id: int = "1"
  


class ListagemReportesSchema(BaseModel):
    """ Define como uma listagem de reportes será retornada.
    """
    reporte:List[ReporteSchema]


def apresenta_reportes(reportes: List[Reporte]):
    """ Retorna uma representação do reporte seguindo o schema definido em
        ReportesViewSchema.
    """
    result = []
    for reporte in reportes:
        result.append({
            "item": reporte.item,
            "local": reporte.local,
            "autor": reporte.autor,
            "id": reporte.id,
        })

    return {"reportes": result}


class ReporteViewSchema(BaseModel):
    """ Define como um reporte será retornado: reporte + comentários.
    """
    id: int = 1
    item: str = "Exemplo"
    local: str = "Laboratório"
    usuario: str = "Autor"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class ReporteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    item: str

def apresenta_reporte(reporte: Reporte):
    """ Retorna uma representação do reporte seguindo o schema definido em
        ReporteViewSchema.
    """
    return {
        "id": reporte.id,
        "item": reporte.item,
        "local": reporte.local,
        "autor": reporte.autor,
        "total_cometarios": len(reporte.comentarios),
        "comentarios": [{"texto": c.texto} for c in reporte.comentarios]
    }
