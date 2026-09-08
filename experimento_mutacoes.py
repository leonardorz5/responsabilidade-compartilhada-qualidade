import csv
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path


CENARIOS = [
    {
        "nome": "Controle - implementação correta",
        "modulo": "frete",
        "possui_defeito": False,
    },
    {
        "nome": "M1 - limite exclusivo",
        "modulo": "mutantes.frete_limite_exclusivo",
        "possui_defeito": True,
    },
    {
        "nome": "M2 - limite incorreto",
        "modulo": "mutantes.frete_limite_incorreto",
        "possui_defeito": True,
    },
    {
        "nome": "M3 - valor do frete incorreto",
        "modulo": "mutantes.frete_valor_incorreto",
        "possui_defeito": True,
    },
    {
        "nome": "M4 - frete grátis incorreto",
        "modulo": "mutantes.frete_gratis_incorreto",
        "possui_defeito": True,
    },
    {
        "nome": "M5 - condição invertida",
        "modulo": "mutantes.frete_condicao_invertida",
        "possui_defeito": True,
    },
]


PASTA_TEMPORARIA = Path(".experimento")
ARQUIVO_RESULTADOS = "resultados_experimento.csv"
ARQUIVO_RESUMO = "resumo_experimento.json"


def ler_junit(caminho):
    arvore = ET.parse(caminho)
    raiz = arvore.getroot()

    if raiz.tag == "testsuite":
        suites = [raiz]
    else:
        suites = raiz.findall("testsuite")

    total = sum(int(s.get("tests", 0)) for s in suites)
    falhas = sum(int(s.get("failures", 0)) for s in suites)
    erros = sum(int(s.get("errors", 0)) for s in suites)
    ignorados = sum(int(s.get("skipped", 0)) for s in suites)

    aprovados = total - falhas - erros - ignorados

    return total, aprovados, falhas, erros, ignorados


def executar_cenario(cenario, indice):
    ambiente = os.environ.copy()
    ambiente["FRETE_MODULE"] = cenario["modulo"]

    arquivo_xml = PASTA_TEMPORARIA / f"cenario_{indice}.xml"

    comando = [
        sys.executable,
        "-m",
        "pytest",
        "test_frete.py",
        "-q",
        f"--junitxml={arquivo_xml}",
    ]

    inicio = time.perf_counter()

    processo = subprocess.run(
        comando,
        env=ambiente,
        capture_output=True,
        text=True,
    )

    tempo = time.perf_counter() - inicio

    total, aprovados, falhas, erros, ignorados = ler_junit(
        arquivo_xml
    )

    defeito_detectado = (
        cenario["possui_defeito"]
        and falhas > 0
    )

    if cenario["possui_defeito"]:
        resultado_esperado = defeito_detectado
    else:
        resultado_esperado = falhas == 0 and erros == 0

    return {
        "cenario": cenario["nome"],
        "possui_defeito": cenario["possui_defeito"],
        "testes_executados": total,
        "testes_aprovados": aprovados,
        "testes_reprovados": falhas,
        "erros": erros,
        "defeito_detectado": defeito_detectado,
        "tempo_feedback_segundos": round(tempo, 4),
        "resultado_esperado_atendido": resultado_esperado,
        "codigo_saida_pytest": processo.returncode,
    }


def salvar_csv(resultados):
    with open(
        ARQUIVO_RESULTADOS,
        "w",
        newline="",
        encoding="utf-8",
    ) as arquivo:
        campos = resultados[0].keys()

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
        )

        escritor.writeheader()
        escritor.writerows(resultados)


def gerar_resumo(resultados):
    cenarios_defeituosos = [
        r for r in resultados
        if r["possui_defeito"]
    ]

    detectados = [
        r for r in cenarios_defeituosos
        if r["defeito_detectado"]
    ]

    total_defeitos = len(cenarios_defeituosos)
    total_detectados = len(detectados)

    taxa_deteccao = (
        total_detectados / total_defeitos * 100
        if total_defeitos
        else 0
    )

    tempos = [
        r["tempo_feedback_segundos"]
        for r in cenarios_defeituosos
    ]

    tempo_medio = (
        sum(tempos) / len(tempos)
        if tempos
        else 0
    )

    return {
        "defeitos_introduzidos": total_defeitos,
        "defeitos_detectados": total_detectados,
        "taxa_deteccao_percentual": round(
            taxa_deteccao,
            2,
        ),
        "tempo_medio_feedback_segundos": round(
            tempo_medio,
            4,
        ),
        "total_execucoes_de_testes": sum(
            r["testes_executados"]
            for r in resultados
        ),
    }


def main():
    PASTA_TEMPORARIA.mkdir(exist_ok=True)

    resultados = []

    print("\n===== EXPERIMENTO CONTROLADO =====\n")

    for indice, cenario in enumerate(CENARIOS):
        resultado = executar_cenario(
            cenario,
            indice,
        )

        resultados.append(resultado)

        status = (
            "DETECTADO"
            if resultado["defeito_detectado"]
            else "NAO DETECTADO"
        )

        if not cenario["possui_defeito"]:
            status = "CONTROLE APROVADO"

        print(cenario["nome"])
        print(
            f"Testes: "
            f"{resultado['testes_executados']}"
        )
        print(
            f"Falhas: "
            f"{resultado['testes_reprovados']}"
        )
        print(
            f"Tempo: "
            f"{resultado['tempo_feedback_segundos']}s"
        )
        print(f"Resultado: {status}")
        print()

    salvar_csv(resultados)

    resumo = gerar_resumo(resultados)

    with open(
        ARQUIVO_RESUMO,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            resumo,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )

    print("===== RESUMO =====")
    print(
        f"Defeitos introduzidos: "
        f"{resumo['defeitos_introduzidos']}"
    )
    print(
        f"Defeitos detectados: "
        f"{resumo['defeitos_detectados']}"
    )
    print(
        f"Taxa de detecção: "
        f"{resumo['taxa_deteccao_percentual']}%"
    )
    print(
        f"Tempo médio de feedback: "
        f"{resumo['tempo_medio_feedback_segundos']}s"
    )

    todos_validos = all(
        r["resultado_esperado_atendido"]
        for r in resultados
    )

    sys.exit(0 if todos_validos else 1)


if __name__ == "__main__":
    main()