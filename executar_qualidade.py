import json
import subprocess
import sys
import xml.etree.ElementTree as ET


ARQUIVO_RELATORIO = "resultado-testes.xml"
ARQUIVO_METRICAS = "metricas.json"


def executar_testes():
    comando = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        f"--junitxml={ARQUIVO_RELATORIO}",
    ]

    resultado = subprocess.run(comando)

    return resultado.returncode


def coletar_metricas():
    arvore = ET.parse(ARQUIVO_RELATORIO)
    raiz = arvore.getroot()

    suites = (
        [raiz]
        if raiz.tag == "testsuite"
        else raiz.findall("testsuite")
    )

    total = sum(int(s.get("tests", 0)) for s in suites)
    falhas = sum(int(s.get("failures", 0)) for s in suites)
    erros = sum(int(s.get("errors", 0)) for s in suites)
    ignorados = sum(int(s.get("skipped", 0)) for s in suites)
    tempo = sum(float(s.get("time", 0)) for s in suites)

    aprovados = total - falhas - erros - ignorados

    taxa_sucesso = (
        round((aprovados / total) * 100, 2)
        if total > 0
        else 0
    )

    metricas = {
        "testes_executados": total,
        "testes_aprovados": aprovados,
        "testes_reprovados": falhas,
        "erros": erros,
        "testes_ignorados": ignorados,
        "taxa_sucesso_percentual": taxa_sucesso,
        "tempo_execucao_segundos": round(tempo, 4),
    }

    with open(ARQUIVO_METRICAS, "w", encoding="utf-8") as arquivo:
        json.dump(metricas, arquivo, indent=4, ensure_ascii=False)

    print("\n===== METRICAS DE QUALIDADE =====")
    print(f"Testes executados: {total}")
    print(f"Testes aprovados: {aprovados}")
    print(f"Testes reprovados: {falhas}")
    print(f"Erros: {erros}")
    print(f"Testes ignorados: {ignorados}")
    print(f"Taxa de sucesso: {taxa_sucesso}%")
    print(f"Tempo de execução: {tempo:.4f}s")
    print("================================")


def main():
    codigo_saida = executar_testes()

    try:
        coletar_metricas()
    except Exception as erro:
        print(f"Erro ao coletar métricas: {erro}")

    sys.exit(codigo_saida)


if __name__ == "__main__":
    main()