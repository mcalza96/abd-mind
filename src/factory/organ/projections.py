"""Proyecciones computables y relación de consistencia ≈ (docs/marco-teorico/03 §3.3, D5).

El entorno sintético de sólidos actúa como "realidad" verificable: dado el sólido que afirma una
hipótesis y la vista de un observador, la silueta se calcula sin ningún LLM.
"""

from collections.abc import Callable, Iterable, Mapping

from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.case import Relacion, Veredicto
from factory.contracts.observation import Observacion, Observador
from factory.organ.texto import normalizar

# Silueta de cada sólido (eje vertical) según la vista del observador.
SILUETAS: Mapping[str, Mapping[str, str]] = {
    "esfera": {"frontal": "circulo", "cenital": "circulo", "lateral": "circulo"},
    "cubo": {"frontal": "cuadrado", "cenital": "cuadrado", "lateral": "cuadrado"},
    "cilindro": {"frontal": "rectangulo", "cenital": "circulo", "lateral": "rectangulo"},
    "cono": {"frontal": "triangulo", "cenital": "circulo", "lateral": "triangulo"},
    "elipsoide": {"frontal": "elipse", "cenital": "circulo", "lateral": "elipse"},
    # Cilindro cortado en cuña por dos planos: rectángulo, círculo y triángulo.
    "tapon_universal": {"frontal": "rectangulo", "cenital": "circulo", "lateral": "triangulo"},
}

Proyeccion = Callable[[HipotesisCandidata, Observador], Valor | None]


def proyectar_solido(hipotesis: HipotesisCandidata, observador: Observador) -> Valor | None:
    """π_i para el entorno de sólidos: silueta del sólido afirmado vista desde el observador."""
    solido = hipotesis.afirmaciones.get("solido")
    vista = observador.parametros.get("vista")
    if not isinstance(solido, str) or not isinstance(vista, str):
        return None
    return SILUETAS.get(normalizar(solido), {}).get(normalizar(vista))


class RelacionConsistencia:
    """π_i(H) ≈ y_i ⇔ d_i(π_i(H), y_i) ≤ ε_i.

    Categórico: igualdad tras normalizar, o pertenencia declarada en `jerarquia`
    (específico → categorías que lo incluyen, p. ej. {"cuadrado": ["rectangulo"]}).
    Numérico: diferencia absoluta dentro de la tolerancia del observador.
    """

    def __init__(self, jerarquia: Mapping[str, Iterable[str]] | None = None) -> None:
        self.jerarquia = {
            normalizar(k): {normalizar(v) for v in vs} for k, vs in (jerarquia or {}).items()
        }

    def consistente(self, predicho: Valor, observado: Valor, tolerancia: float = 0.0) -> bool:
        if isinstance(predicho, bool) or isinstance(observado, bool):
            return type(predicho) is type(observado) and predicho == observado
        if isinstance(predicho, int | float) and isinstance(observado, int | float):
            return abs(predicho - observado) <= tolerancia
        if isinstance(predicho, str) and isinstance(observado, str):
            p, o = normalizar(predicho), normalizar(observado)
            return p == o or o in self.jerarquia.get(p, set())
        return False


class VerificadorProyeccion:
    """Verificador determinista para entornos donde π_i es computable."""

    fuente = "proyeccion"

    def __init__(
        self,
        proyeccion: Proyeccion = proyectar_solido,
        relacion: RelacionConsistencia | None = None,
        variable_observada: str | None = "silueta",
    ) -> None:
        self.proyeccion = proyeccion
        self.relacion = relacion or RelacionConsistencia()
        # Variable del hecho que se compara cuando la observación no trae `valor`
        # (p. ej. la que extrae el córtex de un texto libre).
        self.variable_observada = variable_observada

    def observado(self, observacion: Observacion) -> Valor:
        if observacion.valor is not None:
            return observacion.valor
        if self.variable_observada and self.variable_observada in observacion.variables:
            return observacion.variables[self.variable_observada]
        return observacion.contenido

    def predecir(self, hipotesis: HipotesisCandidata, observador: Observador) -> Valor | None:
        return self.proyeccion(hipotesis, observador)

    def consistente(
        self, predicho: Valor, observacion: Observacion, observador: Observador
    ) -> bool:
        return self.relacion.consistente(
            predicho, self.observado(observacion), observador.tolerancia
        )

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        observado = self.observado(observacion)
        predicho = self.proyeccion(hipotesis, observador)
        if predicho is None:
            relacion = Relacion.NEUTRAL
            justificacion = "la hipótesis no permite proyectar lo que vería este observador"
        else:
            explica = self.relacion.consistente(predicho, observado, observador.tolerancia)
            relacion = Relacion.EXPLICA if explica else Relacion.CONTRADICE
            simbolo = "≈" if explica else "≉"
            justificacion = f"π({observador.id}) = {predicho} {simbolo} {observado}"
        return Veredicto(
            id_hipotesis=hipotesis.id_hipotesis,
            id_observacion=observacion.id,
            relacion=relacion,
            fuente=self.fuente,
            justificacion=justificacion,
        )
