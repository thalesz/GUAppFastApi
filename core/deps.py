from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel

class TokenData(BaseModel):
    username: Optional[str] = None  # Corrigido para 'username'

async def get_session() -> AsyncGenerator:
    async with Session() as session:  # Usando "async with" para garantir o fechamento da sessão
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    db: AsyncSession = Depends(get_session), 
    token: str = Depends(oauth2_schema)
) -> UsuarioModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificando o token JWT
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM],
            options={'verify_aud': False}
        )
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        # Instanciando TokenData corretamente
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    # Acessando a base de dados
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))  # Corrigido para username
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
        if usuario is None:
            raise credential_exception
    
    # Retornando o usuário
    return usuario
