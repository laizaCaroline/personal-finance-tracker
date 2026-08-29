from dataclasses import dataclass
from datetime import date


@dataclass
class Categoria:
    id: int
    nome: str


@dataclass
class Despesa:
    id: int
    descricao: str
    valor: float
    data: str
    categoria_id: int
    categoria_nome: str = ""

    @staticmethod
    def validar(descricao: str, valor: float, data_str: str) -> list[str]:
        erros = []
        if not descricao or not descricao.strip():
            erros.append("Descrição não pode ser vazia.")
        if valor is None or valor <= 0:
            erros.append("Valor deve ser maior que zero.")
        try:
            date.fromisoformat(data_str)
        except (ValueError, TypeError):
            erros.append("Data inválida. Use o formato AAAA-MM-DD.")
        return erros
