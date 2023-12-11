from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Reporte(Base):
    __tablename__ = 'reporte'

    id = Column("pk_reporte", Integer, primary_key=True)
    item = Column(String(140), unique=True)
    local = Column(String(140), unique=True)
    autor = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    comentarios = relationship("Comentario")

    def __init__(self, item:str, local:str, autor:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Reporte

        Arguments:
            item: item do reporte.
            local: local do reporte
            autor: autor do reporte
            data_insercao: data de quando o reporte foi inserido à base
        """
        
        self.item = item
        self.local = local
        self.autor = autor

    
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Reporte
        """
        self.comentarios.append(comentario)

