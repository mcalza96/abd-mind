# Principios

Seis principios que describen cómo se **filtran y prueban** las conjeturas. Salieron de ocho [experimentos mentales](../experimentos-mentales/README.md), cada uno leído a ciegas, y de los axiomas A1–A28 que esas historias exigieron ([axiomas](../experimentos-mentales/axiomas.md)). Reemplazan a los postulados originales ([histórico, 02](../historico/marco-teorico/02-postulados.md)). La versión extensa está en [histórico, 16](../historico/marco-teorico/16-fundamentos-desde-las-historias.md).

## P1 — Mediación

Todo llega por instrumentos con marco, y los instrumentos fallan de tres maneras:

- **al azar**, y eso se ve repitiendo;
- **sistemáticamente**, y eso solo se ve calibrando contra algo conocido;
- **por eco**, cuando un instrumento lee a otros instrumentos.

Por eso:

- la confiabilidad sale de la calibración y del historial, nunca del prestigio ni del acuerdo;
- jueces con la misma formación cuentan como uno;
- se puede observar al observador, en el caso o en otros objetos.

Las evidencias se cuentan por medida, pero un observador que no mide la cantidad en disputa **vota a través de las hipótesis** que ligan su medida con la disputada. Una explicación que vuelve consecuencia lo que para su rival es coincidencia gana por eso ([EXP-014](../bitacora/EXP-014-salas-en-codigo.md)).

## P2 — Ley

Una diferencia entre observaciones solo se vuelve contradicción si una ley las liga. Sin ley, todo es compatible y no hay error detectable.

Ante una contradicción hay tres sospechosos, y cada uno se descarta con su propia prueba:

| Sospechoso | Prueba |
|---|---|
| El instrumento | Calibrar |
| La ley | Repetir cumpliéndola |
| El objeto | Predecir y mirar |

Se diagnostica por el **conjunto mínimo de conflicto**: quien no está en él queda exculpado. La ley también es sospechosa, y escribirla como regla dura puede descartar la hipótesis verdadera. El motor puede **calcular** en proporción a cuánta ley tiene el dominio, así que eso se mide antes de prometer.

## P3 — Riesgo

Una hipótesis vale lo que prohíbe. Se puntúa por lo que predice de lo no visto, no por lo que acomoda de lo visto:

- dentro del caso, con validación dejando una fuera o con hechos reservados;
- entre casos, con apuestas fechadas, graduadas y completas, comparadas contra la tasa base.

Una predicción segura que falla cuesta más que no predecir nada. Las hipótesis auxiliares pagan según lo frecuente que es ese error, y la frecuencia se registra como apuesta, no como conclusión. **No decidir no exime de apostar.** "Depende de quién mire" se admite solo si declara su canal causal y su dependencia antes de mirar.

## P4 — Subdeterminación

Lo visto es compatible con más de lo propuesto. Por eso:

- **se buscan rivales también cuando todo calza**, y es justo ahí donde se apoya la generación abductiva;
- **"determinada" se calcula sobre todo lo compatible con lo visto**, no sobre la lista de candidatas;
- **mientras no se pueda saber, se acota:** se da la cota segura y, aparte, la apuesta más probable;
- **hay preguntas no identificables** con los instrumentos disponibles; se dice, y se propone otro tipo de instrumento;
- **las causas pueden sumarse.**

## P5 — Pregunta

Lo que importa lo decide la pregunta. Un empate solo importa si las empatadas responden distinto. Una ventana vale lo que cambia en la respuesta, frente a lo que cuesta abrirla.

La causa y el desenlace son preguntas distintas. Cuando el objeto es el veredicto de otros jueces, la pregunta real es la **diferencia** con ese veredicto.

## P6 — Contacto

El conocimiento nuevo del mundo entra solo por **observaciones nuevas, instrumentos nuevos o el paso del tiempo**. Razonar, combinar juicios o preguntar distinto puede sacar a la superficie lo que un modelo ya sabe, pero no agrega mundo. Donde el material disponible ya está en el veredicto de otros, el aporte posible es disciplina, no ventaja.

## Estado en el motor

| Función | Principio | Estado |
|---|---|---|
| Proyecciones y contradicciones donde hay ley | P2 | Sí, en el dominio exacto |
| Puntuación por predicción, con familias y error del observador | P3 | Opción (`puntuacion: predictiva`, EXP-015) |
| Predicciones de hipótesis (`que_vigilar`), verdad falible | P3 | Sí |
| Confiabilidad ω por observador | P1 | Sí, pero sin calibración ni historial |
| Sugerir la observación que separa | P4, P5 | Sí, pero solo ventanas del mismo tipo y sin costo |
| Pregunta del caso y respuesta contrastiva | P5 | Sí |
| Apuestas por juez con puntaje de Brier; crédito solo por lo dicho antes de mirar | P3 | No |
| Buscar rivales cuando todo calza; cotas; no identificabilidad | P4 | No |
| Conjunto mínimo de conflicto; error sistemático; contar ecos como uno | P1, P2 | No |
