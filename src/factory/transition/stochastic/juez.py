"""Juez de parsimonia (13 §13.3, ADR-0015): lista lo que cada hipótesis postula sin observarlo.

En dominios con verificador LLM no hay vocabulario verificado que contraste las entidades, y
las que declara la propia hipótesis se pueden manipular. Un modelo independiente del generador
enumera los postulados; cuentan en P junto con los declarados.

El juicio es comparativo (EXP-009 → EXP-010): un lote de hipótesis nuevas se juzga en una sola
llamada, con las ya registradas y sus postulados como referencia, para que todas se midan con
la misma granularidad. Sin ese punto de comparación el modelo sobrecontaba.
"""

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.organ.texto import normalizar
from factory.transition.stochastic.contexto import describir_observaciones
from factory.transition.stochastic.esquemas import JuicioParsimoniaLLM
from factory.transition.stochastic.llm_client import ClienteLLM

SISTEMA_JUEZ = """Eres un juez de parsimonia en un sistema de razonamiento abductivo. Recibes \
las observaciones de un caso y varias hipótesis rivales que intentan explicarlas.

Para cada hipótesis a juzgar, lista sus POSTULADOS: entidades, agentes o eventos independientes \
cuya existencia la hipótesis afirma y que ninguna observación registra.

NO son postulados:
- lo que solo reformula o resume una observación;
- negaciones o ausencias ("no hubo pérdida real");
- afirmaciones sobre qué observación es correcta o incorrecta;
- pasos, partes o consecuencias de otro postulado: si dos elementos solo existen juntos, son uno;
- conocimiento científico establecido y general.

Una cláusula agregada solo para acomodar un hecho ("no deja rastro") SÍ es un postulado.

Usa la MISMA granularidad para todas las hipótesis; las ya juzgadas, si las hay, sirven de \
referencia. La mayoría de las hipótesis postula entre cero y tres cosas. Responde solo nombres \
breves, en minúsculas, sin tildes y con guiones bajos."""


def juzgar_postulados(
    cliente: ClienteLLM,
    rol: ConfigRol,
    nuevas: list[HipotesisCandidata],
    observadores: dict[str, Observador],
    observaciones: list[Observacion],
    juzgadas: list[HipotesisCandidata] | None = None,
) -> dict[str, list[str]]:
    """Postulados de cada hipótesis nueva, por id. `juzgadas` sirven solo de referencia."""
    if not nuevas:
        return {}
    partes = [describir_observaciones(observadores, observaciones)]
    if juzgadas:
        partes.append(
            "Hipótesis ya juzgadas (referencia de granularidad; no las juzgues de nuevo):\n"
            + "\n".join(
                f"- {h.id_hipotesis}: {h.mecanismo_latente} → postulados: "
                f"{', '.join(h.entidades_juzgadas) or 'ninguno'}"
                for h in juzgadas
            )
        )
    partes.append(
        "Hipótesis a juzgar:\n"
        + "\n".join(f"- {h.id_hipotesis}: {h.mecanismo_latente}" for h in nuevas)
    )
    bruto = cliente.completar_json(rol, SISTEMA_JUEZ, "\n\n".join(partes), JuicioParsimoniaLLM)
    ids = {h.id_hipotesis for h in nuevas}
    resultado: dict[str, list[str]] = {i: [] for i in ids}
    for juicio in bruto.juicios:
        if juicio.id_hipotesis in ids:
            resultado[juicio.id_hipotesis] = sorted(
                {normalizar(p) for p in juicio.postulados if p.strip()}
            )
    return resultado
