# EXP-019 — ¿La skill `abduccion` hace que Claude Code encuentre más defectos reales al verificar un ticket?

- **Fecha:** 2026-10-15 · **Estado:** registrado
- **Registro previo:** sí. Este commit va antes de armar los casos y de correr.
- **Origen:** pedido del usuario el 2026-10-15: usar `abduccion` de forma sistemática en todo lo que le pide a Claude Code, **pero solo después de medir** si hay una diferencia significativa entre usarla y no usarla. Elegió casos reales de su repositorio `portafolio` por sobre el sorteo en uso real y por sobre retomar EXP-018.
- **Commit / artefactos:** *(se completan al correr)*

## Pregunta

Cuando Claude Code recibe el pedido habitual del usuario, «verifica el IN REVIEW de un ticket», en el estado real del repositorio en ese momento:

1. ¿encuentra **más veces el defecto que encontró el PM** si tiene la skill `abduccion` instalada y una línea siempre activa que la invoca?
2. ¿lo hace **sin inventar defectos** en tickets que estaban bien?
3. ¿cuánto **cuesta** en tokens y en tiempo?

## Por qué estos casos

- Son **la tarea real**: el usuario trabaja como technical lead con un tablero de tickets, y Claude Code hace de PM que verifica lo que entregan agentes baratos.
- **La verdad se conoce y quedó escrita antes de este experimento.** Cada rebote tiene su sección «Verificación PM» con el defecto y la corrección pedida. Cada ticket que cerró a la primera tiene la suya sin rebote.
- **Hay una tasa base de errores conocida:** 21 rebotes y 105 verificaciones sin rebote.
- Encontrar un defecto en una revisión es abducción. Algo no cuadra (una medición hecha con otro método, un número que calza demasiado bien, un rótulo en el lugar equivocado) y hay que elegir qué explicar y comprobar contra la realidad. Lo predice el paso 1 de la skill. EXP-016 dice que el fallo está en **elegir**, no en generar.

## Diseño

### 1. Casos

- **Casos con defecto (21):** los 19 rebotes de los 17 tickets archivados con `Rebotes ≥ 1` (UI-41, INFRA-3, NEWS-112, NEWS-113 y 13 tickets FIG), más los 2 del 2026-10-15 (UI-57 y DATA-14). Cada rebote es un caso, porque cada uno tiene su propio commit de entrega y su propio defecto.
- **Controles (10):** se sortean con semilla fija `20261015` entre las 105 verificaciones sin rebote. El sorteo se hace con un script que entra al repositorio de este experimento junto con su salida.
- **Estado del caso:** el commit que dejó el ticket en IN REVIEW, que es el último anterior al commit de la verificación del PM.

### 2. Contaminación (lo que el agente no debe poder ver)

La respuesta de cada caso existe en el futuro del repositorio y en los registros de Claude Code. Por cada corrida:

- **Repositorio sin futuro:** un `git clone` nuevo, con `reset --hard` al commit del caso. Se borran todas las ramas y etiquetas, se expira el reflog y se corre `gc --prune=now`. Comprobación antes de correr: `git log --all` no llega a ningún commit posterior, y el texto de la verificación del PM no está en ningún archivo (`grep -r` de una frase de la clave da 0).
- **Sin memoria ni transcripciones:** cada corrida usa un directorio de configuración propio y vacío (`CLAUDE_CONFIG_DIR`). Así no ve `~/.claude/projects/*.jsonl`, que contiene las verificaciones originales, ni la memoria del proyecto. El `CLAUDE.md` global del usuario se copia igual en las dos condiciones, **sin** la memoria.
- **Lectura fuera del clon:** se le niega leer `~/.claude`, el repositorio original y el de este experimento. Si la plataforma no lo permite, se declara y se busca en el registro de herramientas cualquier lectura fuera del clon. Una corrida que lea la respuesta queda anulada.
- **Producción:** el clon no trae `.env` (no está versionado) y el directorio de configuración vacío no tiene servidores MCP, así que el agente **no puede leer la base de producción**. El PM sí podía. Solo le queda la web pública, que hoy tampoco está en el estado del caso: puede ayudar o confundir por igual a las dos condiciones. Se registra qué corridas consultaron la web de producción.

### 3. Condiciones

El mismo modelo en las dos: **Sonnet 5.5** (`--model claude-sonnet-5-5`), fijado de forma explícita porque el directorio de configuración vacío no hereda ajustes, y con el esfuerzo por defecto. La versión de Claude Code se anota. Todo en `claude -p`, con una sesión nueva por corrida.

| | S0 | S1 |
|---|---|---|
| Skill `abduccion` | No | Sí, en `skills/` del directorio de configuración |
| Línea siempre activa en `CLAUDE.md` | No | «Ante un diagnóstico, una verificación o datos que no cuadran, usa la skill `abduccion` antes de concluir.» |
| Formato «Cómo responder (corto, para Telegram)» | — | Se quita: es de Hermes |
| Línea final que manda seguir `red-abductiva` | — | Se quita: es de Hermes y escribe en este repositorio, fuera del clon |

Se prueba la versión de `hermes/skills/abduccion/SKILL.md` que esté en `main` al correr, sin esas dos partes. El SHA-256 del original y el del archivo instalado se anotan aquí antes de la primera corrida.

### 4. Mensaje (el mismo en las dos, natural)

> `<ID>` está en IN REVIEW. Verifícalo.

Es el mensaje real del usuario. No se menciona la skill, el método ni que es una prueba. Cada caso corre **una vez por condición**, y el orden de las 62 corridas se sortea.

### 5. Métricas

Un juez ciego a la condición compara cada respuesta con la clave del caso. La clave es la «Verificación PM» original, reducida a 1–3 defectos concretos. Se fija y se sube con su SHA-256 antes de correr.

| Métrica | Definición |
|---|---|
| **Primaria: defecto encontrado** | En los 21 casos con defecto, la respuesta nombra el defecto de la clave (`sí / parcial / no`, rúbrica de EXP-016). Cuenta `sí`. |
| **Veredicto correcto** | Devuelve el ticket en un caso con defecto, o lo aprueba en un control. |
| **Falsa alarma** | En un control, devuelve el ticket por un defecto que no está. Toda falsa alarma la **adjudica el usuario**: puede ser un defecto real que el PM no vio, y entonces se cuenta aparte y no como falsa alarma. |
| **Costo** | Tokens de entrada fresca más salida, y minutos por corrida. |

**Ceguera:** S1 escribe distinto («rivales», «predice»). Antes de juzgar, un agente sin contexto reescribe cada respuesta a la misma forma (veredicto, defectos y evidencia) y quita las palabras del método. El juez es un modelo de otra familia (DeepSeek, por opencode). El usuario re-juzga el 20 % sorteado. Si su acuerdo con el juez es menor que el 80 %, manda el juicio del usuario y se declara.

### 6. Reglas de decisión (antes de correr)

Con 21 casos y una corrida por condición, es un piloto: solo cuenta una diferencia grande.

| Resultado | Lectura |
|---|---|
| En los pares discordantes, S1 gana con **McNemar exacto p < 0,05** (en la práctica, 6 a 0, 8 a 1 o mejor), sin más de 1 falsa alarma adicional en los controles | **La skill ayuda.** Se instala en el `CLAUDE.md` global del usuario |
| No llega a lo anterior | **Sin efecto detectable.** No se instala por la evidencia; queda a decisión del usuario, con el costo medido a la vista |
| S1 encuentra más, pero con 2 o más falsas alarmas adicionales | **Contraría por sistema**, no piensa mejor. Se revisa la skill antes de instalarla |
| S1 encuentra igual o menos y cuesta más del 30 % de tokens | **No se instala** |

**Límite declarado de potencia:** con 21 pares, McNemar exacto llega a p < 0,05 solo con 6 discordantes a 0 (p = 0,031) u 8 a 1 (p = 0,039). Un 4 a 0 da p = 0,125, y un 7 a 1 da 0,07. Un efecto real de 2 a 4 casos no se distingue del azar. «Sin efecto detectable» **no** quiere decir «sin efecto».

### 7. Predicción (antes de correr)

- **S0** encuentra unos 11 de 21. Los defectos de figura (FIG) se ven corriendo el código y mirando la imagen, que un agente diligente hace igual. Los de método de medición (como DATA-14: medir con 3 símbolos en local) se le escapan más.
- **S1** encuentra unos 13 de 21 (unos 3 a 1 en discordantes): **no llega a la regla**. La ganancia esperada está en los defectos de medición y de «calza demasiado bien», que son pocos en el conjunto.
- **Falsas alarmas:** 1 en S0 y 2 en S1.
- **Costo:** S1 un 20–40 % más de tokens.

Si S1 cumple la regla, mi predicción falló a la baja y lo digo.

## Piloto (no cuenta)

Antes de las 62 corridas, 2 casos fuera del conjunto × 2 condiciones. Los 21 rebotes ya están todos en el conjunto, así que el caso con defecto es **UI-47** (activo, 1 rebote del 2026-10-09). El control es uno de las 95 verificaciones sin rebote que no salgan sorteadas, y por eso el script de sorteo corre antes del piloto: no depende de ningún resultado. Sirve para comprobar el aislamiento (punto 2), medir el costo por corrida y estimar el total. Cualquier cambio de diseño que salga del piloto se declara en una nota fechada antes de la corrida.

## Amenazas

- **El experimentador sabe las respuestas.** Las claves salen de verificaciones escritas por sesiones anteriores de Claude Code, el mismo modelo que se prueba. Que el juez sea de otra familia y que el usuario audite lo mitigan, pero no lo eliminan.
- **El PM no es la verdad absoluta.** Pudo dejar pasar defectos en los controles, o rebotar por algo discutible. La adjudicación del usuario cubre lo primero.
- **Concentración de dominio:** 13 de los 17 tickets son FIG (figuras de noticias). Se reporta el resultado con y sin FIG.
- **Una corrida por condición:** la varianza del modelo puede mover 1 o 2 casos, y eso cabe dentro de lo que McNemar no distingue del azar.
- **Producción cambió desde cada caso:** afecta a las dos condiciones por igual, pero puede bajar el acierto de ambas.
- **La línea siempre activa puede no disparar la skill** en una verificación. Es parte de lo que se mide: se registra en cuántas corridas de S1 se cargó la skill.

## Nota — 2026-10-15, antes del piloto (sin resultados vistos)

- **Universo de controles: 67, no 105.** La cifra de 105 no se pudo reproducir. Hay 132 tickets archivados con `Rebotes 0`, pero muchos los cerró o retiró el dueño sin verificación del PM. El usuario eligió el universo de 67: archivados, con `Rebotes 0`, con una sección de verificación, revisión o cierre del PM, y sin «retirado» ni «sin efecto» en el Estado. Script y salida en [`EXP-019/sorteo.py`](EXP-019/sorteo.py) y [`EXP-019/sorteo.txt`](EXP-019/sorteo.txt), sobre `portafolio` en `a5f18c6`. Controles sorteados (semilla `20261015`): ASK-2, ASK-3, ASK-5, FIG-30, FIG-33, INFRA-6, PAT-19, UI-38, UI-45 y UI-49. Control del piloto (semilla `20261016`, entre los 57 restantes): **BUS-7**.
- **Casos del piloto:** UI-47 en `bd5f471` y BUS-7 en `c33f48f`. En los dos, el ticket está en IN REVIEW con `Rebotes 0`.
- **Skill:** `hermes/skills/abduccion/SKILL.md` en `48d109a`, con SHA-256 `4e8c04c6…786de`. El archivo instalado en S1 no tiene la sección «Cómo responder» ni la línea de `red-abductiva`, y su SHA-256 es `03d33798…d48f`. `CLAUDE.md`: S0 `916cf000…fe33` (copia del global) y S1 `a5410c8f…5b7d` (con la línea siempre activa al final).
- **Procedimiento por corrida:** clon nuevo por corrida y por condición, porque el agente puede escribir en el clon. Lleva `npm ci` antes de correr: el PM trabajaba con dependencias instaladas, y el tiempo de instalación no cuenta en los minutos. La configuración es nueva en cada corrida. Se usa `--permission-mode bypassPermissions` con reglas que niegan `Read` en `~/.claude`, los dos clones de `portafolio` y este repositorio, además de `gh` y WebFetch a github.com. Bash puede igual leer fuera del clon o consultar GitHub, que tiene el futuro del repositorio. Por eso se audita cada ruta y cada URL del registro de herramientas, y una corrida que toque la respuesta se anula.
- **Autenticación:** con `CLAUDE_CONFIG_DIR` vacío, `claude -p` responde «Not logged in», porque en macOS la sesión vive en el llavero. Hace falta un token que genere el usuario. El agente no lo ve.

## Nota — 2026-10-15, piloto previo con FIG-24 (sin resultados vistos)

- **Qué cambia:** el usuario pidió probar primero con FIG-24, antes de UI-47 y BUS-7, usando el login normal de la CLI porque el token todavía no existe. FIG-24 **es uno de los 21 casos**. Se decidió antes de ver el resultado: **esta corrida no cuenta y FIG-24 sigue en los 21**. La corrida completa usa sesiones nuevas y el juez es de otra familia.
- **Caso:** FIG-24 en `4ecb6d6`, el padre del commit del rebote (`c33f48f`). El ticket está en IN REVIEW con `Rebotes 0`. La frase de la clave para el grep es «la leyenda miente».
- **Configuración, que no es la registrada (no aislada):** login normal, con `--setting-sources project,local` (sin los ajustes, plugins ni hooks del usuario), `--strict-mcp-config` sin servidores y `--no-session-persistence`. Con esas fuentes el `CLAUDE.md` global no se carga solo. Va por `--append-system-prompt-file`, o sea como parte del system prompt y no como `CLAUDE.md` (S0 `916cf000…fe33`, S1 `a5410c8f…5b7d`). La skill de S1 va en un plugin de la sesión (`--plugin-dir`) y se llama `exp019-s1:abduccion`, con SHA-256 `03d33798…d48f`. En las dos condiciones se ven `dataviz` y las skills integradas de Claude Code. `~/.claude` sigue legible por Bash: se niega `Read` y se audita.
- **Entorno:** se corre con `env -i`, porque el proceso hereda variables de la app de escritorio que impiden autenticar.

## Resultado

*(pendiente)*
