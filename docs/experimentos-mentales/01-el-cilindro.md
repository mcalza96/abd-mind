# Historia 1 — El cilindro

Versión narrada del experimento canónico [05 §5.1](../marco-teorico/05-experimentos-canonicos.md#51-cilindro-latente). Se incluye para que la serie parta del mismo punto.

## Escena

En la sala hay un **cilindro** de eje vertical (la verdad oculta).

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | un rectángulo |
| Tomás | Techo | un círculo |

Olga y Tomás discuten: "es un rectángulo", "no, es un círculo". Ninguno miente y ninguno se equivoca.

## La pregunta

¿Qué hay en la sala?

## Lo que haría alguien que promedia

Un juez que trata los reportes como opiniones a conciliar busca un punto medio: "un óvalo", "un rectángulo de esquinas redondeadas". Es una quimera: no hay sólido cuya sombra frontal sea un óvalo y cuya sombra cenital sea un círculo y que además coincida con lo que vio Olga.

## El motor, paso a paso

1. `crear_caso` en el dominio con proyección exacta; `agregar_observacion` para Olga y para Tomás, con su ventana como marco.
2. `proponer_hipotesis`: esfera, cubo, cilindro.
3. `evaluar`: el motor **calcula** la sombra de cada sólido por cada ventana. La esfera explica a Tomás, no a Olga; el cubo a ninguno; el cilindro a los dos.
4. `mejor_explicacion`: cilindro, por consiliencia (C = 2).

## Dónde se rompe

En esta sala, en ninguna parte, y por eso es engañosa:

- **La sombra se calcula.** Nadie tiene que *juzgar* si un cilindro produce un rectángulo: es geometría. En un dominio abierto ese cálculo lo reemplaza el juicio de un LLM (L2), y ahí empezaron los problemas de EXP-008 a EXP-012.
- **La línea base también acierta** (EXP-001). Para un LLM, "círculo arriba y rectángulo al frente" es un cilindro de libro. La historia muestra el principio, pero no muestra que el motor aporte algo.
- **El cilindro llegó porque alguien lo propuso.** Si nadie lo propone, el motor no lo inventa (la expansión de 5.2 es otra historia).

## Principio

- **A1 — Mediación.** Nadie ve el objeto, solo proyecciones a través de un instrumento.
- **A2 — Consiliencia, no promedio.** El desacuerdo entre proyecciones es información sobre el objeto. Una explicación debe **producir** cada proyección, no conciliarlas.
