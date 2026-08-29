from src.database import init_db
from src.repository import CategoriaRepository
from src.services import DespesaService, RelatorioService


def linha():
    print("-" * 50)


def menu_principal():
    print("\n=== CONTROLE DE DESPESAS ===")
    print("1. Cadastrar despesa")
    print("2. Listar despesas")
    print("3. Editar despesa")
    print("4. Remover despesa")
    print("5. Relatório por categoria")
    print("6. Relatório mensal")
    print("7. Resumo geral")
    print("8. Maiores despesas")
    print("9. Listar categorias")
    print("0. Sair")
    return input("Escolha uma opção: ").strip()


def listar_categorias_disponiveis():
    categorias = CategoriaRepository.listar()
    for c in categorias:
        print(f"  [{c.id}] {c.nome}")


def cadastrar_despesa():
    linha()
    print("Categorias disponíveis:")
    listar_categorias_disponiveis()
    descricao = input("Descrição: ").strip()
    try:
        valor = float(input("Valor: R$ ").replace(",", "."))
    except ValueError:
        print("Valor inválido.")
        return
    data = input("Data (AAAA-MM-DD): ").strip()
    try:
        categoria_id = int(input("ID da categoria: "))
    except ValueError:
        print("ID de categoria inválido.")
        return

    sucesso, mensagem = DespesaService.cadastrar(descricao, valor, data, categoria_id)
    print(mensagem)


def listar_despesas():
    linha()
    filtro = input("Filtrar por categoria? (id ou Enter para pular): ").strip()
    categoria_id = int(filtro) if filtro else None
    data_inicio = input("Data início (AAAA-MM-DD ou Enter): ").strip() or None
    data_fim = input("Data fim (AAAA-MM-DD ou Enter): ").strip() or None

    despesas = DespesaService.consultar(categoria_id, data_inicio, data_fim)
    if not despesas:
        print("Nenhuma despesa encontrada.")
        return

    linha()
    for d in despesas:
        print(f"[{d.id}] {d.data} | {d.categoria_nome:<15} | R$ {d.valor:>10.2f} | {d.descricao}")
    linha()
    print(f"Total de registros: {len(despesas)}")
    print(f"Soma: R$ {sum(d.valor for d in despesas):.2f}")


def editar_despesa():
    linha()
    try:
        despesa_id = int(input("ID da despesa a editar: "))
    except ValueError:
        print("ID inválido.")
        return

    despesa = DespesaService.consultar()
    print("Deixe em branco para manter o valor atual.")
    descricao = input("Nova descrição: ").strip()
    valor_str = input("Novo valor: ").strip()
    data = input("Nova data (AAAA-MM-DD): ").strip()
    categoria_str = input("Novo ID de categoria: ").strip()

    from src.repository import DespesaRepository
    atual = DespesaRepository.buscar_por_id(despesa_id)
    if not atual:
        print(f"Despesa {despesa_id} não encontrada.")
        return

    descricao = descricao or atual.descricao
    valor = float(valor_str) if valor_str else atual.valor
    data = data or atual.data
    categoria_id = int(categoria_str) if categoria_str else atual.categoria_id

    sucesso, mensagem = DespesaService.editar(despesa_id, descricao, valor, data, categoria_id)
    print(mensagem)


def remover_despesa():
    linha()
    try:
        despesa_id = int(input("ID da despesa a remover: "))
    except ValueError:
        print("ID inválido.")
        return
    sucesso, mensagem = DespesaService.remover(despesa_id)
    print(mensagem)


def relatorio_categoria():
    linha()
    data_inicio = input("Data início (AAAA-MM-DD ou Enter): ").strip() or None
    data_fim = input("Data fim (AAAA-MM-DD ou Enter): ").strip() or None
    resultado = RelatorioService.total_por_categoria(data_inicio, data_fim)
    if not resultado:
        print("Sem dados para o período.")
        return
    linha()
    for r in resultado:
        print(f"{r['categoria']:<15} | {r['quantidade']:>3} despesas | R$ {r['total']:>10.2f}")


def relatorio_mensal():
    linha()
    try:
        ano = int(input("Ano (AAAA): "))
    except ValueError:
        print("Ano inválido.")
        return
    resultado = RelatorioService.total_por_mes(ano)
    if not resultado:
        print("Sem dados para esse ano.")
        return
    linha()
    for r in resultado:
        print(f"Mês {r['mes']}: R$ {r['total']:.2f}")


def resumo_geral():
    linha()
    r = RelatorioService.resumo_geral()
    print(f"Total de registros : {r['total_registros']}")
    print(f"Total gasto        : R$ {r['total_gasto']:.2f}")
    print(f"Média por despesa  : R$ {r['media_por_despesa']:.2f}")
    print(f"Maior despesa      : R$ {r['maior_despesa']:.2f}")
    print(f"Menor despesa      : R$ {r['menor_despesa']:.2f}")


def maiores_despesas():
    linha()
    try:
        limite = int(input("Quantas exibir? (padrão 5): ") or 5)
    except ValueError:
        limite = 5
    resultado = RelatorioService.maiores_despesas(limite)
    linha()
    for r in resultado:
        print(f"{r['data']} | {r['categoria']:<15} | R$ {r['valor']:>10.2f} | {r['descricao']}")


def executar():
    init_db()
    acoes = {
        "1": cadastrar_despesa,
        "2": listar_despesas,
        "3": editar_despesa,
        "4": remover_despesa,
        "5": relatorio_categoria,
        "6": relatorio_mensal,
        "7": resumo_geral,
        "8": maiores_despesas,
        "9": lambda: (linha(), listar_categorias_disponiveis()),
    }

    while True:
        opcao = menu_principal()
        if opcao == "0":
            print("Até mais!")
            break
        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    executar()
