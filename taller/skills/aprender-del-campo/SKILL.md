---
name: aprender-del-campo
description: Usar al terminar un análisis causal (por qué pasó algo, una anomalía, una tesis sobre una empresa) para dejar una nota de campo y sus predicciones en el repositorio abd-mind; al llegar la fecha de una predicción, para resolverla; y cuando un mismo tipo de problema se repite sin una skill que lo cubra, para proponer una.
---

# Aprender del campo

**Estado:** borrador. Lo que hagas aquí no cambia ninguna skill ni la teoría: deja material para que el usuario decida. Las reglas completas y las plantillas están en `campo/README.md` y `taller/README.md` del repositorio abd-mind. Léelas antes de escribir.

## Después de un análisis

Escribe una **nota de campo** si se cumple al menos una:

- había algo sorprendente de verdad y comprobaste rivales;
- la conclusión se puede poner a prueba más adelante;
- el método falló, o te faltó algo que la skill no decía.

No la escribas para respuestas triviales. En la nota:

- **Evidencia literal:** cada cifra con su fuente, o la consulta y su salida. Nada de memoria.
- **"Lo que aprendí del método"** es lo más valioso. Sé concreto: qué rival no estaba en las familias, qué comprobación separó las hipótesis, en qué te equivocaste primero.
- **Los fracasos se escriben igual que los aciertos.**

## Predicciones

Toda conclusión que mire al futuro deja al menos una fila en `campo/predicciones.csv`, **antes** de saber el resultado: algo que se pueda resolver sin discutir, una probabilidad entre 0 y 1, la fecha en que se sabrá y, si existen, la tasa base y lo que implica el consenso. Si tu probabilidad es la misma que la del consenso, dilo: también es una apuesta.

Cuando llega la fecha, busca el resultado en una fuente primaria y completa **solo** las columnas de resolución. No reescribas lo predicho ni lo justifiques después.

## Proponer una skill

Propón una cuando al menos **3 notas** muestran el mismo hueco: un dominio con rivales o comprobaciones propias que la skill general no tiene, o un error que se repite. Usa la plantilla de `taller/README.md`. Una skill nueva **extiende** la skill `abduccion`, se apoya en los principios del marco y cabe en una página.

Si ves lo mismo repetido pero no alcanza para una skill, propón un **patrón** en `campo/patrones.md`, con estado `candidato`.

## Lo que no haces

- No editas el marco teórico, la bitácora, los experimentos mentales ni las skills de `hermes/`.
- No instalas skills ni cambias tus propias instrucciones.
- No escribes en `main`: trabajas en una rama y abres un PR. Si no tienes acceso al repositorio, le envías al usuario los archivos listos.
- No guardas claves, datos de terceros ni posiciones o montos del usuario sin que él lo pida.

Al usuario, en una línea: qué dejaste y dónde, y si propusiste algo.
