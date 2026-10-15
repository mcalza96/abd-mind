"""Puntuación predictiva (EXP-015): validación dejando una fuera con error del observador."""

import math

import pytest

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.organ.projections import VerificadorProyeccion
from factory.transition.deterministic.prediccion import MAX_MIEMBROS, puntuar


def _proyectar(h: HipotesisCandidata, o: Observador) -> str | None:
    valor = h.afirmaciones.get(str(o.parametros["vista"]))
    return None if valor is None else str(valor)


def _obs(vista: str, valor: str, omega: float = 0.9) -> tuple[Observacion, Observador, float]:
    observador = Observador(id=vista, nombre=vista, parametros={"vista": vista})
    return (
        Observacion(id=vista, observador_id=vista, contenido=valor, valor=valor),
        observador,
        omega,
    )


PROYECTOR = VerificadorProyeccion(proyeccion=_proyectar)


def _universo(_: Observacion, __: Observador) -> int:
    return 4


def test_hipotesis_fija_es_su_log_verosimilitud() -> None:
    h = HipotesisCandidata(
        id_hipotesis="h", mecanismo_latente="m", afirmaciones={"a": "x", "b": "y"}
    )
    p = puntuar(h, [_obs("a", "x"), _obs("b", "z")], PROYECTOR, _universo)
    acierto, error = 0.9 + 0.1 / 4, 0.1 / 4
    assert p.por_observacion == pytest.approx({"a": acierto, "b": error})
    assert p.total == pytest.approx(math.log(acierto) + math.log(error))


def test_familia_que_acomoda_todo_no_predice() -> None:
    """Una vista libre por observación: lo oculto queda repartido entre todo el universo."""
    valores = ["x", "y", "z", "w"]
    merlin = HipotesisCandidata(
        id_hipotesis="merlin",
        mecanismo_latente="cualquier cosa",
        parametros_libres={"a": valores, "b": valores},
    )
    p = puntuar(merlin, [_obs("a", "x"), _obs("b", "y")], PROYECTOR, _universo)
    assert p.miembros == 16
    assert p.por_observacion["a"] == pytest.approx(0.25)


def test_familia_demasiado_grande() -> None:
    grande = HipotesisCandidata(
        id_hipotesis="g",
        mecanismo_latente="m",
        parametros_libres={f"v{i}": list(range(40)) for i in range(3)},
    )
    assert MAX_MIEMBROS < 40**3
    with pytest.raises(ValueError, match="miembros"):
        puntuar(grande, [_obs("a", "x")], PROYECTOR, _universo)
