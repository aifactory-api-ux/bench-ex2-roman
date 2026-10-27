# DEVELOPMENT PLAN: Conversor de números romanos

## 1. ARCHITECTURE OVERVIEW
Utilidad Python autónoma sin servicios web, base de datos ni frontend. La lógica se concentra en `src/roman.py` con dos funciones públicas puras: `to_roman` y `from_roman`. Las pruebas residen en `tests/test_roman.py` y se ejecutan con `pytest` usando únicamente la biblioteca estándar. El `README.md` documenta uso, reglas de validación y ejecución de pruebas.

## 2. ACCEPTANCE CRITERIA
1. `src/roman.py` exporta `to_roman` y `from_roman` con `__all__ = ["to_roman", "from_roman"]`.
2. `to_roman(n)` convierte correctamente enteros 1..3999 a notación romana estándar con formas sustractivas (4="IV", 9="IX", 40="XL", 90="XC", 400="CD", 900="CM") y eleva `TypeError` para no `int`/`bool` y `ValueError` fuera de rango.
3. `from_roman(s)` acepta mayúsculas y minúsculas canónicas, rechaza cadenas vacías/espacios/no canónicas ("IIII", "VV", "IC", "MMMM") y eleva los errores especificados.
4. `tests/test_roman.py` incluye casos normales, límites, errores y roundtrip `from_roman(to_roman(n)) == n` para 1..3999.
5. `README.md` documenta brevemente el uso de la utilidad y el comando de pruebas.

## 3. EXECUTABLE ITEMS

### ITEM 1: Foundation — Implementación de src/roman.py con to_roman y from_roman
**Goal:** Crear el módulo autónomo `src/roman.py` con las funciones públicas `to_roman(n: int) -> str` y `from_roman(s: str) -> int`. `to_roman` valida tipo (rechaza `bool` y no `int`) antes del rango 1..3999 y usa una tabla descendente con formas sustractivas. `from_roman` normaliza a mayúsculas, valida gramática canónica y devuelve un entero en el rango 1..3999. Solo biblioteca estándar.
**Files to create:**
- src/roman.py (create) - módulo autónomo con implementaciones y `__all__ = ["to_roman", "from_roman"]`; constante privada de mapeo descendente.
**Dependencies:** None
**Validation:** `PYTHONPATH=. python -c "from src.roman import to_roman, from_roman; assert to_roman(1994)=='MCMXCIV'; assert from_roman('mcmxciv')==1994"`
**Role:** role-dev (backend_developer)

### ITEM 2: Pruebas — tests/test_roman.py con casos normales, límites, errores y roundtrip
**Goal:** Crear la suite de pruebas en `tests/test_roman.py` para ambas funciones. Cubrir conversiones normales representativas, límites 1 y 3999, errores de tipo y rango, rechazo de formas no canónicas, aceptación de mayúsculas/minúsculas y roundtrip completo para 1..3999.
**Files to create:**
- tests/test_roman.py (create) - pruebas pytest sin dependencias externas.
**Dependencies:** Item 1
**Validation:** `PYTHONPATH=. python -m pytest tests/test_roman.py -q`
**Role:** role-qa (qa_engineer)

### ITEM 3: Infrastructure & Deployment — README y validación final
**Goal:** Crear `README.md` breve con descripción de la utilidad, ejemplos de uso, reglas de validación y comando para ejecutar las pruebas. Asegurar que el proyecto puede ser consumido y verificado desde un workspace vacío.
**Files to create:**
- README.md (create) - documentación breve de la utilidad y ejecución de pruebas.
**Dependencies:** Item 1, Item 2
**Validation:** `PYTHONPATH=. python -m pytest tests/test_roman.py -q && test -f README.md`
**Role:** role-doc (documentation_writer)