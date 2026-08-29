from src.database import get_connection
from src.repository import DespesaRepository, CategoriaRepository
from src.models import Despesa


class DespesaService:

    @staticmethod
    def cadastrar(descricao: str, valor: float, data: str, categoria_id: int) -> tuple[bool, str]:
        erros = Despesa.validar(descricao, valor, data)
        if erros:
            return False, " | ".join(erros)

        categoria = CategoriaRepository.buscar_por_id(categoria_id)
        if not categoria:
            return False, f"Categoria com id {categoria_id} não existe."

        novo_id = DespesaRepository.criar(descricao.strip(), valor, data, categoria_id)
        return True, f"Despesa cadastrada com id {novo_id}."

    @staticmethod
    def editar(despesa_id: int, descricao: str, valor: float, data: str, categoria_id: int) -> tuple[bool, str]:
        if not DespesaRepository.buscar_por_id(despesa_id):
            return False, f"Despesa com id {despesa_id} não encontrada."

        erros = Despesa.validar(descricao, valor, data)
        if erros:
            return False, " | ".join(erros)

        if not CategoriaRepository.buscar_por_id(categoria_id):
            return False, f"Categoria com id {categoria_id} não existe."

        DespesaRepository.atualizar(despesa_id, descricao.strip(), valor, data, categoria_id)
        return True, "Despesa atualizada."

    @staticmethod
    def remover(despesa_id: int) -> tuple[bool, str]:
        if DespesaRepository.excluir(despesa_id):
            return True, "Despesa removida."
        return False, f"Despesa com id {despesa_id} não encontrada."

    @staticmethod
    def consultar(categoria_id: int = None, data_inicio: str = None, data_fim: str = None) -> list[Despesa]:
        return DespesaRepository.listar(categoria_id, data_inicio, data_fim)


class RelatorioService:

    @staticmethod
    def total_por_categoria(data_inicio: str = None, data_fim: str = None) -> list[dict]:
        query = """
            SELECT c.nome as categoria, SUM(d.valor) as total, COUNT(d.id) as quantidade
            FROM despesas d
            JOIN categorias c ON c.id = d.categoria_id
            WHERE 1=1
        """
        params = []
        if data_inicio:
            query += " AND d.data >= ?"
            params.append(data_inicio)
        if data_fim:
            query += " AND d.data <= ?"
            params.append(data_fim)

        query += " GROUP BY c.nome ORDER BY total DESC"

        with get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def total_por_mes(ano: int) -> list[dict]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT strftime('%m', data) as mes, SUM(valor) as total
                FROM despesas
                WHERE strftime('%Y', data) = ?
                GROUP BY mes
                ORDER BY mes
                """,
                (str(ano),)
            ).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def resumo_geral() -> dict:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) as total_registros,
                    COALESCE(SUM(valor), 0) as total_gasto,
                    COALESCE(AVG(valor), 0) as media_por_despesa,
                    COALESCE(MAX(valor), 0) as maior_despesa,
                    COALESCE(MIN(valor), 0) as menor_despesa
                FROM despesas
                """
            ).fetchone()
            return dict(row)

    @staticmethod
    def maiores_despesas(limite: int = 5) -> list[dict]:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT d.descricao, d.valor, d.data, c.nome as categoria
                FROM despesas d
                JOIN categorias c ON c.id = d.categoria_id
                ORDER BY d.valor DESC
                LIMIT ?
                """,
                (limite,)
            ).fetchall()
            return [dict(r) for r in rows]
