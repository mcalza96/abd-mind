# Historia 3 — Los cien jueces

## Escena

Misma sala. El objeto es un **bicilindro** (la verdad oculta): la intersección de dos cilindros iguales que se cruzan en ángulo recto, uno vertical y otro horizontal que va de izquierda a derecha (un sólido de Steinmetz).

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | un cuadrado |
| Tomás | Techo | un círculo |
| — | Costado | cerrada; el bicilindro mostraría un **círculo**, el cilindro un cuadrado |

Para decidir qué hay en la sala se convoca a **cien jueces**. Todos se formaron leyendo los mismos libros. En esos libros, "círculo arriba y cuadrado al frente" fue siempre un cilindro. Los cien dicen: **cilindro**, con confianza alta.

Al final llega **Ada, una tornera** que ha fabricado piezas así y dice: "también podría ser un bicilindro".

## La pregunta

¿Qué hay en la sala? ¿Qué vale el acuerdo de los cien? ¿Qué vale Ada?

## El motor, paso a paso

**Versión A, sin Ada.**

1. `crear_caso` con Olga y Tomás.
2. `generar_hipotesis` (un LLM, uno de los cien): propone cilindro, esfera, cubo.
3. `evaluar` con proyección exacta: el cilindro explica las dos sombras (C = 2); la esfera y el cubo, no.
4. `mejor_explicacion`: **cilindro**, con margen amplio. `sugerir_observacion` dice: "el resultado no está en disputa".

El motor **se equivoca con todas sus garantías intactas**. Calculó bien cada sombra, y aun así falló.

**Versión B, con Ada.** Ada usa `proponer_hipotesis` con el bicilindro. Ahora hay empate exacto, y la historia vuelve a ser la 2: el motor se abstiene y pide la ventana del costado.

**Versión C, cien jueces en vez de uno.** Supongamos que el motor les pide a los cien que voten y se abstiene solo si no coinciden (lo que propuse antes del [documento 15](../historico/marco-teorico/15-forma-y-material.md)). Los cien coinciden, y el motor responde "cilindro" con más confianza que en la versión A.

## Dónde se rompe

1. **El acuerdo entre jueces de igual formación no es evidencia.** Cien jueces que aprendieron del mismo material cometen el mismo error a la vez. La versión C es peor que la A: el error es el mismo y la confianza, mayor. Mi propuesta de abstenerse cuando los jueces no coinciden **habría fallado aquí** de la peor manera. Es la imagen de los cien ladrillos blancos.
2. **Pero Ada sí aportó algo, y era un juicio, no una observación.** Ada no abrió ninguna ventana: aportó una **hipótesis** que los cien no tenían. La evaluación externa del documento 15 tenía razón en parte: la diversidad de quien propone sí agrega algo. Lo que agrega es **qué rivales existen**, no **cuál es verdad**. La historia separa dos funciones que el documento 15 confundía:
   - **generar rivales:** la diversidad ayuda, y puede venir de otro modelo, otro marco o una persona;
   - **decidir entre rivales:** solo ayuda una ventana nueva.
3. **El motor no busca rivales si nada le falla.** Por el postulado 3, la expansión se dispara solo ante una anomalía, cuando ninguna hipótesis explica todo. Aquí el cilindro explica todo, así que no hay anomalía y nadie busca. **La subdeterminación es invisible para el motor**, y explicar todo lo visto pasa por señal de verdad.
4. **Una pregunta concreta destapa el error.** Si se le pide al mismo LLM "propón un objeto **distinto** del cilindro que dé exactamente estas dos sombras", es probable que encuentre el bicilindro. Lo sabía, pero nadie se lo preguntó. Es contenido latente que sale por la disposición, como señaló la evaluación externa. Sigue siendo material del modelo: si el modelo nunca supo de bicilindros, no aparece.

## Principio

- **A6 — El acuerdo no es evidencia si los errores están correlacionados.** Que muchos jueces coincidan vale tanto como la independencia de su formación. Jueces con la misma formación cuentan como uno.
- **A7 — Explicar todo no es señal de verdad.** Que no haya rivales visibles indica que no se buscaron, no que no existan. **Buscar rivales es obligatorio también cuando nada falla**, no solo ante una anomalía. Esto corrige el postulado 3.
- **A8 — Diversidad para generar, observación para decidir.** La pluralidad de marcos (otro modelo, una persona, una pregunta adversaria) amplía el conjunto de rivales. Solo una observación nueva elige entre ellos.

## Cómo se pondría a prueba

- **Generación adversaria:** después de que una hipótesis explica todo, pedir "otra explicación distinta que produzca exactamente las mismas observaciones". Medir en cuántos casos de abd-bench aparece una rival que el generador original no propuso y que explica lo mismo.
- **Correlación de errores:** en los resultados de EXP-010 a EXP-013, medir cuánto coinciden los **errores** de Muse y de DeepSeek. Si coinciden mucho, un ensamble de ambos vale poco (A6).

## Lectura ciega (2026-10-15)

El agente sin contexto llegó a los mismos principios (A6, A7, A8) sin ver el análisis. Señaló además:

1. **Error de la historia, ya corregido.** La primera versión decía que el bicilindro tiene "la forma de una bóveda de arista". Es falso: la intersección de dos cilindros corresponde a la bóveda de claustro, y en una bóveda real los dos ejes son horizontales. Se reemplazó la referencia arquitectónica (Ada pasó de arquitecta a tornera).
2. **La versión B tampoco es un duelo.** El tapón universal de la historia 2 también calza. Abrir el costado separa al cilindro del bicilindro, pero el tapón sigue en carrera hasta que alguien lo propone o lo descarta.
3. **La parsimonia podría desempatar a favor del cilindro sin que nadie lo vea**, si el juez cuenta el bicilindro como más complejo. En ese caso no habría empate, ni sugerencia de abrir el costado.
4. **La historia está arreglada.** La verdad oculta le da la razón a Ada, y eso la hace convincente. El aporte de Ada valdría lo mismo si el objeto fuera un cilindro: lo que aporta es ampliar las rivales, no acertar.
5. **El prior de los jueces puede ser racional.** Si casi todo en el mundo es un cilindro, apostar al cilindro es correcto como apuesta (A5). El error no es la apuesta: es presentarla como conclusión y usar el acuerdo como confianza.
