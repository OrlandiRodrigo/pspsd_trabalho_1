import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verificar_senha(senha_texto_puro: str, senha_hashada: str) -> bool:
    return pwd_context.verify(senha_texto_puro, senha_hashada)


def obter_hash_senha(senha: str) -> str:
    """
    Gera um hash argon2 para a senha fornecida.
    """
    return pwd_context.hash(senha)


SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "A variável SECRET_KEY não foi definida. A aplicação não pode iniciar."
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def criar_token_acesso(dados: dict, expira_em: Optional[timedelta] = None):
    copia_dados = dados.copy()

    if expira_em:
        horario_expiracao = datetime.now(timezone.utc) + expira_em
    else:
        horario_expiracao = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    copia_dados.update({"exp": horario_expiracao})

    token_jwt_codificado = jwt.encode(copia_dados, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt_codificado


def verificar_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
