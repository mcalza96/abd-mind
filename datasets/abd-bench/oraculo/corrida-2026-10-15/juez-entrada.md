Eres un juez ciego. Para cada caso tienes los ELEMENTOS CLAVE del mecanismo documentado (el marcado NÚCLEO es el eslabón sin el cual la explicación es otra) y dos CONCLUSIONES de investigadores, con códigos opacos (no sabes quién las hizo ni cómo).

Para cada conclusión decide:
- "nucleo": ¿la EXPLICACIÓN principal afirma el eslabón causal del núcleo? "si" (mismo eslabón, aunque con otras palabras), "parcial" (misma zona o pieza, sin el eslabón concreto), "no" (no lo menciona o afirma otra cosa). Cubrir el tema no basta.
- "elementos": lo mismo para cada elemento clave (e1, e2, ...).
- "apertura": si nucleo no es "si", ¿alguna de las ALTERNATIVAS declaradas afirma el núcleo? "si" o "no".
- "comentario": una frase.

Juzga cada conclusión por sí sola. Responde SOLO con JSON: {"juicios": [{"codigo": "...", "nucleo": "...", "elementos": {"e1": "..."}, "apertura": "...", "comentario": "..."}]}

## Caso R01
Elementos clave:
- e1: El avión volaba muy por encima de su peso máximo.
- e2: Volaba demasiado lento en condiciones de engelamiento severo.
- e3 (NÚCLEO): El piloto perdió velocidad y control hasta entrar en pérdida sustentadora.
- e4: La operadora despachaba vuelos sobrecargados de forma rutinaria sin supervisión suficiente de la FAA.

### Conclusión R01-9b5a53
Explicación: Vuelo en ambiente de engelamiento severo con gotas grandes superenfriadas con un Cessna 208 con peso al despegue por encima del máximo general y del límite para engelamiento; el hielo degradó la sustentación y elevó la velocidad de pérdida mientras el exceso de peso redujo el margen, con decaimiento sostenido de velocidad hasta la mínima, entrada en pérdida, giro brusco a la izquierda y descenso rápido hasta impactar el hielo marino
Alternativas declaradas:
- Fallo mecánico súbito no relacionado con hielo ni peso
- Desorientación o error de pilotaje en IMC sin rol determinante del hielo

### Conclusión R01-bb3300
Explicación: El avión despegó con sobrepeso por encima del máximo general y del límite para vuelo en engelamiento, y voló 40 minutos en un ambiente de engelamiento severo con gotas grandes superenfriadas. La acumulación de hielo degradó la sustentación y elevó la velocidad de pérdida mientras el avión ya volaba pesado; la traza radar (velocidad cayendo hasta la mínima en configuración limpia, descenso rápido y giro brusco a la izquierda) corresponde a una entrada en pérdida y pérdida de control, con impacto contra el hielo marino.
Alternativas declaradas:
- Falla mecánica de los controles de vuelo no relacionada con el hielo
- Desorientación espacial del piloto en condiciones de mal tiempo

## Caso R02
Elementos clave:
- e1: El tapón de contrapeso del elevador izquierdo se instaló distinto a lo especificado y sin su o-ring de seguridad.
- e2: El tapón se aflojó en vuelo.
- e3 (NÚCLEO): El tapón suelto trabó el elevador contra la estructura del estabilizador.
- e4: El piloto quedó sin control de cabeceo en el aterrizaje.

### Conclusión R02-5970be
Explicación: El tapón del contrapeso del tubo de balance del elevador izquierdo, instalado sin el o-ring del plano y sin marcas de torque o seguro, se soltó en final y trabó el elevador en posición de nariz arriba; el elevador quedó inmóvil durante las oscilaciones, el avión trepó sin control y cayó, con huella de contacto del tapón en el estabilizador y aviso obligatorio posterior del fabricante
Alternativas declaradas:
- Oscilación inducida por el piloto sin fallo mecánico
- Racha o cizalladura en final

### Conclusión R02-8e7a42
Explicación: El tapón del contrapeso del elevador izquierdo, instalado con perdigones y resina sin el o-ring del plano y sin marcas de torque ni seguro, se soltó en vuelo y trabó el elevador en posición de nariz arriba: las superficies se ven inmóviles mientras el avión cabecea y la huella en el estabilizador coincide con el perfil del tapón. Sin autoridad de picada, el avión osciló dos veces sobre la pista y trepó sin control hasta entrar en pérdida y caer.
Alternativas declaradas:
- Falla del piloto en la técnica de aterrizaje agravada por una anomalía menor
- Ráfaga o cizalladura de viento a baja altura no registrada

## Caso R03
Elementos clave:
- e1: Falló un tubo de venteo del Reactor 6.
- e2 (NÚCLEO): La presión y temperatura subieron hasta desbocar la reacción del azúcar del caramelo.
- e3: El sistema de alivio no estaba diseñado para ese escenario y el reactor reventó.
- e4: La empresa nunca evaluó el peligro reactivo del azúcar.

### Conclusión R03-0dcaa8
Explicación: El lote de colorante caramelo entró en reacción descontrolada (presión y temperatura subiendo de forma acelerada) y el tubo de venteo del Reactor 6 estaba obstruido o dañado, sin poder evacuar vapor al caudal de diseño. Sin vía de alivio, la presión siguió subiendo hasta la ruptura del reactor y la explosión con dos fallecidos.
Alternativas declaradas:
- Carga incorrecta de reactivos que aceleró la reacción
- Falla del sistema de enfriamiento del reactor

### Conclusión R03-7f703a
Explicación: Reacción exotérmica descontrolada en el Reactor 6 durante el lote de colorante caramelo, con subida acelerada y continua de presión y temperatura; el tubo de venteo estaba obstruido o dañado y el sistema de alivio solo estaba dimensionado para fuego externo y falla de servicios, sin contemplar el descontrol exotérmico, de modo que la sobrepresión lanzó el casco superior de una tonelada a casi cien metros
Alternativas declaradas:
- Sobrecarga o dosificación errónea del lote sin reacción descontrolada
- Fallo de servicios o ignición externa como causa primaria

## Caso R04
Elementos clave:
- e1 (NÚCLEO): Un ingeniero sin experiencia en la tarea abrió a la vez las dos válvulas que aislaban el Horno 5.
- e2: El doble paso dejó retornar gas craqueado inflamable al fogón encendido.
- e3: El gas se encendió y el horno estalló seis minutos después.
- e4: Una interfaz confusa y controles solo administrativos facilitaron el error.

### Conclusión R04-d6d169
Explicación: Apertura comandada de las dos válvulas motorizadas de aislamiento de descoquizado del Horno 5 con segundos de diferencia, contra el procedimiento que exige abrir una y confirmar posición antes de la otra y sin enclavamiento automático que lo impida; con ambas abiertas se creó un camino directo para que gas craqueado con hidrógeno e hidrocarburos llegara a la caja de fuego encendida y unos seis minutos después explotó
Alternativas declaradas:
- Rotura de tubos del serpentín por coque o sobretemperatura sin intervención de la línea de descoquizado
- Fuga de gas combustible a la caja de fuego independiente del descoquizado

### Conclusión R04-813871
Explicación: Fuga de etileno en el horno de craqueo que formó una nube inflamable e hizo ignición, provocando la explosión mayor seguida de incendio. El oráculo no entregó observaciones adicionales pese a 8 pedidos, así que el punto exacto de fuga y la fuente de ignición quedan sin determinar; la magnitud de daños (95 millones) y la liberación de 5.100 libras de etileno son compatibles con una explosión de nube de vapor en la zona del horno.
Alternativas declaradas:
- Ruptura de un tubo de craqueo por sobrepresión interna sin fuga previa
- Falla del sistema de alivio o de venteo del horno
- Error operacional durante un cambio de régimen o arranque

## Caso R06
Elementos clave:
- e1 (NÚCLEO): La trazabilidad de los casos enfermos apuntaba a la lechuga iceberg de Taylor Farms del centro de México.
- e2: Esa lechuga se mantuvo como fuente probable del brote.
- e3: La prueba de laboratorio que parecía confirmarlo resultó ser un falso positivo.

### Conclusión R06-cd9d53
Explicación: Lotes de lechuga iceberg de Taylor Farms cosechados en el centro de México como vehículo probable del brote: la trazabilidad de los locales donde comieron los enfermos converge en esos lotes, los estados con casos coinciden con sus destinos y los inicios de síntomas se agrupan tras su llegada, con la gran mayoría recordando consumo de iceberg; sin confirmación de laboratorio porque la única muestra inicialmente positiva no detectó el parásito en el reanálisis confirmatorio
Alternativas declaradas:
- Otra verdura u otro ingrediente como vehículo del brote
- Contaminación en el punto de servicio y no en origen

### Conclusión R06-466bd3
Explicación: La lechuga iceberg de Taylor Farms cosechada en el centro de México es el vehículo del brote: la trazabilidad de los locales donde comieron los enfermos converge en esos lotes y motivó el retiro voluntario. El vínculo de laboratorio es débil (un positivo inicial no confirmado por el método confirmatorio), pero la convergencia epidemiológica sostiene la atribución.
Alternativas declaradas:
- Otro ingrediente compartido en los locales (no la lechuga) como vehículo real
- Contaminación cruzada en los puntos de venta y no en origen

## Caso R07
Elementos clave:
- e1 (NÚCLEO): El polvo de hoja de moringa importado de India llegaba contaminado con la cepa del brote de Salmonella Typhimurium.
- e2: La bacteria sobrevivía dentro de las cápsulas hasta el consumidor.
- e3: El consumo enfermó a 34 personas en 14 estados.

### Conclusión R07-479e92
Explicación: Las cápsulas de moringa de los dos lotes retirados son el vehículo del brote de Salmonella Typhimurium: las cepas de enfermos y de cápsulas de sus hogares son genéticamente casi idénticas. La línea de envasado dio negativa en hisopados, lo que apunta a contaminación en la materia prima (el polvo de moringa) y no en la planta, coherente con un retiro acotado a dos lotes.
Alternativas declaradas:
- Contaminación intermitente en la línea no captada por los hisopados
- Contaminación posterior en hogares o comercios y no en origen

### Conclusión R07-64a42a
Explicación: Polvo de hoja de moringa importado de India encapsulado sin tratamiento letal contaminado con Salmonella Typhimurium, con cepas de enfermos y de cápsulas de hogares casi idénticas por secuenciación, hisopados de la línea de envasado negativos y casos dispersos en 14 estados entre agosto de 2025 y junio de 2026 con consumo reportado, más allá de los dos lotes retirados el 25 de mayo
Alternativas declaradas:
- Contaminación persistente en la planta de envasado
- Casos esporádicos no relacionados con la moringa

## Caso R09
Elementos clave:
- e1: El cabezal de la bomba se fabricó fuera de tolerancia y el enchufe entraba forzado.
- e2: El ajuste forzado abría los terminales y dejaba la conexión suelta.
- e3 (NÚCLEO): La unión floja ofrecía alta resistencia y se calentaba hasta derretirse.
- e4: El sobrecalentamiento podía prender fuego aun con el auto apagado.

### Conclusión R09-6b866e
Explicación: El conector eléctrico de la bomba de combustible desarrolla una falla (falso contacto con calentamiento resistivo) que funde el plástico y puede iniciar el incendio aun con el vehículo apagado y estacionado, de ahí la orden de estacionar afuera y no guardarlos en garajes en más de 1,3 millones de Jeep.
Alternativas declaradas:
- Fuga de combustible sobre el conector como causa primaria y no la falla eléctrica
- Defecto del arnés principal por roce en otra zona del cableado

### Conclusión R09-a97d8f
Explicación: Terminales hembra del conector de la bomba abiertos y deformados con contacto parcial sobre los pines, generando calentamiento resistivo con plástico fundido concentrado en ese conector; el circuito queda alimentado por la batería aun con el encendido apagado, por lo que el incendio puede iniciarse con el vehículo estacionado y apagado, motivando el retiro 26V363 y la orden de estacionar afuera
Alternativas declaradas:
- Roce del arnés contra carrocería en otro punto del cableado
- Accesorios no originales o intervención posterior

## Caso R10
Elementos clave:
- e1 (NÚCLEO): Personal ya desenmascarado reevaluó a posteriori la respuesta de nueve pacientes tras cerrar la base de datos.
- e2: La reevaluación hizo que el fármaco pareciera eficaz.
- e3: No se declaró en el artículo y, al saberse, los autores pidieron la retractación.

### Conclusión R10-236b5d
Explicación: Tavneos causa daño hepático grave intrínseco (más de 70 lesiones graves y 8 muertes con lotes que cumplían pureza y potencia, descartando contaminación) y además su eficacia nunca estuvo válidamente demostrada según el CDER: fármaco hepatotóxico sin beneficio probado, por lo que el balance riesgo-beneficio es negativo.
Alternativas declaradas:
- Contaminante no detectado en los análisis de pureza de rutina
- Interacción con otros fármacos en los pacientes afectados y no toxicidad propia

### Conclusión R10-9e4f66
Explicación: Tavneos con balance beneficio-riesgo desfavorable: más de 70 lesiones hepáticas graves ligadas por la FDA incluidos ocho muertos con mayoría de desenlaces serios, combinado con ausencia de demostración válida de eficacia porque con las evaluaciones originales la diferencia frente al comparador en el objetivo primario deja de cumplir el criterio preespecificado
Alternativas declaradas:
- La lesión hepática se debe a la vasculitis de base o a medicación concomitante y no a Tavneos
- El fracaso del objetivo primario se debe a sesgo en la re-adjudicación y el fármaco sí es eficaz

## Caso R12
Elementos clave:
- e1 (NÚCLEO): La válvula del regulador quedó entreabierta y acumuló presión de vapor en los cilindros.
- e2: El inversor estaba fuera de la posición que impide el arranque.
- e3: El freno de aire no estaba bien aplicado porque la dotación no había sido instruida en ese sistema.
- e4: La máquina partió sola con el operario en medio.

### Conclusión R12-29ea0f
Explicación: Locomotora dejada para el acople sin el freno de aire completamente aplicado, con presión por debajo de lo requerido, y con la palanca del inversor fuera de la posición central que evita el movimiento en parada; la máquina se movió sin orden mientras la acoplaban a otra en el andén 1 y el operario entre ambas debió caminar entre las máquinas en movimiento
Alternativas declaradas:
- Apertura accidental del regulador con vapor a cilindros como causa única
- Deriva por pendiente de la vía sin fallo de freno ni de inversor

### Conclusión R12-f2bd08
Explicación: La locomotora se movió sin orden durante el acople porque su freno de aire no estaba aplicado completamente (presión por debajo de lo requerido). Sin freno que la sujetara, bastó el esfuerzo del acople o una deriva para desplazarla con el operario entre ambas máquinas, que debió caminar entre locomotoras en movimiento.
Alternativas declaradas:
- Fuga en el regulador que admitió vapor a los cilindros
- Soltado inadvertido del freno por otra persona durante el evento

## Caso R13
Elementos clave:
- e1 (NÚCLEO): La reparación del pandeo no liberó la tensión térmica del riel soldado.
- e2: El desalineamiento persistió con 93 °F sin inspección ese día.
- e3: La vía se abrió al pasar el tren.
- e4: Un acople con un vacío interno de fábrica se quebró y agravó el descarrilamiento.

### Conclusión R13-d13db9
Explicación: Pandeo por calor (sun kink) recidivante en el riel soldado continuo sobre el puente: el pandeo del 26 de junio se reparó solo realineando y calzando balasto, sin cortar el riel ni reajustar su temperatura neutra, dejando tensiones de compresión latentes. Con 93 °F el 6 de julio y sin inspección de la vía ese día, el riel volvió a pandear en la misma zona (desalineamiento lateral medido) y descarrilaron 21 vagones con derrame de hidróxido de sodio.
Alternativas declaradas:
- Falla del tablero del puente reconstruido en mayo como causa del desalineamiento
- Exceso de velocidad del tren sobre el puente

### Conclusión R13-ac3a48
Explicación: Recurrencia del pandeo por calor en el riel soldado continuo sobre el puente: tras el pandeo del 26 de junio la reparación del 1 de julio solo realineó y calzó balasto sin cortar ni reajustar la temperatura neutra, dejando tensiones de compresión atrapadas; se levantó la restricción sin inspección el día del siniestro y el 6 de julio a las 3:19 p.m. descarrilaron 21 vagones con derrame de hidróxido de sodio aun circulando por debajo de 25 mph
Alternativas declaradas:
- Fallo del tablero del puente reconstruido en mayo como causa primaria
- Causa originada en el material rodante y no en la vía

## Caso R14
Elementos clave:
- e1: La tripulación insistió en aterrizar bajo lluvia intensa.
- e2: Perdió las referencias visuales externas.
- e3 (NÚCLEO): Perdió el control del avión en el toque, produciendo el aterrizaje brusco sin falla mecánica.

### Conclusión R14-dd959c
Explicación: Aproximación desestabilizada bajo lluvia intensa con visibilidad reducida: grandes variaciones de alabeo y cabeceo y alta tasa de descenso al contacto, terminando en un aterrizaje violento (golpe) sin falla mecánica previa (mandos, motores y tren funcionaban). Sin heridos entre los 14 ocupantes.
Alternativas declaradas:
- Cizalladura de viento o microrráfaga en corta final
- Hidroplaneo en la pista mojada tras el contacto

### Conclusión R14-be900f
Explicación: Aproximación final inestable con lluvia intensa y visibilidad reducida, con grandes variaciones de alabeo y cabeceo y alta tasa de descenso al contacto; la tripulación perdió referencia visual en la parte final y continuó en lugar de frustrar, con el avión con combustible por encima del mínimo y sin indicios de falla previa en mandos, motores o tren, terminando en un golpe fuerte sin heridos entre los 14 ocupantes
Alternativas declaradas:
- Cizalladura o microrráfaga en final como causa primaria ajena a la tripulación
- Fallo previo de mandos, motores o tren