"""Pruebas del conversor de números romanos."""

import sys
from pathlib import Path

import pytest

# Permite ejecutar las pruebas sin instalar el paquete ni exportar PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.roman import from_roman, to_roman  # noqa: E402

LIMITE_INFERIOR = 1
LIMITE_SUPERIOR = 3999
SIMBOLOS = frozenset("IVXLCDM")

# (valor entero, numeral romano canónico)
CASOS_CANONICOS = [
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (6, "VI"),
    (7, "VII"),
    (8, "VIII"),
    (9, "IX"),
    (10, "X"),
    (11, "XI"),
    (14, "XIV"),
    (19, "XIX"),
    (27, "XXVII"),
    (40, "XL"),
    (44, "XLIV"),
    (49, "XLIX"),
    (50, "L"),
    (58, "LVIII"),
    (90, "XC"),
    (99, "XCIX"),
    (100, "C"),
    (400, "CD"),
    (444, "CDXLIV"),
    (500, "D"),
    (900, "CM"),
    (944, "CMXLIV"),
    (1000, "M"),
    (1994, "MCMXCIV"),
    (2024, "MMXXIV"),
    (3999, "MMMCMXCIX"),
]

# Formas sustractivas obligatorias: valor y numeral esperado.
CASOS_SUSTRACTIVOS = [
    (4, "IV"),
    (9, "IX"),
    (40, "XL"),
    (90, "XC"),
    (400, "CD"),
    (900, "CM"),
]

VALORES_FUERA_DE_RANGO = [0, -1, -3999, 4000, 10000]

VALORES_TIPO_INVALIDO = [True, False, 3.14, 4.0, "4", None, [4], (4,)]

NUMERALES_NO_CANONICOS = [
    "IIII",  # cuatro unidades consecutivas
    "VV",  # dos cincos
    "IC",  # resta inválida
    "IL",
    "ID",
    "XD",
    "XM",
    "LC",
    "DM",
    "MMMM",  # supera el máximo representable
    "XXXX",
    "CCCC",
    "IIV",
    "IXC",  # secciones fuera de orden
    "VIV",
    "DD",
    "LL",
    "IIX",
    "MCMC",
]

CADENAS_INVALIDAS = ["", "   ", "\t", "ABC", "12", "IV!", "O", "VIIII"]


@pytest.mark.parametrize("valor,romano", CASOS_CANONICOS)
def test_to_roman_casos_conocidos(valor, romano):
    assert to_roman(valor) == romano


@pytest.mark.parametrize("valor,romano", CASOS_SUSTRACTIVOS)
def test_to_roman_usa_formas_sustractivas(valor, romano):
    assert to_roman(valor) == romano


def test_to_roman_limite_inferior():
    assert to_roman(LIMITE_INFERIOR) == "I"


def test_to_roman_limite_superior():
    assert to_roman(LIMITE_SUPERIOR) == "MMMCMXCIX"


@pytest.mark.parametrize("valor", VALORES_FUERA_DE_RANGO)
def test_to_roman_fuera_de_rango(valor):
    with pytest.raises(ValueError):
        to_roman(valor)


@pytest.mark.parametrize("valor", VALORES_TIPO_INVALIDO)
def test_to_roman_tipo_invalido(valor):
    with pytest.raises(TypeError):
        to_roman(valor)


def test_to_roman_solo_devuelve_simbolos_validos():
    for valor in range(LIMITE_INFERIOR, LIMITE_SUPERIOR + 1):
        romano = to_roman(valor)
        assert romano
        assert set(romano) <= SIMBOLOS
        assert romano == romano.upper()


@pytest.mark.parametrize("valor,romano", CASOS_CANONICOS)
def test_from_roman_casos_conocidos(valor, romano):
    assert from_roman(romano) == valor


def test_from_roman_limite_inferior():
    assert from_roman("I") == LIMITE_INFERIOR


def test_from_roman_limite_superior():
    assert from_roman("MMMCMXCIX") == LIMITE_SUPERIOR


@pytest.mark.parametrize(
    "romano,valor",
    [("i", 1), ("iv", 4), ("mcmxciv", 1994), ("mmmcmxcix", 3999)],
)
def test_from_roman_acepta_minusculas(romano, valor):
    assert from_roman(romano) == valor


@pytest.mark.parametrize("romano", NUMERALES_NO_CANONICOS)
def test_from_roman_rechaza_no_canonicos(romano):
    with pytest.raises(ValueError):
        from_roman(romano)


@pytest.mark.parametrize("cadena", CADENAS_INVALIDAS)
def test_from_roman_rechaza_cadenas_invalidas(cadena):
    with pytest.raises(ValueError):
        from_roman(cadena)


@pytest.mark.parametrize("valor", [None, 123, 1.5, b"IV", ["IV"], True])
def test_from_roman_tipo_invalido(valor):
    with pytest.raises(TypeError):
        from_roman(valor)


def test_roundtrip_rango_completo():
    for valor in range(LIMITE_INFERIOR, LIMITE_SUPERIOR + 1):
        romano = to_roman(valor)
        assert from_roman(romano) == valor, f"roundtrip fallido para {valor}"


def test_roundtrip_en_minusculas():
    for valor in range(LIMITE_INFERIOR, LIMITE_SUPERIOR + 1):
        romano = to_roman(valor)
        assert from_roman(romano.lower()) == valor, f"roundtrip fallido para {valor}"


def test_api_publica_limitada():
    from src import roman

    assert roman.__all__ == ["to_roman", "from_roman"]
