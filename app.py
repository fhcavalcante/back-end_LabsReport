from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Reporte, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="API LabsReport", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
reporte_tag = Tag(name="Reporte", description="Adição, visualização e remoção de reportes à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um reporte cadastrado na base")


@app.get('/', tags=[home_tag])
def home():

    """Redirecionamento para a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/reporte', tags=[reporte_tag],
          responses={"200": ReporteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_reporte(form: ReporteSchema):
    """Adiciona um novo reporte à base de dados
    Retorna uma representação dos reportes e comentários associados."""
    reporte = Reporte(
     
        item=form.item,
        local=form.local,
        autor=form.autor)
    logger.debug(f"Adicionando reporte de nome: '{reporte.item}'")
    try:
        # conexão com a base
        session = Session()
        # adiciona reporte
        session.add(reporte)
        # comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado reporte de nome: '{reporte.item}'")
        return apresenta_reporte(reporte), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Reporte de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar reporte '{reporte.item}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # para um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar reporte '{reporte.item}', {error_msg}")
        return {"mensagem": error_msg}, 400


@app.get('/listareportes', tags=[reporte_tag],
         responses={"200": ListagemReportesSchema, "404": ErrorSchema})
def get_lista():
    """Busca pelos reportes cadastrados
    Retorna uma representação da listagem de reportes."""
    logger.debug(f"Coletando reporte ")
    # conexão com a base
    session = Session()
    # busca
    lista = session.query(Reporte).all()

    if not lista:
        # se não há reporte cadastrados
        return {"reportes": []}, 200
    else:
        logger.debug(f"%d Reportes encontrados" % len(lista))
        # retorna a representação de reporte
        print(lista)
        return apresenta_reportes(lista), 200


@app.get('/reporte', tags=[reporte_tag],
         responses={"200": ReporteViewSchema, "404": ErrorSchema})
def get_reporte(query: ReporteBuscaIdSchema):
    """Faz a busca por um reporte a partir do id do reporte
    Retorna uma representação dos reporte e comentários associados."""
    reporte_id = query.id
    logger.debug(f"Coletando dados sobre reporte #{reporte_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    reporte = session.query(Reporte).filter(Reporte.id == reporte_id).first()

    if not reporte:
        # se o reporte não foi encontrado
        error_msg = "Reporte não encontrado na base :/"
        logger.warning(f"Erro ao buscar reporte '{reporte_id}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(f"Reporte encontrado: '{reporte.item}'")
        # retorna a representação de reporte
        return apresenta_reporte(reporte), 200



@app.delete('/reporte', tags=[reporte_tag],
            responses={"200": ReporteDelSchema, "404": ErrorSchema})
def del_reporte(query: ReporteBuscaSchema):

    """Deleta um reporte
    Retorna uma mensagem de confirmação da remoção."""

    reporte_item = unquote(unquote(query.item))
    print(reporte_item)
    logger.debug(f"Deletando dados do reporte #{reporte_item}")
    # cria conexão com a base
    session = Session()
    # faz a remoção
    count = session.query(Reporte).filter(Reporte.item == reporte_item).delete()
    session.commit()

    if count:
        # representação da mensagem de confirmação
        logger.debug(f"Deletado reporte #{reporte_item}")
        return {"mensagem": "Reporte removido", "reporte": reporte_item}
    else:
        # se não encontrar o reporte
        error_msg = "Reporte não encontrado na base :/"
        logger.warning(f"Erro ao deletar reporte #'{reporte_item}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": ReporteViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    
    """Novo comentário à um reporte cadastrado na base identificado pelo id

    Retorna uma representação dos reporte e comentários associados.
    """
    
    reporte_id  = form.reporte_id
    logger.debug(f"Adicionando comentários ao reporte #{reporte_id}")
    # conexão com a base
    session = Session()
    # busca reporte
    reporte = session.query(Reporte).filter(Reporte.id == reporte_id).first()

    if not reporte:
        # se reporte não encontrado
        error_msg = "Reporte não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao reporte '{reporte_id}', {error_msg}")
        return {"mensagem": error_msg}, 404

    # cria comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adiciona o comentário ao reporte
    reporte.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao reporte #{reporte_id}")

    # representação de reporte
    return apresenta_reporte(reporte), 200
