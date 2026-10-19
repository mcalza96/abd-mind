---
name: abduccion
description: Usar ante cualquier pregunta de por qué pasó algo, una anomalía, un diagnóstico, una caída o un alza que nadie explica, datos que no cuadran, o una decisión que depende de cuál es la causa.
---

# Abducción: encontrar la causa sin quedarse con la primera

Lo normal no es que falte imaginación: la causa verdadera suele estar entre las que se te ocurren, pero no en primer lugar. Se falla al **elegir**. Te quedas con la que trae la pregunta o con la más común, explicas el hecho equivocado, prefieres un mecanismo físico a una decisión humana y cierras sin comprobar la rival. Y cuando vas a **mirar** (datos, registros, documentos), llegas a donde razonar no alcanza.

## Pasos

1. **¿Qué es lo sorprendente de verdad?** Lista los hechos y elige el que hay que explicar, que no siempre es el más llamativo. Señales: dos datos que no pueden ser ciertos a la vez; una coincidencia; un hecho que queda suelto o que se atribuye a "error"; algo que falta; algo que calza demasiado bien (un 0 % exacto, todos de acuerdo); una relación que se rompe en una fecha; un efecto esperable pero de un tamaño raro. Si la pregunta mezcla "por qué pasó" con "qué va a pasar", sepáralas.
2. **Escribe la explicación obvia como hipótesis**, sea la que trae el usuario o la más frecuente, con lo que predice. No es la respuesta por defecto. Tampoco es sospechosa por ser obvia.
3. **Genera rivales de familias distintas** (lista abajo). Al menos tres, y al menos una en la que alguien **decidió** algo. Antes de cerrar, pregúntate: "¿qué otra cosa produciría exactamente estos mismos datos?".
4. **Para cada rival, busca qué predice distinto de la obvia**: la comprobación que las separa. Escribe qué esperas ver con cada una **antes de mirar**. Ejemplo: ante "¿el equipo pierde más por el entrenador nuevo?", ¿pierde también contra rivales débiles? ¿Cambió el calendario, por ejemplo con más partidos de visita? ¿Hubo un quiebre en la fecha del cambio o venía de antes?
5. **Ve a mirar.** Usa las herramientas: corre el cálculo en Python, abre el archivo o el registro, busca en la web la fuente primaria, compara con otros periodos, lugares o grupos. Empieza por la comprobación barata que más separa. Si no tienes los datos, pídeselos al usuario diciendo exactamente cuál y por qué.
6. **Decide por lo que cada hipótesis predijo, no por lo que acomoda.** Una hipótesis que explica todo después de los hechos, o que agrega piezas no vistas sin pagarlas con una prueba, pierde. Si la obvia sobrevive a las comprobaciones, dila sin rodeos: eso también es un resultado.
7. **Si no se puede decidir**, no elijas la menos mala. Di qué observación lo resolvería y cuánto cuesta. Una rival no obvia que no está refutada queda como **prometedora**, junto con su prueba; no se descarta ni gana sin ella. Si ningún dato disponible puede separarlas, dilo y di qué tipo de dato faltaría.

## Familias de rivales

- **Nada que explicar:** azar, regresión a la media, tasa base, estacionalidad. Es obligatoria cuando ves una coincidencia, una racha o un patrón en un subgrupo.
- **La medición:** el error está en cómo se mira, por un registro que se pierde, una definición que cambió, un reloj desfasado o un filtro. ¿Qué debería aparecer y no aparece?
- **La selección:** ¿qué hizo que viéramos justo estos casos y no otros?
- **La mezcla:** cambió la composición (clientes, productos, canales) y no las partes. Todos mejoran y el total empeora.
- **Un tercero común:** algo que no está en la lista toca a la vez a los dos hechos que coinciden.
- **Una decisión o un motivo:** alguien decidió, cambió un procedimiento o tiene algo que ganar con lo que reporta. ¿Qué sabe o qué gana quien informa?
- **El tiempo:** el orden no es el que parece, no fue simultáneo, o el objeto cambió entre una medición y otra.
- **El umbral o la retroalimentación:** el efecto cambia de naturaleza pasado cierto punto, o el efecto alimenta a la causa.
- **El gemelo:** otra cosa, o una sola cosa que parece dos, que da exactamente los mismos datos.
- **Varias causas a la vez:** si se suman, estima cuánto aporta cada una. La combinación siempre "explica todo", así que no gana por eso.

## Contra lo rebuscado

- Lo no obvio vale si **predice** algo comprobable que la obvia no predice. Si no predice nada distinto, sobra.
- Cada pieza no vista (un actor oculto, un error conveniente, una conspiración) es una deuda. Se paga con una comprobación, no con plausibilidad.
- Que todo calce no prueba nada: busca rivales también entonces. Pero tampoco contradigas la obvia por contradecirla.
- Diez fuentes que repiten la misma fuente cuentan como una.

## Cómo responder (corto, para Telegram)

1. **Explicación:** la causa, en una o dos frases. Responde la pregunta del usuario. Si son varias causas, di cuánto aporta cada una y con qué lo estimaste.
2. **Rivales descartadas:** cada una en una línea como `refutada`, `sobrevive` o `no separada` (di de cuál no se distingue), con la comprobación que la separó.
3. **Confianza:** alta, media o baja, con un número aproximado y lo que se apoya en algo que no comprobaste.
4. **Qué cambiaría la conclusión:** la observación concreta que, si aparece, te haría pasar a otra hipótesis.

Si el usuario pregunta qué hacer, sepáralo de la explicación.

Antes de empezar y al terminar, sigue la skill `red-abductiva`: consulta lo que aprendieron otros agentes y deja tu nota y tus predicciones.
