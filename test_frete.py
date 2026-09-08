import importlib
import os


MODULO_FRETE = os.getenv("FRETE_MODULE", "frete")

calcular_frete = importlib.import_module(
    MODULO_FRETE
).calcular_frete


def test_compra_acima_de_200_tem_frete_gratis():
    assert calcular_frete(250) == 0


def test_compra_abaixo_de_200_paga_frete():
    assert calcular_frete(150) == 20


def test_compra_exatamente_200_tem_frete_gratis():
    assert calcular_frete(200) == 0