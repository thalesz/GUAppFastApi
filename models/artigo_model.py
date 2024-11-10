from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class ArtigoModel(settings.DBBaseModel):
    __tablename__ = 'artigos'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Alterando para String(256) para armazenar texto com comprimento máximo de 256 caracteres
    titulo = Column(String(256), nullable=False)  # Definir tamanho para a string, se necessário
    
    url_fonte = Column(String(256))
    descricao = Column(String(256))
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    
    # Relacionamento com a tabela 'UsuarioModel'
    criador = relationship("UsuarioModel", back_populates='artigos', lazy='joined')
