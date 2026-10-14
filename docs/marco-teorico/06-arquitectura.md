# 06 — Arquitectura del pipeline

## 6.1 Principio rector

> **El LLM propone, la infraestructura decide.**

El pipeline separa el razonamiento **estocástico** (lenguaje, generación de ideas) del razonamiento **determinista** (cálculo, verificación, selección). Cada frontera entre ambos es un contrato de datos tipado y validado.

## 6.2 Módulos

```
 [Observaciones crudas y_i]
            │
            ▼
 ┌────────────────────────────┐
 │ 1. Córtex perceptivo (LLM) │  lenguaje natural → hechos, entidades, predicados
 └─────────────┬──────────────┘
               │ JSON tipado (Pydantic)
               ▼
 ┌────────────────────────────┐
 │ 2. Generador de hipótesis  │  muestreo contrastivo / árbol de búsqueda
 │    (LLM, varios modelos)   │  + modo de expansión ontológica
 └─────────────┬──────────────┘
               │ 𝓗 = {H_1 … H_n}
               ▼
 ┌────────────────────────────┐      ┌──────────────────────────┐
 │ 3. Verificación de virtudes│ ───► │ Proyecciones / verificador│  → C
 │                            │ ───► │ Extractor de entidades    │  → P
 │                            │ ───► │ Motor de reglas           │  → K
 └─────────────┬──────────────┘      └──────────────────────────┘
               ▼
 ┌────────────────────────────┐
 │ 4. Tronco determinista     │  Score(H) = αC + βK − γP, umbral τ, desempate
 │    (Python puro)           │
 └─────────────┬──────────────┘
               ▼
 ┌────────────────────────────┐
 │ 5. Árbol de estados        │  hipótesis vivas / derrotadas, evidencia,
 │    (derrotabilidad)        │  reevaluación ante y_k nuevo
 └────────────────────────────┘
```

| # | Módulo | Función | Naturaleza |
|---|---|---|---|
| 1 | **Córtex perceptivo** | Traduce observaciones ruidosas y desestructuradas a hechos, entidades y predicados; separa hechos de opiniones del observador | LLM, salida estructurada |
| 2 | **Generador de hipótesis** | Expande el espacio de hipótesis con explicaciones divergentes y mutuamente excluyentes; postula latentes cuando hace falta | LLM, alta diversidad |
| 3 | **Verificación de virtudes** | Produce los insumos de $C$, $P$, $K$ de forma independiente del generador | Mixto: código + LLM verificador acotado |
| 4 | **Tronco determinista** | Calcula el score, aplica umbral y desempate, selecciona $H^*$ | Python puro, sin IA |
| 5 | **Árbol de estados** | Mantiene el estado del razonamiento y aplica la derrotabilidad | Python puro, sin IA |

## 6.3 Frontera estocástico / determinista

| Decisión | ¿Puede tomarla un LLM? |
|---|---|
| Extraer hechos de un texto | Sí (validado contra esquema) |
| Proponer hipótesis | Sí |
| Postular una entidad latente | Sí (y paga parsimonia) |
| Decidir si $H$ explica $y_i$ en dominio real | Sí, **solo** como verificador independiente, una observación por llamada |
| Contar entidades latentes de $H$ | Insumo sí; el conteo y el contraste con $\mathcal{V}$ son código |
| Decidir si $H$ viola una regla | **No** — motor de reglas |
| Calcular el score | **No** |
| Elegir la hipótesis ganadora | **No** |
| Declarar derrotada una hipótesis | **No** — consecuencia de $\approx$ y del árbol de estados |

Si un componente del lado determinista necesita llamar a un LLM para tomar su decisión, la frontera está mal trazada.

## 6.4 Generación: aproximar una búsqueda no guiada por verosimilitud

El ideal teórico ([07](07-estado-del-arte.md#el-vacío-formal)) es buscar hipótesis optimizando directamente las virtudes, sin pasar por la distribución de tokens. Con un LLM accedido por API eso no es posible. El proyecto lo **aproxima** con:

1. **Muestreo contrastivo.** Cada nueva ronda recibe las hipótesis ya propuestas y debe producir explicaciones mutuamente excluyentes con ellas.
2. **Diversidad de modelos.** Varios modelos distintos generan en paralelo; sus sesgos de corpus no coinciden del todo.
3. **Temperatura alta en generación, baja en verificación.** Divergir al proponer, converger al juzgar.
4. **Búsqueda en árbol.** Las hipótesis prometedoras se refinan; el score determinista (no la probabilidad del LLM) decide qué rama expandir.
5. **Instrucción explícita de expansión** cuando se cumple la condición de [03, §3.5](03-formalizacion.md#35-ampliación-ontológica).

Es una aproximación y se trata como tal en [08](08-decisiones-y-limitaciones.md).

## 6.5 Uso del contexto extenso

La disponibilidad de ventanas de contexto amplias permite pasar entre módulos representaciones **completas**, sin resumir: el córtex ve toda la evidencia cruda, el verificador ve la hipótesis completa. Dos salvaguardas:

- El verificador recibe **solo** la tripleta $(H, O_i, y_i)$ y las reglas pertinentes, nunca el resto de las observaciones ni los scores, para que no racionalice hacia una conclusión.
- La prueba de estrés de contexto ([05, §5.5](05-experimentos-canonicos.md#55-pruebas-que-derivan-de-estos-experimentos)) verifica que el rendimiento no se degrada con muchas reglas de fondo.

## 6.6 Contratos de datos

Contratos mínimos de la especificación (Python 3.12, Pydantic):

```python
class HipotesisCandidata(BaseModel):
    id_hipotesis: str
    mecanismo_latente: str            # descripción causal invariante
    entidades_latentes: list[str]     # declaradas por el generador (referencia para P)
    observaciones_explicadas: list[str]  # declaradas por el generador (predicción auditable para C)
    predicados_de_consistencia: list[str]  # insumo para K

class EvaluacionAbductiva(BaseModel):
    id_hipotesis: str
    parsimonia_p: int
    consiliencia_c: int
    coherencia_k: float
    score_final: float
```

Ampliaciones que el marco requiere (detalle en [08](08-decisiones-y-limitaciones.md)):

- `Observer` y `Observation`: toda observación con su observador y marco (Postulado 1).
- Predicados **estructurados** para $K$ (variable, operador, valor) además del texto.
- Registro por observación del veredicto $\pi_i(H) \approx y_i$, con su fuente (función de proyección o verificador) y justificación.
- Estado de la hipótesis (`VIVA`, `DERROTADA`) con la evidencia que la derrotó.

## 6.7 Estructura del código

Según las instrucciones de implementación:

```
src/factory/
├── contracts/abduction.py                   # contratos Pydantic
├── organ/rule_engine.py                     # motor de reglas (K)
└── transition/deterministic/ibe_evaluator.py  # score y selección
tests/units/test_ibe_evaluator.py
```

Los módulos con LLM (córtex, generador, verificador) se agregan junto a estos, detrás de una interfaz de cliente que no fija proveedor ni modelo: la asignación de modelos a roles es configuración.
