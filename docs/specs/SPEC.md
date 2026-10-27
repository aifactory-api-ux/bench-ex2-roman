# SPEC.md

> Scope: Standalone Python utility for bidirectional conversion between integers 1–3999 and standard Roman numeral notation using subtractive forms.

## 1. TECHNOLOGY STACK

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | 3.11 (CPython) | Must run on Python 3.11+ |
| Runtime dependencies | None | N/A | Standard library only |
| Package manager | None | N/A | Single-file module; no packaging required |
| Test runner | None requested | N/A | No test files required by original request |
| Frontend | None | N/A | No UI/frontend layer |
| Database | None | N/A | No persistence |
| HTTP server | None | N/A | No API endpoints |
| External services | None | N/A | No network calls |

The utility is completely deterministic and self-contained.

## 2. DATA CONTRACTS

This project has no persisted data models, no Pydantic models, no TypeScript interfaces, and no database entities. The public contract is defined exclusively by the following two Python function signatures and their validation rules.

### 2.1 Public Function Contract: `to_roman`

```python
def to_roman(n: int) -> str:
    """
    Convert an integer in the inclusive range 1..3999 to standard Roman numeral notation.

    Args:
        n: Integer to convert.

    Returns:
        Uppercase standard Roman numeral string.

    Raises:
        TypeError: If n is not an int, or if n is a bool.
        ValueError: If n is outside the inclusive range 1..3999.
    """
```

#### Input Contract

| Field | Type | Required | Constraints |
|---|---|---|---|
| `n` | `int` | Yes | Must satisfy `1 <= n <= 3999`; `type(n) is int` must be true. `bool` is rejected even though `bool` subclasses `int`. |

#### Output Contract

| Field | Type | Constraints |
|---|---|---|
| Return value | `str` | Uppercase, non-empty, standard Roman numeral using only `I`, `V`, `X`, `L`, `C`, `D`, `M` |

#### Exception Contract

| Condition | Exception | Precedence |
|---|---|---|
| `n` is not `int` | `TypeError` | Check first |
| `n` is `bool` | `TypeError` | Check first, before range validation |
| `n < 1` | `ValueError` | Check after type validation |
| `n > 3999` | `ValueError` | Check after type validation |

#### Required Subtractive Mapping

The conversion MUST use the following descending value-to-symbol table:

| Value | Symbol |
|---|---:|
| 1000 | `M` |
| 900 | `CM` |
| 500 | `D` |
| 400 | `CD` |
| 100 | `C` |
| 90 | `XC` |
| 50 | `L` |
| 40 | `XL` |
| 10 | `X` |
| 9 | `IX` |
| 5 | `V` |
| 4 | `IV` |
| 1 | `I` |

The algorithm must use subtractive notation:
- `4 = "IV"` (not `"IIII"`)
- `9 = "IX"` (not `"VIIII"`)
- `40 = "XL"` (not `"XXXX"`)
- `90 = "XC"` (not `"LXXXX"`)
- `400 = "CD"` (not `"CCCC"`)
- `900 = "CM"` (not `"DCCCC"`)

#### Representative Examples

| `n` | Expected `to_roman(n)` |
|---|---:|
| 1 | `"I"` |
| 4 | `"IV"` |
| 9 | `"IX"` |
| 40 | `"XL"` |
| 90 | `"XC"` |
| 400 | `"CD"` |
| 900 | `"CM"` |
| 58 | `"LVIII"` |
| 1994 | `"MCMXCIV"` |
| 3999 | `"MMMCMXCIX"` |

### 2.2 Public Function Contract: `from_roman`

```python
def from_roman(s: str) -> int:
    """
    Convert a standard Roman numeral string to its integer value.

    Args:
        s: Standard uppercase Roman numeral string.

    Returns:
        Integer value in the inclusive range 1..3999.

    Raises:
        TypeError: If s is not a str.
        ValueError: If s is not a valid standard Roman numeral or represents a value outside 1..3999.
    """
```

#### Input Contract

| Field | Type | Required | Constraints |
|---|---|---|---|
| `s` | `str` | Yes | Must be non-empty, uppercase, standard Roman numeral using only `I`, `V`, `X`, `L`, `C`, `D`, `M`; must follow standard subtractive grammar |

#### Output Contract

| Field | Type | Constraints |
|---|---|---|
| Return value | `int` | Must satisfy `1 <= result <= 3999` |

#### Exception Contract

| Condition | Exception |
|---|---|
| `s` is not `str` | `TypeError` |
| `s` is empty string or only whitespace | `ValueError` |
| `s` contains characters outside `I V X L C D M` | `ValueError` |
| `s` violates standard Roman numeral syntax | `ValueError` |
| `s` would parse to a value less than 1 or greater than 3999 | `ValueError` |

#### Standard Roman Numeral Grammar

The accepted input grammar is:

```
roman    ::= thousands? hundreds? tens? ones?
thousands ::= M{0,3}
hundreds  ::= CM | CD | D? C{0,3}
tens      ::= XC | XL | L? X{0,3}
ones      ::= IX | IV | V? I{0,3}
```

This grammar rejects:
- Four or more consecutive identical symbols such as `IIII`, `XXXX`, `CCCC`, `MMMM`
- Invalid subtractive pairs such as `IC`, `IL`, `XD`, `XM`, `LC`, `DM`
- Out-of-order sections such as `IXC`
- Lowercase input such as `"iv"` or `"mmxxii"`
- Empty string `""`

#### Representative Examples

| `s` | Expected `from_roman(s)` |
|---|---:|
| `"I"` | 1 |
| `"IV"` | 4 |
| `"IX"` | 9 |
| `"XL"` | 40 |
| `"XC"` | 90 |
| `"CD"` | 400 |
| `"CM"` | 900 |
| `"LVIII"` | 58 |
| `"MCMXCIV"` | 1994 |
| `"MMMCMXCIX"` | 3999 |
| `"IIII"` | `ValueError` |
| `"IC"` | `ValueError` |
| `""` | `ValueError` |
| `"mmxxii"` | `ValueError` |
| `None` | `TypeError` |
| `123` | `TypeError` |

### 2.3 Internal Constants and Helpers

Any internal constants or helper functions are private implementation details. They MUST NOT be exported as public API. The public API consists only of:

- `to_roman`
- `from_roman`

## 3. API ENDPOINTS

There are no HTTP API endpoints in this project. The utility is a standalone Python module.

The complete public interface is:

| Interface | Kind | Signature |
|---|---|---|
| `to_roman` | Python function | `to_roman(n: int) -> str` |
| `from_roman` | Python function | `from_roman(s: str) -> int` |

No admin configuration endpoints, export endpoints, webhook endpoints, Lambda triggers, Prometheus metrics endpoints, healthchecks, or observability endpoints are required.

## 4. FILE STRUCTURE

```text
.
└── src/
    └── roman.py   # Contains to_roman and from_roman implementations and private helper constants
```

**One-line description per file:**

| Path | Description |
|---|---|
| `src/roman.py` | Standalone Python module exporting `to_roman` and `from_roman`; no external dependencies |

No test files are included because the original user request does not explicitly request tests.

No `__init__.py` is required. The module `src/roman.py` may be imported as `src.roman` when the workspace root is on `sys.path`, or consumers may load the file directly.

No Dockerfile, no docker-compose, no startup script, no `.env.example`, no README is required.

### Port Table

No port table applies. This project contains no long-running service, no web server, no database, and no infrastructure that listens on a port.

### Shared Modules

No shared modules directory is required. The entire implementation lives in one file.

## 5. ENVIRONMENT VARIABLES

No environment variables are used by this utility.

The behavior of `to_roman` and `from_roman` is deterministic and does not depend on:

- Third-party API keys
- Service URLs
- Feature flags
- Credentials
- Runtime configuration
- Deployment environment

No `.env.example` file is required.

## 6. IMPORT CONTRACTS

The following public symbols must be importable from `src.roman`:

```python
from src.roman import to_roman
from src.roman import from_roman
```

Combined import:

```python
from src.roman import to_roman, from_roman
```

The module MUST define `__all__` as follows:

```python
__all__ = ["to_roman", "from_roman"]
```

No other names are public. Internal constants such as the descending numeral mapping MUST NOT appear in `__all__`.

### Function Signature Contract

```python
def to_roman(n: int) -> str:
    ...

def from_roman(s: str) -> int:
    ...
```

Consumers MUST be able to call these functions without passing additional arguments. Both functions are pure functions: no side effects, no I/O, no network access, no mutable global state.

## 7. FRONTEND STATE & COMPONENT CONTRACTS

Not applicable.

This project has no frontend framework, no UI components, no React hooks, no Vue composables, no Angular services, and no Svelte stores.

There are no browser-side state primitives and no reusable frontend components to specify.

## 8. FILE EXTENSION CONVENTION

- **Project language:** Python
- **Frontend files:** None
- **Frontend extension:** Not applicable — no `.jsx`, `.tsx`, `.js`, or `.ts` files exist
- **Backend/source files:** `.py`
- **Entry point:** `src/roman.py`
- **JavaScript/TypeScript entry point:** Not applicable — no `index.html` or `<script src>` is involved

The only source file is `/src/roman.py`.

## 9. DESIGN TOKENS

Not applicable.

No UI/UX Design Implementation Contract exists for this project. There are no visual tokens, colors, typography, spacing, border radius, shadows, or frontend styles to specify because the project has no user interface.

## 10. FUNCTIONAL REQUIREMENTS COVERAGE

| Requirement | Implementation | Files |
|---|---|---|
| Create `src/roman.py` | Single-file standalone utility module | `src/roman.py` |
| Expose public function `to_roman(n: int) -> str` | Function with exact signature and return type | `src/roman.py` |
| Convert integers 1..3999 to standard Roman numeral notation | Descending table iteration from 1000 down to 1, appending symbols while remaining division value exists | `src/roman.py` |
| Use subtractive notation `4 = "IV"` | Mapping entry `(4, "IV")` in descending numeral table | `src/roman.py` |
| Use subtractive notation `9 = "IX"` | Mapping entry `(9, "IX")` in descending numeral table | `src/roman.py` |
| Use subtractive notation `40 = "XL"` | Mapping entry `(40, "XL")` in descending numeral table | `src/roman.py` |
| Use subtractive notation `90 = "XC"` | Mapping entry `(90, "XC")` in descending numeral table | `src/roman.py` |
| Use subtractive notation `400 = "CD"` | Mapping entry `(400, "CD")` in descending numeral table | `src/roman.py` |
| Use subtractive notation `900 = "CM"` | Mapping entry `(900, "CM")` in descending numeral table | `src/roman.py` |
| `to_roman` raises `ValueError` when `n` is out of range | Explicit precondition: `if n < 1 or n > 3999: raise ValueError` | `src/roman.py` |
| `to_roman` raises `TypeError` when `n` is not `int` | Explicit type check before range check | `src/roman.py` |
| `to_roman` raises `TypeError` for `bool` | Explicit `isinstance(n, bool)` check before range check | `src/roman.py` |
| `to_roman` returns uppercase Roman numeral string | Only uppercase symbols used in mapping | `src/roman.py` |
| Expose public function `from_roman(s: str) -> int` | Function with exact signature and return type | `src/roman.py` |
| Convert standard Roman numeral notation to integer | Parse input string left-to-right, validate grammar, accumulate numeric value | `src/roman.py` |
| `from_roman` accepts standard subtractive Roman numerals | Grammar validation with allowed patterns `CM`, `CD`, `XC`, `XL`, `IX`, `IV` | `src/roman.py` |
| `from_roman` rejects non-standard forms such as `IIII`, `IC`, `IL`, `XD`, `XM` | Grammar enforcement or equivalent validation | `src/roman.py` |
| `from_roman` raises `TypeError` when `s` is not `str` | Explicit type check | `src/roman.py` |
| `from_roman` raises `ValueError` when `s` is invalid | Invalid grammar, empty string, unsupported characters, out-of-range value all raise `ValueError` | `src/roman.py` |
| `from_roman` returns integer in range 1..3999 | Validation ensures parsed value is within inclusive range | `src/roman.py` |
| Standalone utility with no external dependencies | Uses only Python standard library; no imports beyond standard library | `src/roman.py` |
| No network, no filesystem, no database access | Pure functions only | `src/roman.py` |
| Public API limited to `to_roman` and `from_roman` | `__all__ = ["to_roman", "from_roman"]` | `src/roman.py` |

### 10.1 Explicit Error Precedence for `to_roman`

The implementation MUST enforce this precedence:

1. If `n` is `bool`, raise `TypeError`.
2. If `n` is not `int`, raise `TypeError`.
3. If `n < 1`, raise `ValueError`.
4. If `n > 3999`, raise `ValueError`.
5. Otherwise, convert.

This means:

```python
to_roman(True)   # TypeError, not ValueError
to_roman(False)  # TypeError, not ValueError
to_roman(3.14)   # TypeError
to_roman(0)      # ValueError
to_roman(4000)   # ValueError
```

### 10.2 Explicit Error Precedence for `from_roman`

The implementation MUST enforce this precedence:

1. If `s` is not `str`, raise `TypeError`.
2. If `s` is empty or whitespace-only, raise `ValueError`.
3. If `s` contains characters outside `I`, `V`, `X`, `L`, `C`, `D`, `M`, raise `ValueError`.
4. If `s` violates the standard Roman numeral grammar, raise `ValueError`.
5. If the parsed value is outside 1..3999, raise `ValueError`.
6. Otherwise, return the integer.

This means:

```python
from_roman(None)      # TypeError
from_roman(123)      # TypeError
from_roman("")       # ValueError
from_roman("IIII")   # ValueError
from_roman("IC")     # ValueError
from_roman("MMMM")   # ValueError, would parse to 4000
```

### 10.3 Out of Scope

The following are explicitly NOT required:

- HTTP APIs or REST endpoints
- Webhooks
- Authentication or authorization
- Persistence layers or databases
- Caching
- Observability, metrics, tracing, or dashboards
- Frontend UI
- Deployment infrastructure
- Docker images
- Lambda functions
- PDF/CSV/HTML export
- Third-party integrations
- Internationalization/localization
- Support for values outside 1..3999
- Lowercase Roman numerals
- Non-standard Roman notation variants
- Roman numeral notation for zero or negative numbers

If any of these are needed in the future, they must be added as new explicit requirements; they must not be silently introduced into `src/roman.py`.