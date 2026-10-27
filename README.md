# Conversor de números romanos

Utilidad Python autónoma que convierte enteros entre `1` y `3999` y su notación
romana estándar (con formas sustractivas). No depende de nada fuera de la
biblioteca estándar de Python.

## Requisitos

- Python 3.11 o superior.
- `pytest` solo es necesario para ejecutar las pruebas.

## Uso

```python
from src.roman import from_roman, to_roman

to_roman(4)        # "IV"
to_roman(1994)     # "MCMXCIV"
to_roman(3999)     # "MMMCMXCIX"

from_roman("IV")        # 4
from_roman("mcmxciv")   # 1994  (acepta mayúsculas y minúsculas)
```

El módulo solo expone dos funciones públicas:

```python
__all__ = ["to_roman", "from_roman"]
```

## Reglas de validación

`to_roman(n: int) -> str`

- `TypeError` si `n` no es un `int` o es un `bool` (el chequeo de tipo precede al
  de rango).
- `ValueError` si `n` está fuera del rango inclusivo `1..3999`.
- Devuelve siempre mayúsculas con las formas sustractivas `IV`, `IX`, `XL`,
  `XC`, `CD` y `CM`.

`from_roman(s: str) -> int`

- `TypeError` si `s` no es un `str`.
- `ValueError` si `s` está vacía, solo contiene espacios, incluye caracteres
  fuera de `I V X L C D M` o no respeta la gramática canónica.
- Se rechazan formas no estándar como `IIII`, `VV`, `IC`, `IL`, `XD`, `XM`,
  `IXC` y `MMMM`.
- Acepta mayúsculas y minúsculas y devuelve un entero en el rango `1..3999`.

Gramática canónica aceptada:

```text
roman      ::= miles? centenas? decenas? unidades?
miles      ::= M{0,3}
centenas   ::= CM | CD | D? C{0,3}
decenas    ::= XC | XL | L? X{0,3}
unidades   ::= IX | IV | V? I{0,3}
```

## Pruebas

```bash
PYTHONPATH=. python -m pytest tests/test_roman.py -q
```

La suite cubre casos conocidos, formas sustractivas, límites (`1` y `3999`),
errores de tipo y de rango, rechazo de numerales no canónicos y el roundtrip
`from_roman(to_roman(n)) == n` para todo el rango `1..3999`.

## Estructura

```text
.
├── src/
│   └── roman.py        # Implementación de to_roman y from_roman
├── tests/
│   └── test_roman.py   # Pruebas
└── README.md
```
