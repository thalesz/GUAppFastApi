from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema

from core.deps import get_session, get_current_user

router = APIRouter()

# POST Artigo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema, 
    usuario_logado: UsuarioModel = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo, 
        descricao=artigo.descricao, 
        url_fonte=artigo.url_fonte, 
        usuario_id=usuario_logado.id  # Associando o usuário autenticado
    )
    db.add(novo_artigo)
    await db.commit()
    await db.refresh(novo_artigo)
    return novo_artigo

# Get Artigos 

@router.get('/', response_model=List[ArtigoSchema])

async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos = result.scalars().unique().all()
        return artigos
    

#Get artigo

@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)

async def get_artigo(
    artigo_id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo = result.scalars().first()
        if not artigo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
        return artigo
    
#PUT Artigo
@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)

async def put_artigo(
    artigo_id: int, 
    artigo: ArtigoSchema, 
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel=Depends(get_current_user)
    ):
    
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_existente = result.scalars().first()
        
        if artigo_existente:
            if artigo.titulo:
                artigo_existente.titulo = artigo.titulo
            if artigo.descricao:
                artigo_existente.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_existente.url_fonte = artigo.url_fonte
            if usuario_logado.id != artigo_existente.usuario_id:
                artigo_existente.usuario_id = usuario_logado.id

                
            await session.commit()
            return artigo_existente
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")  
        
#DELETE Artigo

@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    artigo_id: int, 
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):

    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo_existente = result.scalars().first()

        if artigo_existente:
            if usuario_logado.id == artigo_existente.usuario_id:
                await session.delete(artigo_existente)  # Correção aqui: use session.delete() ao invés de db.delete()
                await session.commit()  # Commit da transação
                return None  # Não é necessário retornar nada, o status 204 é implicitamente retornado
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não tem permissão para deletar esse artigo")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado")
