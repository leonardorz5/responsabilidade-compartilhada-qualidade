import csv
from collections import defaultdict


ARQUIVO_DADOS = "dados_estudo_caso.csv"


def carregar_dados():
    dados = []

    with open(ARQUIVO_DADOS, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            dados.append(
                {
                    "periodo": linha["periodo"],
                    "bugs_qa": int(linha["bugs_qa"]),
                    "bugs_producao": int(linha["bugs_producao"]),
                    "retrabalho_horas": float(linha["retrabalho_horas"]),
                    "tempo_feedback_min": float(linha["tempo_feedback_min"]),
                    "chamados_clientes": int(linha["chamados_clientes"]),
                }
            )

    return dados


def calcular_medias(dados):
    periodos = defaultdict(list)

    for linha in dados:
        periodos[linha["periodo"]].append(linha)

    resultados = {}

    for periodo, registros in periodos.items():
        quantidade = len(registros)

        resultados[periodo] = {
            "bugs_qa": sum(r["bugs_qa"] for r in registros) / quantidade,
            "bugs_producao": sum(
                r["bugs_producao"] for r in registros
            ) / quantidade,
            "retrabalho_horas": sum(
                r["retrabalho_horas"] for r in registros
            ) / quantidade,
            "tempo_feedback_min": sum(
                r["tempo_feedback_min"] for r in registros
            ) / quantidade,
            "chamados_clientes": sum(
                r["chamados_clientes"] for r in registros
            ) / quantidade,
        }

    return resultados


def reducao_percentual(antes, depois):
    if antes == 0:
        return 0

    return ((antes - depois) / antes) * 100


def exibir_resultados(resultados):
    antes = resultados["Antes"]
    depois = resultados["Depois"]

    metricas = {
        "Bugs encontrados pelo QA": "bugs_qa",
        "Bugs em produção": "bugs_producao",
        "Retrabalho (horas)": "retrabalho_horas",
        "Tempo para feedback (min)": "tempo_feedback_min",
        "Chamados de clientes": "chamados_clientes",
    }

    print("\n===== ANALISE DO ESTUDO DE CASO =====\n")

    for nome, chave in metricas.items():
        reducao = reducao_percentual(
            antes[chave],
            depois[chave],
        )

        print(nome)
        print(f"Antes: {antes[chave]:.2f}")
        print(f"Depois: {depois[chave]:.2f}")
        print(f"Reducao: {reducao:.2f}%")
        print()


def main():
    dados = carregar_dados()
    resultados = calcular_medias(dados)
    exibir_resultados(resultados)


if __name__ == "__main__":
    main()