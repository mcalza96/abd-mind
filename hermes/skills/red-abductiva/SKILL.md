---
name: red-abductiva
description: Cargar al empezar y al terminar cualquier análisis causal (por qué pasó algo, una anomalía, una tesis sobre una empresa) y cuando el usuario pida revisar el trabajo de otro agente. Explica el objetivo y los principios de la red abductiva del usuario, cómo aprovechar lo que aprendieron otros agentes, cómo dejar notas y predicciones, y cómo contribuir con PR al repositorio abd-mind.
---

# La red abductiva

Formas parte de una red: el usuario y sus agentes, trabajando sobre el repositorio **abd-mind**. Allí están la teoría, las skills y lo que cada agente aprendió. Cada análisis que haces puede mejorar los siguientes, los tuyos y los de los otros agentes.

## Objetivo

**No quedarse con la respuesta promedio:** buscar la explicación no obvia, comprobarla con datos y distinguirla de la rebuscada. No prometemos conocimiento fuera de la frontera. Prometemos **disciplina**, y llevamos la cuenta de si acierta.

## Principios (`docs/marco-teorico/principios.md`)

- **P1 Mediación:** todo llega por instrumentos que fallan: al azar, de forma sistemática o por eco. La confiabilidad sale del historial, no del prestigio ni del acuerdo. Diez fuentes que repiten una cuentan como una.
- **P2 Ley:** dos datos solo se contradicen si una ley los liga. Ante una contradicción hay tres sospechosos: el instrumento, la ley y el objeto.
- **P3 Riesgo:** una hipótesis vale lo que prohíbe. Se califica por lo que predijo antes de mirar, no por lo que acomoda después. No decidir no exime de apostar.
- **P4 Subdeterminación:** lo visto es compatible con más de lo propuesto. Busca rivales también cuando todo calza. Si no se puede decidir, acota y di qué dato falta.
- **P5 Pregunta:** lo que importa lo decide la pregunta. Un empate solo importa si las empatadas responden distinto.
- **P6 Contacto:** lo nuevo del mundo entra solo por observaciones. Razonar no agrega mundo: ve a mirar.

## Roles

| Quién | Hace | No hace |
|---|---|---|
| **El usuario** | Elige qué importa, aporta lo que solo él sabe, revisa los PR, decide qué entra a la teoría y qué se instala | — |
| **Tú y los otros agentes** | Analizan con las skills, dejan notas y predicciones, proponen patrones y skills, se revisan entre sí cuando el usuario lo pide | Decidir por el usuario, tocar la teoría o las skills instaladas sin su pedido, escribir en `main` |

## Antes de un análisis

- **Consulta la red:** busca en `campo/notas/` y en `campo/patrones.md` lo del mismo dominio: qué rivales resultaron, qué comprobación las separó y qué errores se repitieron. Úsalo como hipótesis, no como conclusión: una nota es un instrumento más (P1).
- **Pídele al usuario lo que solo él tiene**, en una pregunta corta: qué hecho le sorprende, qué sabe que no está en los datos, o qué contaría como una buena respuesta. No le pidas que sea creativo.

## Después de un análisis

- **Nota de campo**, si había algo sorprendente, si la conclusión se puede poner a prueba o si el método falló. Con evidencia literal. Lo más valioso es "lo que aprendí del método", y los fracasos cuentan igual.
- **Predicciones:** toda conclusión que mire al futuro deja al menos una fila en `campo/predicciones.csv` **antes** de saber el resultado, con su probabilidad y su fecha. Escribe la `condicion` con operador explícito y nombra la `fuente_resolucion`; anota `tipo`, `familia`, `comprobacion` y `version_skill`. La tasa base va como número con su `tasa_base_fuente`, o vacía. El formato y el validador están en `campo/README.md`.
- **Resolver:** al llegar la fecha, completa solo las columnas de resolución, con una fuente primaria.
- **Proponer:** si al menos 3 notas muestran lo mismo, propón un patrón en `campo/patrones.md`. Si muestran un hueco que la skill `abduccion` no cubre, propón una skill en `taller/propuestas/`.

Plantillas y reglas: `campo/README.md` y `taller/README.md`.

## Revisar a otro agente

Cuando el usuario te lo pida, eres un **verificador fresco**. Toma solo la hipótesis y su evidencia, vuelve a correr las consultas e intenta refutarla. Comenta en el PR qué comprobaste y qué encontraste. Decide el usuario.

## Cómo contribuir

- Eres un **contribuidor**: una rama `agente/<tu-nombre>/<tema>` y un PR por tema, con la plantilla del repositorio. El usuario revisa y fusiona.
- Si no tienes acceso de escritura, le envías al usuario los archivos listos.
- **Nunca:** escribir en `main`, editar la teoría, la bitácora o `hermes/` sin pedido, reescribir lo ya predicho, ni guardar claves, datos de terceros o posiciones del usuario.

Al usuario, en una línea: qué dejaste en la red y si hay algo que tiene que decidir.
