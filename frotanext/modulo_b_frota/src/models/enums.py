import enum


class StatusContaEnum(str, enum.Enum):
    ATIVO = "ativo"
    BLOQUEADO = "bloqueado"
    PENDENTE_CONFIRMACAO = "pendente_confirmacao"


class TipoPerfilEnum(str, enum.Enum):
    CLIENTE_PF = "cliente_pf"
    CLIENTE_PJ = "cliente_pj"
    ADMIN = "admin"


class TipoVeiculoEnum(str, enum.Enum):
    PASSEIO = "passeio"
    UTILITARIO = "utilitario"
    MOTOCICLETA = "motocicleta"


class StatusVeiculoEnum(str, enum.Enum):
    DISPONIVEL = "disponível"
    RESERVADO = "reservado"
    ALUGADO = "alugado"
    EM_MANUTENCAO = "em manutenção"
    INDISPONIVEL = "indisponível"


class CorVeiculoEnum(str, enum.Enum):
    PRETO = "Preto"
    BRANCO = "Branco"
    PRATA = "Prata"
    CINZA = "Cinza"
    VERMELHO = "Vermelho"
    AZUL = "Azul"
    VERDE = "Verde"
    AMARELO = "Amarelo"
    OUTRO = "Outro"


class StatusReservaEnum(str, enum.Enum):
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"
