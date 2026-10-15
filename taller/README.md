# Taller de skills

Aquí nacen y se prueban las skills de la familia abductiva. **Solo las estables se instalan**, y viven en [`hermes/`](../hermes/). Lo que está en el taller no se instala en ningún agente.

## La familia

Todas las skills salen del mismo [marco teórico](../docs/marco-teorico/README.md). La skill general, [`abduccion`](../hermes/skills/abduccion/SKILL.md), tiene el método. Las demás **la extienden**: no lo repiten, agregan lo propio de un dominio o de una tarea.

| Skill | Qué agrega | Estado | Dónde |
|---|---|---|---|
| `abduccion` | El método general: lo sorprendente, rivales de familias distintas, comprobar antes de decidir | **Estable** (en prueba en [EXP-018](../docs/bitacora/EXP-018-fuera-de-la-caja-con-datos.md)) | [`hermes/skills/abduccion/`](../hermes/skills/abduccion/SKILL.md) |
| `aprender-del-campo` | Dejar notas de campo y predicciones, y proponer skills | Borrador | [`taller/skills/aprender-del-campo/`](skills/aprender-del-campo/SKILL.md) |
| `abduccion-mercados` | Acciones y empresas: qué descuenta el precio, precios objetivo por supuestos, caída estructural o rebote | Borrador | [`taller/skills/abduccion-mercados/`](skills/abduccion-mercados/SKILL.md) |

## Ciclo de vida

```text
propuesta ──► borrador ──► en prueba ──► estable ──► retirada
(agente)     (taller/)    (experimento   (hermes/)   (docs/historico/)
                           registrado)
```

| Estado | Qué hace falta para llegar | Quién decide |
|---|---|---|
| **Propuesta** | Un archivo en `taller/propuestas/` con la plantilla de abajo | Cualquier agente |
| **Borrador** | La skill escrita en `taller/skills/<nombre>/SKILL.md` | El usuario acepta la propuesta |
| **En prueba** | Un experimento registrado en la [bitácora](../docs/bitacora/README.md) **antes** de correrlo, con lo que contaría como fracaso. Puede ser prospectivo: predicciones en [`campo/`](../campo/README.md) que se resuelven con el tiempo | El usuario |
| **Estable** | Pasó su prueba. Se copia a `hermes/skills/` y se instala | El usuario |
| **Retirada** | No pasó, o la reemplazó otra. Se mueve a `docs/historico/` con la razón | El usuario |

## Reglas para una skill de la familia

1. **Extiende, no repite.** Empieza diciendo que aplica la skill `abduccion` y agrega solo lo propio.
2. **Se apoya en el marco.** Cada regla del dominio se puede rastrear a un principio (P1 a P6), a una familia de rivales o a un disparador. Si necesita algo que el marco no tiene, eso es una propuesta al marco, no a la skill.
3. **Nace de la evidencia.** Enlaza las notas de campo, los patrones o los experimentos que la justifican. Una skill sin uso real que la pida es especulación.
4. **Una página como máximo.** Lo que no cabe va al marco o a una referencia aparte, dentro de la carpeta de la skill.
5. **No se ajusta mirando los casos de prueba** de su propio experimento.
6. **Declara su límite**: qué no puede hacer (por ejemplo, en un mercado, disciplina sí, ventaja no garantizada).

## Plantilla de propuesta

Archivo `taller/propuestas/AAAA-MM-DD-<nombre>.md`:

```markdown
# Propuesta: <nombre-de-la-skill>

- **Propuesta por:** <agente>, <fecha>
- **Dominio o tarea:** <cuándo se usaría, en una línea>

## Por qué hace falta
<qué problema se repitió y la skill general no cubrió. Enlaces a notas de campo o patrones: al menos 3>

## Qué agregaría
<familias de rivales del dominio, comprobaciones típicas, formato de respuesta. Solo lo que no está en `abduccion`>

## De qué principios sale
<P1 a P6, familias o disparadores del marco que aplica>

## Cómo se probaría
<qué conducta del agente cambiaría si funciona, y qué resultado contaría como fracaso>

## Riesgos
<cómo podría volver rebuscado al agente o sobreajustarse>
```
