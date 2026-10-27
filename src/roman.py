"""Conversor bidireccional entre enteros y números romanos estándar.

Utilidad autónoma, sin dependencias externas, que expone dos funciones
públicas: `to_roman` (entero -> numeral romano) y `from_roman`
(numeral romano -> entero).
"""

import re

__all__ = ["to_roman", "from_roman"]

_MIN = 1
_MAX = 3999

# Tabla descendente de valor y símbolo. Las formas sustractivas se colocan
# antes que las aditivas para que ganen prioridad al descomponer el número.
_ROMANOS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_SIMBOLOS = "IVXLCDM"
_VALORES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
_SIMBOLOS_VALIDOS = frozenset(_SIMBOLOS + _SIMBOLOS.lower())

# Gramática canónica: miles? centenas? decenas? unidades?
_CANONICO = re.compile(
    r"M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})"
)


def to_roman(n: int) -> str:
    """Convierte un entero del rango 1..3999 a notación romana estándar.

    Args:
        n: Entero a convertir.

    Returns:
        Numeral romano en mayúsculas.

    Raises:
        TypeError: Si `n` no es un `int` o es un `bool`.
        ValueError: Si `n` está fuera del rango 1..3999.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n debe ser un int, no {type(n).__name__}")
    if n < _MIN or n > _MAX:
        raise ValueError(f"n debe estar en el rango {_MIN}..{_MAX}, no {n}")

    partes = []
    for valor, simbolo in _ROMANOS:
        veces, n = divmod(n, valor)
        partes.append(simbolo * veces)
    return "".join(partes)


def from_roman(s: str) -> int:
    """Convierte un numeral romano canónico a su valor entero.

    Acepta mayúsculas y minúsculas.

    Args:
        s: Numeral romano canónico.

    Returns:
        Valor entero en el rango 1..3999.

    Raises:
        TypeError: Si `s` no es un `str`.
        ValueError: Si `s` está vacía, contiene caracteres no válidos o no
            respeta la gramática romana estándar.
    """
    if not isinstance(s, str):
        raise TypeError(f"s debe ser un str, no {type(s).__name__}")
    if not s.strip():
        raise ValueError("el numeral romano no puede estar vacío")
    if any(simbolo not in _SIMBOLOS_VALIDOS for simbolo in s):
        raise ValueError(f"el numeral romano contiene caracteres no válidos: {s!r}")

    texto = s.upper()
    if not _CANONICO.fullmatch(texto):
        raise ValueError(f"el numeral romano no es canónico: {s!r}")

    total = 0
    indice = 0
    longitud = len(texto)
    while indice < longitud:
        valor = _VALORES[texto[indice]]
        siguiente = _VALORES[texto[indice + 1]] if indice + 1 < longitud else 0
        if valor < siguiente:
            total += siguiente - valor
            indice += 2
        else:
            total += valor
            indice += 1

    if total < _MIN or total > _MAX:
        raise ValueError(f"el valor {total} está fuera del rango {_MIN}..{_MAX}")
    return total
