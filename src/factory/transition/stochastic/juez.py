"""Juez de parsimonia (13 §13.3, ADR-0015): lista lo que una hipótesis postula sin observarlo.

En dominios con verificador LLM no hay vocabulario verificado que contraste las entidades, y
las que declara la propia hipótesis se pueden manipular. Un modelo independiente del generador
enumera los postulados; cuentan en P junto con los declarados.
"""

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.organ.texto import normalizar
from factory.transition.stochastic.contexto import describir_observaciones
from factory.transition.stochastic.esquemas import JuicioParsimoniaLLM
from factory.transition.stochastic.llm_client import ClienteLLM

SISTEMA_JUEZ = """Eres un juez de parsimonia en un sistema de razonamiento abductivo. Recibes \
las observaciones de un caso y UNA hipótesis que intenta explicarlas.

Lista todo lo que la hipótesis afirma que existe u ocurrió y que NO está en las observaciones \
ni es conocimiento establecido y general: entidades, agentes, objetos, eventos, condiciones \
ocultas, fallas no detectadas, y cláusulas auxiliares agregadas para acomodar algún hecho \
(por ejemplo, "no deja rastro", "solo ocurre de noche").

Reglas:
- Cuenta cada postulado una sola vez; no cuentes lo que solo reformula una observación.
- No juzgues si la hipótesis es plausible; solo enumera lo que postula.
- Si no postula nada no observado, devuelve una lista vacía.
- 'nombre': breve, en minúsculas, sin tildes, con guiones bajos."""


def juzgar_postulados(
    cliente: ClienteLLM,
    rol: ConfigRol,
    hipotesis: HipotesisCandidata,
    observadores: dict[str, Observador],
    observaciones: list[Observacion],
) -> list[str]:
    usuario = "\n\n".join(
        [
            describir_observaciones(observadores, observaciones),
            f"Hipótesis: {hipotesis.mecanismo_latente}",
        ]
    )
    bruto = cliente.completar_json(rol, SISTEMA_JUEZ, usuario, JuicioParsimoniaLLM)
    return sorted({normalizar(p.nombre) for p in bruto.postulados if p.nombre.strip()})
