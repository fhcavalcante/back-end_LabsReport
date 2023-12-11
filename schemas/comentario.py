from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    
    """ Representação de um novo comentário
    """
    reporte_id: str = "Exemplo"
    texto: str = "Reporte"
