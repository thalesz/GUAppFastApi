from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response

from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import JSONResponse

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from models.usuario_model import UsuarioModel

from schemas.usuario_schema import UsuarioSchema, UsuarioSchemaCreate, UsuarioSchemaArtigos, UsuarioSchemaUp

from core.deps import get_session, get_current_user

from core.security import gerar_hash_snha

from core.auth import autenticar, criar_token_acesso


router = APIRouter()

#Get Logado

@router.get('/logado', response_model=UsuarioSchema)
def get_logado(usuario_logado:UsuarioModel=Depends(get_current_user)):
    return usuario_logado

#Post /signup

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)

async def signup(usuario: UsuarioSchemaCreate, db: AsyncSession=Depends(get_session)):
    novo_usuario:UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_snha(usuario.senha)
    )
    
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado")
    

# GET Usuarios

@router.get('/', response_model=List[UsuarioSchema])
async def get_usuarios(db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchema]= result.scalars().unique().all()
        return usuarios
    
#GET Usuario

@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):  # Alterado para int
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: Optional[UsuarioModel] = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")
        
        return usuario

@router.put('/{usuario_id}', response_model=UsuarioSchemaUp, status_code=status.HTTP_202_ACCEPTED)
async def update_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):  # Alterado para int
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaUp = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_snha(usuario.senha)

            await session.commit()
            return usuario_up
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")

@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):  # Alterado para int
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")
     
        
#POST Login

@router.post('/login', response_model=UsuarioSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_session)):
    usuario = await autenticar(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciais inválidas")
    
    return JSONResponse(content={"access_token":criar_token_acesso(sub=usuario.id), 'token_type':'bearer'}, status_code=status.HTTP_200_OK)



