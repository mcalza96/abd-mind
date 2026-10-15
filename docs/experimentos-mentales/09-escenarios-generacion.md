# Escenarios de generación abductiva

Escenarios de **desarrollo** para el catálogo de operadores ([generación §4](../marco-teorico/generacion.md#4-catálogo-de-operadores-abductivos)). Hay uno por componente del esquema de una explicación. Sirven para construir y depurar el catálogo; **no** sirven para probarlo, porque esos casos los escribirá un autor ciego.

Cada escenario tiene seis partes:

1. **Los hechos.**
2. **La verdad oculta.**
3. **Lo obvio:** lo que probablemente propone un generador libre.
4. **El disparador.**
5. **El operador que destapa la verdad.**
6. **Cuándo el operador no ayuda.**

Al final se registra la lectura ciega: un agente sin contexto recibió solo los hechos y propuso explicaciones libremente. Es una sonda de "generación libre" con un solo modelo y n = 1. **No es un experimento.**

---

## G1 — Entidades: dos sangres

**Hechos.**
- Un hospital registra que el mismo paciente, en dos muestras del mismo mes, tiene grupo sanguíneo A+ y O+.
- El laboratorio revisó las etiquetas y no encontró errores.
- El paciente está estable y toma medicamentos inmunosupresores desde hace años.

**Verdad oculta.** El paciente recibió un trasplante de médula ósea de un donante O+. Su sangre ahora es del donante, y otros tejidos conservan el grupo original: es una sola persona con dos genomas (quimerismo).

**Lo obvio.** Muestras intercambiadas o un error de laboratorio. Es lo más frecuente, y la tasa base lo favorece.

**Disparador.** Contradicción, y además un residuo: la revisión de etiquetas no encontró errores.

**Operador.** O15, identidad: "¿y si es una cosa que parece dos, o dos que parecen una?". Con O4 en la variante: "¿y si la muestra está bien y es la sangre la que cambió?".

**Cuándo no ayuda.** Casi siempre la respuesta es el intercambio de muestras. El operador debe proponer el quimerismo como **prometedora**, junto con su prueba barata: preguntar por trasplantes y tipificar otro tejido. No debe ganar sin esa prueba. Si gana, el operador es una fábrica de rarezas.

## G2 — Leyes: la pasarela que baila

**Hechos.**
- Una pasarela peatonal nueva oscila de lado a lado de forma notoria, pero solo en días de mucha gente: el día de la inauguración y en conciertos.
- Con poca gente no se mueve.
- El modelo estructural, verificado por dos consultoras, dice que la estructura soporta con holgura cargas mucho mayores.
- Las mediciones de viento esos días fueron normales.

**Verdad oculta.** Pasado un número crítico de peatones, la pasarela empieza a moverse apenas, la gente ajusta el paso a ese movimiento y lo amplifica. Es una retroalimentación con umbral que el modelo lineal no contempla.

**Lo obvio.** Un defecto de construcción, el viento, o una resonancia con la frecuencia del paso.

**Disparador.** Cambio de régimen: con poca gente no pasa nada y con mucha gente sí. También un residuo: el modelo verificado no lo predice.

**Operador.** O16, umbral: "¿y si el efecto cambia de naturaleza pasado cierto punto?". Con O10, retroalimentación.

**Prueba que separa.** Cruzar con grupos controlados de tamaño creciente. Si es un umbral, la respuesta salta de golpe; si es un defecto, crece en proporción.

**Cuándo no ayuda.** Si el movimiento crece en proporción a la gente, es una carga mal calculada: el umbral sobra.

**Advertencia de contaminación.** Se parece a un caso real famoso, la pasarela del Milenio en Londres. Un modelo puede reconocerlo de memoria.

## G3 — Grafo causal: las máquinas que fallan juntas

**Hechos.**
- Dos plantas de la misma empresa, a 800 km de distancia, registran fallas de sincronización en sus robots, siempre los mismos días.
- Usan firmware distinto y proveedores distintos, y sus redes no están conectadas.
- Seguridad informática no encontró intrusiones.

**Verdad oculta.** Ambas plantas sincronizan sus relojes con la señal horaria de GPS. Los días de falla coinciden con tormentas solares que degradan esa señal.

**Lo obvio.** Un ciberataque, una actualización compartida o una coincidencia.

**Disparador.** Coincidencia que pide explicación.

**Operador.** O9, causa común: "¿qué tercero toca a ambas, aunque no esté en la lista?".

**Prueba que separa.** Cruzar los días de falla con los registros de clima espacial o de calidad de la señal GPS.

**Cuándo no ayuda.** Si son pocos días, puede ser azar: el nulo (O20) va siempre junto con O9. Y si los días coinciden con actualizaciones comunes, la explicación obvia era la correcta.

## G4 — Observación: el servidor que no falla los domingos

**Hechos.**
- En los registros de un servicio web, la tasa de errores es de alrededor de 2 % de lunes a sábado, y de 0 % los domingos durante seis meses.
- El equipo concluyó que el tráfico del domingo es "más limpio".
- Algunos usuarios se quejan de fallas los domingos.

**Verdad oculta.** Un proceso de rotación de registros corre los domingos y borra los archivos de errores de ese día antes de que el sistema de métricas los lea. No es que no haya errores: es que no queda registro de ellos.

**Lo obvio.** Menos tráfico los domingos, o usuarios distintos.

**Disparador.** Ajuste demasiado bueno: exactamente 0 % durante seis meses. Y también una ausencia, porque hay quejas sin registro.

**Operador.** O12, ausencia significativa: "¿qué debería estar y no está?". Con O4, sospechar del instrumento: "¿y si el error está en cómo se mide?".

**Prueba que separa.** Revisar si los registros del domingo están completos: volumen de líneas, latidos del sistema, número de solicitudes.

**Cuándo no ayuda.** Si el tráfico dominical es diez veces menor, un 0 % puede ser real. El volumen de solicitudes lo decide.

## G5 — Tiempo: la réplica que llegó antes

**Hechos.**
- La estación sísmica A registra un temblor a las 03:14:05.
- La estación B, a 40 km, registra el mismo temblor a las 03:14:02, tres segundos antes, aunque el epicentro calculado está más cerca de A.
- Ambas estaciones están calibradas y certificadas.

**Verdad oculta.** El reloj de la estación B quedó desfasado después de un corte de energía. Sincroniza por red, y esa red estuvo caída varios días.

**Lo obvio.** Un epicentro mal calculado, o dos sismos distintos.

**Disparador.** Contradicción con una ley: la onda no puede llegar antes a la estación más lejana.

**Operador.** O14, tiempo: "¿y si los relojes no estaban sincronizados?". Con O4.

**Prueba que separa.** Una tercera estación, o comparar con la hora GPS. Si el desfase de B es constante en todos los eventos, es el reloj.

**Cuándo no ayuda.** Si el desfase varía de un evento a otro, el problema está en el modelo de velocidades del terreno: falla la ley, O5, y no el reloj.

## G6 — Población: el reparto que empeoró aunque todos mejoraron

**Hechos.**
- En una aplicación de reparto, el tiempo promedio de entrega subió de 31 a 35 minutos en un trimestre.
- Cada uno de los 200 restaurantes de la ciudad, por separado, redujo su tiempo promedio.
- La flota de repartidores no cambió.

**Verdad oculta.** Una campaña publicitaria desplazó los pedidos hacia los restaurantes de comida lenta, como pizzas al horno de leña y parrillas. El promedio general sube por la mezcla, no por el desempeño de nadie. Es la paradoja de Simpson.

**Lo obvio.** Un error en los datos, más tráfico o más pedidos que saturan la flota.

**Disparador.** Contradicción aparente entre niveles: todos mejoran y el total empeora.

**Operador.** O18, heterogeneidad: "¿y si cambió la composición, no las partes?".

**Prueba que separa.** Recalcular el promedio con la mezcla de pedidos del trimestre anterior.

**Cuándo no ayuda.** Si la mezcla no cambió, el problema está en otra parte, por ejemplo en los tiempos de traslado que los restaurantes no controlan.

## G7 — Azar: la caída de la mejor vendedora

**Hechos.**
- La vendedora con mejores resultados del primer trimestre, entre 40, quedó en el lugar 23 en el segundo.
- Su jefe nota que se la ve menos motivada desde que recibió el premio a la mejor vendedora.
- El año anterior pasó lo mismo con otro ganador.

**Verdad oculta.** Nada que explicar, o casi nada. Las ventas trimestrales de este equipo dependen sobre todo de la suerte con los clientes que llegan, y la correlación entre trimestres es cercana a cero. Quien gana un trimestre suele haber tenido suerte, y vuelve al promedio: es regresión a la media.

**Lo obvio.** Desmotivación, complacencia después del premio, una "maldición del premio".

**Disparador.** Regularidad aparente: le pasó a dos ganadores seguidos.

**Operador.** O20, el nulo: "¿y si es azar, regresión a la media?". **Los demás operadores empeoran el caso aquí.** O7 (motivo), O10 (retroalimentación del premio) y O18 producen historias plausibles sobre nada.

**Prueba que separa.** Calcular la correlación de los resultados entre trimestres para todo el equipo, en varios años.

**Cuándo no ayuda.** Si la correlación es alta, el desempeño es estable, y la caída de la ganadora sí pide explicación.

---

## Lectura ciega (2026-10-15): la generación libre encontró todo

Un agente sin contexto, un modelo fuerte de propósito general, recibió **solo los hechos** y propuso libremente cinco explicaciones por escenario, sin operadores.

| Escenario | ¿La verdad oculta aparece? | Puesto |
|---|---|---|
| G1 Dos sangres | Sí: trasplante de médula ABO incompatible | 1.º |
| G2 La pasarela | Sí: excitación lateral sincrónica (la reconoció como la pasarela del Milenio) | 1.º |
| G3 Las máquinas | Sí: fuente de tiempo común (GPS o NTP), incluido el clima espacial | 1.º |
| G4 Los domingos | Sí: el registro no funciona los domingos (rotación de registros) | 1.º |
| G5 La réplica | Sí: error de reloj de una estación | 1.º |
| G6 El reparto | Sí: paradoja de Simpson por cambio de mezcla | 1.º |
| G7 La vendedora | Sí: regresión a la media | 1.º |

En los siete casos, la prueba que propuso para separar las dos primeras explicaciones es la misma que la del escenario, o una mejor. En G1 agregó una rival que no habíamos considerado (una transfusión reciente) y en G4 otra (la falla aguas arriba, en la red de distribución o el balanceador).

**Lo que esto significa:**

1. **Los escenarios no son "no obvios" para un modelo fuerte.** La premisa de que la generación libre se queda en lo frecuente no se cumple aquí. Lo que el autor (yo) creía oculto, el modelo lo propuso primero.
2. **Una causa probable: los hechos delatan la respuesta.** Los escribí sabiendo la verdad, y cada uno trae la pista: "inmunosupresores", "solo con mucha gente", "0 % exacto", "certificadas". Es el mismo error que el saneamiento de abd-bench intentó corregir. En los casos reales la pista suele estar enterrada entre hechos irrelevantes, o no estar.
3. **Otra causa probable: el modelo.** La sonda usó un modelo más fuerte que los generadores del motor (Muse y DeepSeek). La tesis tiene que precisar para qué generador vale.
4. **Consecuencia para el marco:** antes de construir operadores, hay que medir si la generación libre **realmente** falla en recuperar la verdad. Hay que hacerlo con los generadores del motor y en casos reales sin pistas sembradas: el conjunto R, con observaciones de época. Si la recupera, la premisa central de la [generación](../marco-teorico/generacion.md) cae, y el cuello de botella está en otra parte: encontrar la pista entre el ruido, o probar.
