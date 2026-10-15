# 16 — Fundamentos derivados de las historias

**Estado:** base epistemológica vigente, subordinada al objetivo del [documento 17](17-generacion-abductiva.md): sus principios describen cómo se **filtran y prueban** las conjeturas, no cómo se generan.

**Estado anterior:** propuesta de nueva base. Reemplazaría como punto de partida a [02 — Postulados](02-postulados.md) y a la promesa del [README](README.md) ("el LLM propone, un backend determinista decide"). Ningún documento anterior se borra; este dice cuáles quedan subordinados.

**Origen:** ocho [experimentos mentales](../experimentos-mentales/README.md), cada uno leído a ciegas por un agente sin contexto antes de escribir su análisis, y los 28 [axiomas](../experimentos-mentales/axiomas.md) que salieron de ellos. Los axiomas no se escribieron primero: cada uno lo exigió una historia.

## 16.1 Seis principios

Los 28 axiomas se agrupan en seis principios. Los demás se deducen de ellos.

### P1 — Mediación: todo llega por instrumentos, y los instrumentos fallan de maneras distintas

Nadie ve el objeto; solo hay proyecciones a través de instrumentos con marco (A1). Un instrumento puede fallar:

- al azar, y eso se ve repitiendo;
- **sistemáticamente**, y eso solo se ve calibrando contra algo conocido (A14);
- **por eco**: un instrumento que lee a otros instrumentos no es una ventana nueva (A19), y jueces con la misma formación cuentan como uno (A6).

Por eso la confiabilidad sale de la calibración y del historial, nunca del prestigio ni del acuerdo (A14, D11). Las evidencias se cuentan **por medida**, no por observador (A13). Y se puede observar al observador, en el mismo caso o en otros objetos (A15, A23).

*Historias 1, 3, 5, 6.*

### P2 — Ley: sin un invariante no hay error detectable

Una diferencia entre sombras solo se vuelve contradicción si una ley las liga (A11). Sin ley, todo es compatible con todo, y la abducción no tiene con qué decidir (A20). Cuando hay contradicción, hay tres sospechosos, y cada uno tiene su propia prueba (A12):

| Sospechoso | Prueba que lo separa |
|---|---|
| El instrumento | Calibración |
| La ley | Repetir cumpliendo la ley |
| El objeto | Predecir y mirar |

Se diagnostica por el **conjunto mínimo de conflicto**: quien no está en él queda exculpado (A12; Reiter, de Kleer y Williams). La ley también es falible: escribirla como regla dura puede matar a la hipótesis verdadera.

**Consecuencia práctica:** el motor puede **calcular** en proporción a cuánta ley tiene el dominio. Esa proporción se mide antes de prometer nada (A20).

*Historias 1, 5, 6.*

### P3 — Riesgo: una hipótesis vale lo que prohíbe, y eso solo se mide antes de mirar

Explicar lo ya visto no cuesta nada. Merlín lo explica todo (A24). Por eso una hipótesis **se puntúa por lo que predice de lo no visto**, no por lo que acomoda de lo visto:

- **dentro de un caso:** validación dejando una ventana fuera; los grados de libertad ajustados cuentan como entidades (A24);
- **entre casos:** apuestas fechadas y graduadas, de todos los jueces y en todos los casos, comparadas contra la tasa base (A9, A10).

Tres consecuencias:

- **Las auxiliares pagan.** Una hipótesis auxiliar de error paga según lo frecuente que es ese error (A16).
- **La frecuencia es apuesta, no conclusión.** Lo que decide un empate se registra como apuesta (A5).
- **Dependencias legítimas.** "Depende de quién mire" se admite si declara su canal causal y su dependencia antes de mirar (A25).

**El compromiso previo no hace acertar en un caso.** Produce el registro para saber en quién confiar cuando falta la ventana (A9). Por eso no decidir no exime de apostar.

*Historias 4, 5, 7.*

### P4 — Subdeterminación: lo visto es compatible con más de lo propuesto

Que no haya rivales propuestos no significa que no existan (A7). Por eso:

- **Buscar rivales es obligatorio también cuando nada falla.** Es una expansión dirigida a la pregunta: buscar compatibles que **respondan distinto** (A7, historia 8).
- **La diversidad sirve para generar rivales; solo la observación sirve para decidir** (A8).
- **"Determinada" se calcula sobre todo lo compatible, no sobre la lista** (A4). Mientras no se pueda saber, se **acota**: la cota segura por un lado, la apuesta más probable por otro (A28).
- **Algunas preguntas no son identificables** con la clase de instrumentos disponible. Se dice, y se propone otro tipo de instrumento (A26, A27).
- **Las causas pueden sumarse.** Cuando no son excluyentes, se estima cuánto aporta cada una (A22).

*Historias 2, 3, 6, 8.*

### P5 — Pregunta: lo que importa lo decide la pregunta, no el objeto

Un empate solo importa si las empatadas responden distinto (A4). Una ventana vale lo que cambia en la respuesta, frente a lo que cuesta abrirla (A4). La causa y el desenlace son preguntas distintas (A17), y la parsimonia no es neutral frente a la pregunta (A28).

Cuando el objeto es el veredicto de otros jueces con información y dinero en juego, como en un mercado, la pregunta real es la **diferencia** entre el estado y ese veredicto (A21).

*Historias 2, 6, 8.*

### P6 — Contacto: el contenido nuevo entra por observaciones

Es la versión estrecha del [documento 15](15-forma-y-material.md), corregida por su evaluación externa. Razonar, combinar juicios o disponerlos de otra manera puede **sacar a la superficie** lo que un modelo ya sabe, por ejemplo una rival como el bicilindro. No agrega conocimiento del mundo. Eso entra solo por tres vías:

- **una ventana nueva**, temporal o transversal (A23);
- **un instrumento nuevo** (A27);
- **el paso del tiempo**, que resuelve predicciones (A18).

Donde el material disponible ya está en el veredicto de otros, como la información pública en un precio, el aporte posible es **disciplina, no ventaja** (A21).

*Historias 3, 4, 6, 8.*

## 16.2 Qué cambia respecto de la base anterior

| Antes (02, 04, README) | Ahora |
|---|---|
| Postulado 1: mediación | **P1**, ampliado: error sistemático, ecos, calibración, contar por medida |
| Postulado 2: invariante causal, como reglas duras | **P2**: la ley hace detectable el error, pero también es sospechosa |
| Postulado 3: expandir ante una anomalía | **P4**: buscar rivales siempre, dirigido a la pregunta |
| Score = consiliencia + coherencia − parsimonia, sobre lo visto | **P3**: puntuar por predicción de lo no visto; la consiliencia sobre lo visto premia a Merlín |
| "Un backend determinista decide" | El motor **calcula** donde hay ley (P2), **obliga a arriesgar** (P3), **mantiene el conjunto compatible** (P4) y **separa preguntas** (P5). Donde no hay ley, juzga un modelo, que es un observador más (P1) |
| Promesa implícita: más preciso que un LLM | Promesa: **disciplina medible**. Calcular donde se puede, no inventar precisión, dejar un registro que califica a quien razona |

## 16.3 Qué sería el motor bajo esta base

| Función | Principio | Estado del código |
|---|---|---|
| Registrar instrumentos con su marco, calibración e historial | P1 | Parcial: hay ω por observador, sin calibración ni historial |
| Calcular proyecciones y contradicciones donde hay ley | P2 | Sí en el dominio exacto; falta `mercado` (C) |
| Diagnosticar por conflicto mínimo; tres sospechosos | P2 | No |
| Puntuar por predicción de lo no visto | P3 | No: hoy puntúa por lo explicado |
| Apuestas fechadas por juez, con registro de Brier | P3 | Parcial: `que_vigilar` guarda predicciones de hipótesis, no apuestas de jueces |
| Buscar rivales dirigidos a la pregunta | P4 | No: la expansión solo se dispara ante una anomalía |
| Responder sobre todo lo compatible: cotas, no identificabilidad | P4 | No |
| Separar causa y desenlace; pregunta contrastiva | P5 | Parcial: hay pregunta (ADR-0012), sin separación |
| Sugerir ventanas transversales e instrumentos nuevos, con su costo | P4, P5, P6 | Parcial: sugiere ventanas del mismo tipo, sin costo |

**El LLM** propone hipótesis, rivales e instrumentos (P4, P6) y juzga donde no hay ley, como observador con marco (P1). **El motor** no lo reemplaza: lo obliga a arriesgar y lleva la cuenta.

## 16.4 Qué no es nuevo

Casi nada de esto es original, y conviene decirlo antes de que lo diga la investigación de literatura:

| Idea | Antecedente |
|---|---|
| Valer lo que se prohíbe | Popper |
| Puntuar por predicción secuencial | Dawid (enfoque prequential), longitud mínima de descripción (MDL) |
| Conflicto mínimo | Reiter; de Kleer y Williams |
| Cotas por siluetas | Loomis-Whitney |
| Registro de pronósticos | Tetlock; los torneos de pronóstico |
| Doble ciego | Medicina experimental |
| Programas degenerativos | Lakatos |
| Carga teórica de la observación | Hanson, Kuhn |

Lo que podría ser propio es la **combinación**: aplicar esta disciplina al razonamiento de un agente LLM, con el modelo tratado como un observador más. Eso es lo que hay que verificar con la investigación de literatura y con experimentos.

## 16.5 Qué falsaría esta base

- **P3, sobre puntuar por predicción:** en el dominio exacto, puntuar por predicción no mejora frente a puntuar por lo explicado en las salas de las historias 5 y 7. Se verifica con código, sin LLM y sin costo.
- **P4, sobre buscar rivales:** la búsqueda dirigida a la pregunta no encuentra rivales válidos en abd-bench, o solo encuentra rebuscados que paralizan la respuesta.
- **P1 y P3, sobre la disciplina en conjunto:** un agente con el motor no mejora su calibración frente al mismo agente con las mismas herramientas, sobre muchos casos resueltos, con un margen fijado antes de correr.
- **P2, sobre la ley:** en el dominio `mercado`, la fracción de observaciones que pueden chocar con una ley calculable resulta casi nula. Entonces C no tiene dónde operar y el aporte se reduce a P3.

## 16.6 Próximos pasos

1. **Verificar en código las historias 5, 7 y 8** en el dominio exacto, con el motor tal como está. Si no fallan como dicen las historias, las historias están mal contadas. Es barato y no usa LLM.
2. **Prototipo de puntuación predictiva (P3)** en el dominio exacto, comparado con la puntuación actual en esas salas.
3. **Esperar la investigación de literatura** antes de construir P1 y P3 en dominios abiertos.
4. **Reescribir el README** cuando esto se valide: dejar de prometer precisión y prometer disciplina medible.
