import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import database
from src.services import DespesaService, RelatorioService
from src.repository import CategoriaRepository


class TestDespesas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.DB_PATH = database.DB_PATH.parent / "test_finance.db"
        if database.DB_PATH.exists():
            database.DB_PATH.unlink()
        database.init_db()
        cls.categoria_id = CategoriaRepository.listar()[0].id

    @classmethod
    def tearDownClass(cls):
        if database.DB_PATH.exists():
            database.DB_PATH.unlink()

    def test_cadastrar_despesa_valida(self):
        sucesso, _ = DespesaService.cadastrar("Mercado", 150.50, "2026-01-10", self.categoria_id)
        self.assertTrue(sucesso)

    def test_cadastrar_despesa_valor_invalido(self):
        sucesso, mensagem = DespesaService.cadastrar("Mercado", -10, "2026-01-10", self.categoria_id)
        self.assertFalse(sucesso)
        self.assertIn("Valor", mensagem)

    def test_cadastrar_com_categoria_inexistente(self):
        sucesso, mensagem = DespesaService.cadastrar("Mercado", 50, "2026-01-10", 9999)
        self.assertFalse(sucesso)
        self.assertIn("Categoria", mensagem)

    def test_consultar_despesas(self):
        DespesaService.cadastrar("Uber", 25.00, "2026-01-15", self.categoria_id)
        despesas = DespesaService.consultar()
        self.assertGreaterEqual(len(despesas), 1)

    def test_resumo_geral(self):
        resumo = RelatorioService.resumo_geral()
        self.assertIn("total_gasto", resumo)
        self.assertGreaterEqual(resumo["total_registros"], 1)


if __name__ == "__main__":
    unittest.main()
