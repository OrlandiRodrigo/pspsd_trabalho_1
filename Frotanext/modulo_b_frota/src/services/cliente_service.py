from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from .. import seguranca as seguranca_service
from ..models.enums import StatusContaEnum
from ..schemas import cliente_schema


def criar_pessoa_fisica(
    dados_entrada_cliente: cliente_schema.SchemaPessoaFisicaCriar, sessao_banco: Session
) -> models.PessoaFisica:
    email_existente = (
        sessao_banco.query(models.Pessoa)
        .filter(models.Pessoa.email == dados_entrada_cliente.email)
        .first()
    )
    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado."
        )

    cpf_existente = (
        sessao_banco.query(models.PessoaFisica)
        .filter(models.PessoaFisica.cpf == dados_entrada_cliente.cpf)
        .first()
    )
    if cpf_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado."
        )

    cnh_existente = (
        sessao_banco.query(models.PessoaFisica)
        .filter(models.PessoaFisica.cnh == dados_entrada_cliente.cnh)
        .first()
    )
    if cnh_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CNH já cadastrada."
        )

    novo_endereco_modelo = models.Endereco(
        **dados_entrada_cliente.endereco.model_dump()
    )

    hash_senha = seguranca_service.obter_hash_senha(
        dados_entrada_cliente.senha_texto_puro
    )

    dados_pessoa_fisica = dados_entrada_cliente.model_dump(
        exclude={"endereco", "senha_texto_puro"}
    )

    nova_pessoa_fisica_modelo = models.PessoaFisica(
        **dados_pessoa_fisica, senha=hash_senha
    )

    nova_pessoa_fisica_modelo.endereco = novo_endereco_modelo

    sessao_banco.add(nova_pessoa_fisica_modelo)
    sessao_banco.commit()
    sessao_banco.refresh(nova_pessoa_fisica_modelo)

    return nova_pessoa_fisica_modelo


def criar_pessoa_juridica(
    dados_entrada_empresa: cliente_schema.SchemaPessoaJuridicaCriar,
    sessao_banco: Session,
) -> models.PessoaJuridica:
    email_existente = (
        sessao_banco.query(models.Pessoa)
        .filter(models.Pessoa.email == dados_entrada_empresa.email)
        .first()
    )
    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado."
        )

    cnpj_existente = (
        sessao_banco.query(models.PessoaJuridica)
        .filter(models.PessoaJuridica.cnpj == dados_entrada_empresa.cnpj)
        .first()
    )
    if cnpj_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="CNPJ já cadastrado."
        )

    novo_endereco_modelo = models.Endereco(
        **dados_entrada_empresa.endereco.model_dump()
    )

    hash_senha = seguranca_service.obter_hash_senha(
        dados_entrada_empresa.senha_texto_puro
    )

    dados_empresa = dados_entrada_empresa.model_dump(
        exclude={"endereco", "motoristas_ids", "senha_texto_puro"}
    )

    nova_empresa_modelo = models.PessoaJuridica(**dados_empresa, senha=hash_senha)

    nova_empresa_modelo.endereco = novo_endereco_modelo

    if dados_entrada_empresa.motoristas_ids:
        motoristas_encontrados = (
            sessao_banco.query(models.PessoaFisica)
            .filter(
                models.PessoaFisica.id_pessoa.in_(dados_entrada_empresa.motoristas_ids)
            )
            .all()
        )

        if len(motoristas_encontrados) != len(dados_entrada_empresa.motoristas_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Um ou mais IDs de motoristas fornecidos não foram encontrados.",
            )

        nova_empresa_modelo.motoristas.extend(motoristas_encontrados)

    sessao_banco.add(nova_empresa_modelo)
    sessao_banco.commit()

    sessao_banco.refresh(nova_empresa_modelo)
    return nova_empresa_modelo


def listar_pessoas_fisicas(sessao_banco: Session) -> List[models.PessoaFisica]:
    lista_clientes = sessao_banco.query(models.PessoaFisica).all()
    return lista_clientes


def buscar_pessoa_fisica_por_id(
    id_pessoa: int, sessao_banco: Session
) -> models.PessoaFisica:
    cliente_encontrado = sessao_banco.get(models.PessoaFisica, id_pessoa)

    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente Pessoa Física com ID {id_pessoa} não encontrado.",
        )
    return cliente_encontrado


def atualizar_pessoa_fisica(
    id_pessoa: int,
    dados_atualizacao: cliente_schema.SchemaPessoaFisicaUpdate,
    sessao_banco: Session,
) -> models.PessoaFisica:
    cliente_para_atualizar = buscar_pessoa_fisica_por_id(id_pessoa, sessao_banco)

    if dados_atualizacao.email != cliente_para_atualizar.email:
        outro_cliente_email = (
            sessao_banco.query(models.Pessoa)
            .filter(models.Pessoa.email == dados_atualizacao.email)
            .first()
        )
        if outro_cliente_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado para outro cliente.",
            )

    if dados_atualizacao.cpf != cliente_para_atualizar.cpf:
        outro_cliente_cpf = (
            sessao_banco.query(models.PessoaFisica)
            .filter(models.PessoaFisica.cpf == dados_atualizacao.cpf)
            .first()
        )
        if outro_cliente_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado para outro cliente.",
            )

    if dados_atualizacao.cnh != cliente_para_atualizar.cnh:
        outro_cliente_cnh = (
            sessao_banco.query(models.PessoaFisica)
            .filter(models.PessoaFisica.cnh == dados_atualizacao.cnh)
            .first()
        )
        if outro_cliente_cnh:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNH já cadastrada para outro cliente.",
            )

    cliente_para_atualizar.email = dados_atualizacao.email
    cliente_para_atualizar.nome_completo = dados_atualizacao.nome_completo
    cliente_para_atualizar.telefone = dados_atualizacao.telefone
    cliente_para_atualizar.cpf = dados_atualizacao.cpf
    cliente_para_atualizar.cnh = dados_atualizacao.cnh

    if not cliente_para_atualizar.endereco:
        cliente_para_atualizar.endereco = models.Endereco(pessoa_id=id_pessoa)

    dados_endereco = dados_atualizacao.endereco.model_dump()
    for key, value in dados_endereco.items():
        setattr(cliente_para_atualizar.endereco, key, value)

    sessao_banco.add(cliente_para_atualizar)
    sessao_banco.commit()
    sessao_banco.refresh(cliente_para_atualizar)

    return cliente_para_atualizar


def deletar_pessoa_fisica(id_pessoa: int, sessao_banco: Session) -> None:
    cliente_para_deletar = buscar_pessoa_fisica_por_id(id_pessoa, sessao_banco)

    if cliente_para_deletar.reservas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar o cliente com ID {id_pessoa}, pois ele possui reservas associadas.",
        )

    sessao_banco.delete(cliente_para_deletar)
    sessao_banco.commit()


def listar_pessoas_juridicas(sessao_banco: Session) -> List[models.PessoaJuridica]:
    lista_empresas = sessao_banco.query(models.PessoaJuridica).all()
    return lista_empresas


def buscar_pessoa_juridica_por_id(
    id_pessoa: int, sessao_banco: Session
) -> models.PessoaJuridica:
    empresa_encontrada = sessao_banco.get(models.PessoaJuridica, id_pessoa)

    if not empresa_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente Pessoa Jurídica com ID {id_pessoa} não encontrado.",
        )
    return empresa_encontrada


def atualizar_pessoa_juridica(
    id_pessoa: int,
    dados_atualizacao: cliente_schema.SchemaPessoaJuridicaUpdate,
    sessao_banco: Session,
) -> models.PessoaJuridica:
    empresa_para_atualizar = buscar_pessoa_juridica_por_id(id_pessoa, sessao_banco)

    if dados_atualizacao.cnpj != empresa_para_atualizar.cnpj:
        outra_empresa_cnpj = (
            sessao_banco.query(models.PessoaJuridica)
            .filter(models.PessoaJuridica.cnpj == dados_atualizacao.cnpj)
            .first()
        )
        if outra_empresa_cnpj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado para outra empresa.",
            )

    if dados_atualizacao.email != empresa_para_atualizar.email:
        outro_cliente_email = (
            sessao_banco.query(models.Pessoa)
            .filter(models.Pessoa.email == dados_atualizacao.email)
            .first()
        )
        if outro_cliente_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado para outro cliente.",
            )

    empresa_para_atualizar.razao_social = dados_atualizacao.razao_social
    empresa_para_atualizar.telefone = dados_atualizacao.telefone
    empresa_para_atualizar.email = dados_atualizacao.email
    empresa_para_atualizar.cnpj = dados_atualizacao.cnpj

    if not empresa_para_atualizar.endereco:
        empresa_para_atualizar.endereco = models.Endereco(pessoa_id=id_pessoa)

    dados_endereco = dados_atualizacao.endereco.model_dump()
    for key, value in dados_endereco.items():
        setattr(empresa_para_atualizar.endereco, key, value)

    if dados_atualizacao.motoristas_ids is not None:
        motoristas_encontrados = []
        if dados_atualizacao.motoristas_ids:
            motoristas_encontrados = (
                sessao_banco.query(models.PessoaFisica)
                .filter(
                    models.PessoaFisica.id_pessoa.in_(dados_atualizacao.motoristas_ids)
                )
                .all()
            )
            if len(motoristas_encontrados) != len(dados_atualizacao.motoristas_ids):
                raise HTTPException(
                    status_code=404,
                    detail="Um ou mais IDs de motoristas não encontrados.",
                )

        empresa_para_atualizar.motoristas = motoristas_encontrados

    sessao_banco.add(empresa_para_atualizar)
    sessao_banco.commit()
    sessao_banco.refresh(empresa_para_atualizar)

    return empresa_para_atualizar


def deletar_pessoa_juridica(id_pessoa: int, sessao_banco: Session) -> None:
    empresa_para_deletar = buscar_pessoa_juridica_por_id(id_pessoa, sessao_banco)

    if empresa_para_deletar.reservas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível deletar a empresa com ID {id_pessoa}, pois ela possui reservas associadas.",
        )

    sessao_banco.delete(empresa_para_deletar)
    sessao_banco.commit()


def alterar_status_pessoa_fisica(
    id_pessoa: int, novo_status: StatusContaEnum, sessao_banco: Session
) -> models.PessoaFisica:
    cliente = buscar_pessoa_fisica_por_id(id_pessoa, sessao_banco)

    cliente.e_ativo = novo_status == StatusContaEnum.ATIVO

    sessao_banco.add(cliente)
    sessao_banco.commit()
    sessao_banco.refresh(cliente)
    return cliente


def alterar_status_pessoa_juridica(
    id_pessoa: int, novo_status: StatusContaEnum, sessao_banco: Session
) -> models.PessoaJuridica:
    empresa = buscar_pessoa_juridica_por_id(id_pessoa, sessao_banco)

    empresa.e_ativo = novo_status == StatusContaEnum.ATIVO

    sessao_banco.add(empresa)
    sessao_banco.commit()
    sessao_banco.refresh(empresa)
    return empresa


def adicionar_motorista_empresa(
    empresa_logada: models.PessoaJuridica,
    cpf_motorista: str,
    sessao_banco: Session,
) -> models.PessoaJuridica:
    motorista = (
        sessao_banco.query(models.PessoaFisica)
        .filter(models.PessoaFisica.cpf == cpf_motorista)
        .first()
    )

    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motorista com CPF {cpf_motorista} não encontrado. Ele precisa ter cadastro como Pessoa Física.",
        )

    if (
        motorista.empresa_id is not None
        and motorista.empresa_id != empresa_logada.id_pessoa
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O motorista {motorista.nome_completo} já está vinculado a outra empresa.",
        )

    if motorista in empresa_logada.motoristas:
        return empresa_logada

    empresa_logada.motoristas.append(motorista)

    sessao_banco.add(empresa_logada)
    sessao_banco.commit()
    sessao_banco.refresh(empresa_logada)

    return empresa_logada


def remover_motorista_empresa(
    empresa_logada: models.PessoaJuridica,
    id_motorista_remover: int,
    sessao_banco: Session,
) -> models.PessoaJuridica:
    motorista = sessao_banco.get(models.PessoaFisica, id_motorista_remover)

    if not motorista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Motorista com ID {id_motorista_remover} (Pessoa Física) não encontrado.",
        )

    if motorista not in empresa_logada.motoristas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Este motorista (ID {id_motorista_remover}) não está associado à sua empresa.",
        )

    empresa_logada.motoristas.remove(motorista)

    sessao_banco.add(empresa_logada)
    sessao_banco.commit()
    sessao_banco.refresh(empresa_logada)

    return empresa_logada
