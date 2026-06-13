# pylint: disable=duplicate-code
from typing import Optional

from sqlalchemy.orm import Session

from .. import models
from .. import seguranca as seguranca_service


def autenticar_cliente(
    sessao_banco: Session, email_formulario: str, senha_formulario: str
) -> Optional[models.Pessoa]:
    cliente_encontrado = (
        sessao_banco.query(models.Pessoa)
        .filter(models.Pessoa.email == email_formulario)
        .first()
    )
    if not cliente_encontrado:
        return None

    if not cliente_encontrado.e_ativo:
        return None

    if not seguranca_service.verificar_senha(
        senha_texto_puro=senha_formulario, senha_hashada=cliente_encontrado.senha
    ):
        return None

    return cliente_encontrado
