# Patch manuel (si tu ne veux pas de script)

Dans common/utils.py, remplace la signature de perf_timer vers PEP 695.

## Variante A (cas le plus courant)
Avant:
  from typing import Callable, ParamSpec, TypeVar
  P = ParamSpec("P")
  R = TypeVar("R")

  def perf_timer(func: Callable[P, R]) -> Callable[P, R]:
      ...

Après:
  from typing import Callable

  def perf_timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:
      ...

## Variante B (si P/R sont ailleurs)
Si P et R sont déjà définis/partagés plus haut et tu veux les garder (moins propre mais possible),
l'essentiel est d'avoir:
  def perf_timer[**P, R](...)

Puis:
  - supprimer les lignes P = ParamSpec("P") / R = TypeVar("R") si elles deviennent inutiles
  - supprimer ParamSpec/TypeVar des imports si inutiles
