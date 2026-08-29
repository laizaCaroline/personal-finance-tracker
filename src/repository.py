from src.database import get_connection
from src.models import Despesa, Categoria


class CategoriaRepository:

    @staticmethod
    def listar() -> list[Categoria]:
        with get_connection() as conn:
            rows = conn.execute("SELECT id, nome FROM categorias ORDER BY nome").fetchall()
            return [Categoria(id=r["id"], nome=r["nome"]) for r in rows]

    @staticmethod
    def buscar_por_id(categoria_id: int) -> Categoria | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, nome FROM categorias WHERE id = ?", (categoria_id,)
            ).fetchone()
            return Categoria(id=row["id"], nome=row["nome"]) if row else None

    @staticmethod
    def criar(nome: str) -> int:
        with get_connection() as conn:
            cursor = conn.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
            conn.commit()
            return cursor.lastrowid


class DespesaRepository:

    @staticmethod
    def criar(descricao: str, valor: float, data: str, categoria_id: int) -> int:
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO despesas (descricao, valor, data, categoria_id)
                   VALUES (?, ?, ?, ?)""",
                (descricao, valor, data, categoria_id)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def atualizar(despesa_id: int, descricao: str, valor: float, data: str, categoria_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                """UPDATE despesas SET descricao = ?, valor = ?, data = ?, categoria_id = ?
                   WHERE id = ?""",
                (descricao, valor, data, categoria_id, despesa_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def excluir(despesa_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def listar(categoria_id: int | None = None, data_inicio: str | None = None,
               data_fim: str | None = None) -> list[Despesa]:
        query = """
            SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id, c.nome as categoria_nome
            FROM despesas d
            JOIN categorias c ON c.id = d.categoria_id
            WHERE 1=1
        """
        params = []

        if categoria_id is not None:
            query += " AND d.categoria_id = ?"
            params.append(categoria_id)
        if data_inicio:
            query += " AND d.data >= ?"
            params.append(data_inicio)
        if data_fim:
            query += " AND d.data <= ?"
            params.append(data_fim)

        query += " ORDER BY d.data DESC"

        with get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                Despesa(
                    id=r["id"], descricao=r["descricao"], valor=r["valor"],
                    data=r["data"], categoria_id=r["categoria_id"],
                    categoria_nome=r["categoria_nome"]
                )
                for r in rows
            ]

    @staticmethod
    def buscar_por_id(despesa_id: int) -> Despesa | None:
        with get_connection() as conn:
            row = conn.execute(
                """SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id, c.nome as categoria_nome
                   FROM despesas d JOIN categorias c ON c.id = d.categoria_id
                   WHERE d.id = ?""",
                (despesa_id,)
            ).fetchone()
            if not row:
                return None
            return Despesa(
                id=row["id"], descricao=row["descricao"], valor=row["valor"],
                data=row["data"], categoria_id=row["categoria_id"],
                categoria_nome=row["categoria_nome"]
            )
