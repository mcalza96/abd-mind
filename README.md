# abd-mind

Una familia de skills de pensamiento abductivo para agentes de IA, con la teoría de la que salen y el registro de lo que se aprende al usarlas. **Objetivo:** que un agente no se quede con la respuesta promedio, sino que busque la explicación no obvia, la compruebe y la distinga de la rebuscada ([tesis](docs/marco-teorico/tesis.md)).

No promete conocimiento fuera de la frontera. Promete **disciplina**: elegir bien qué explicar, comprobar rivales con datos, apostar antes de saber y llevar la cuenta de si acierta.

## Cómo está organizado

| Carpeta | Qué hay | Quién escribe |
|---|---|---|
| [`hermes/`](hermes/) | Lo que se instala en el agente: las skills **estables** y las [líneas siempre activas](hermes/instrucciones-permanentes.md) | El usuario |
| [`taller/`](taller/README.md) | Skills en propuesta, borrador o prueba, y las reglas de la familia | Agentes proponen; el usuario decide |
| [`campo/`](campo/README.md) | Notas de campo, predicciones y patrones: lo que los agentes aprenden al trabajar | Agentes |
| [`docs/marco-teorico/`](docs/marco-teorico/README.md) | Tesis, generación, principios y formalización. De aquí salen todas las skills | Solo con pedido del usuario |
| [`docs/bitacora/`](docs/bitacora/README.md) | Experimentos registrados antes de correrlos, y lecciones | Con pedido del usuario |
| [`docs/experimentos-mentales/`](docs/experimentos-mentales/README.md) | Las historias y axiomas de los que salen los principios | Con pedido del usuario |
| [`docs/historico/`](docs/historico/README.md) | El marco anterior, el motor y sus ADRs, skills retiradas | Nadie: es archivo |
| [`datasets/`](datasets/abd-bench/README.md) | Los conjuntos usados en los experimentos | Con pedido del usuario |

## El ciclo del conocimiento

```text
        marco teórico ──────────► skills (taller → hermes)
             ▲                          │
             │  solo con pedido         │  uso real
             │  del usuario             ▼
   bitácora (experimento) ◄── patrones ◄── notas de campo y predicciones
```

1. **Las skills salen del marco.** `abduccion` tiene el método general. Las demás lo extienden a un dominio, como [`abduccion-mercados`](taller/skills/abduccion-mercados/SKILL.md), o a una tarea, como [`red-abductiva`](taller/skills/red-abductiva/SKILL.md).
2. **El uso deja rastro.** Al terminar un análisis, el agente escribe una nota de campo y registra predicciones fechadas.
3. **Lo que se repite se vuelve patrón.** Con al menos 3 notas independientes, un agente lo propone y el usuario lo acepta o no.
4. **Un patrón justifica una skill o un experimento**, nunca un cambio directo a la teoría. El marco cambia solo cuando un experimento o una historia lo exige y el usuario lo pide.
5. **Las predicciones resueltas dicen si sirve.** La revisión periódica compara el acierto de los agentes con la tasa base y con el consenso.

## Contribuir: los agentes abren PR, el usuario revisa

Los agentes que usan estas skills (Hermes y otros) son **contribuidores** del repositorio. Todo aporte entra por un **pull request** que el usuario revisa y fusiona, o devuelve. Nadie escribe directo en `main`.

- **Qué puede proponer un agente por su cuenta:** notas de campo, predicciones y sus resoluciones, patrones `candidato` y propuestas de skills.
- **Qué solo propone si el usuario se lo pidió:** cambios a `hermes/`, al marco teórico, a la bitácora, a los experimentos mentales y a los datos. Un PR no reemplaza ese pedido.
- **Cómo:** una rama por aporte, con nombre `agente/<nombre-del-agente>/<tema>`, y un PR con la [plantilla](.github/pull_request_template.md): qué aporta, la evidencia, qué no se tocó y qué tiene que decidir el usuario. Un PR, un tema.
- **Si el agente no tiene acceso de escritura**, le envía al usuario los archivos listos, y el usuario abre el PR.
- **La revisión es la curaduría.** El usuario fusiona, pide cambios o cierra con una razón. Un PR cerrado no se borra: la razón también enseña.

## Qué se instala hoy

- [`hermes/skills/abduccion/SKILL.md`](hermes/skills/abduccion/SKILL.md): el método, en una página.
- [`hermes/instrucciones-permanentes.md`](hermes/instrucciones-permanentes.md): siete líneas para las instrucciones siempre activas de Hermes. Son las que buscan volverlo un hábito.

No tienen una prueba controlada: [EXP-018](docs/bitacora/EXP-018-fuera-de-la-caja-con-datos.md) se abandonó sin correr. Su acierto se mide en uso real, con las predicciones de [`campo/`](campo/README.md). El primer candidato a instalar es [`red-abductiva`](taller/skills/red-abductiva/SKILL.md): les da a los agentes el objetivo, los principios y las reglas de la red, y pone en marcha el ciclo.

**El motor abductivo** (verificación, puntuación y servidor MCP) se construyó y se midió, pero no agregaba nada que un agente con sus herramientas no pudiera hacer, y se quitó ([ADR-0017](docs/historico/arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)). Último commit con el motor: `44b51f694420cd3df004428e59c85fb000008c46`.
