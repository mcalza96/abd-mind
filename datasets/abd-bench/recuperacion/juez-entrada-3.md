Eres un juez ciego. Para cada caso tienes los ELEMENTOS CLAVE del mecanismo documentado y varias LISTAS de explicaciones candidatas, identificadas con códigos (no sabes quién ni cómo las generó). Para cada candidata y cada elemento decide si la candidata lo cubre:
- "si": la candidata afirma ese mismo eslabón causal (puede usar otras palabras, pero el mecanismo concreto es el mismo).
- "parcial": apunta a la misma zona o pieza pero sin el eslabón concreto (p. ej. "falla en el sistema de control del elevador" frente a "el tapón suelto trabó el elevador").
- "no": no lo menciona, o afirma algo distinto.
Cubrir el tema no basta: se exige el eslabón causal. Juzga cada candidata por sí sola.

Responde SOLO con JSON: {"listas": [{"codigo": "...", "juicios": [{"pos": 1, "e1": "si|parcial|no", "e2": "..."}]}]}, con un juicio por candidata, en el orden de la lista.

## Caso R14
Elementos clave:
- e1: La tripulación insistió en aterrizar bajo lluvia intensa.
- e2: Perdió las referencias visuales externas.
- e3: Perdió el control del avión en el toque, produciendo el aterrizaje brusco sin falla mecánica.

### Lista R14-1dc1ee
1. La fatiga de la tripulación tras un largo vuelo transatlántico degradó su desempeño y llevó a una aproximación inestable con aterrizaje duro o contacto prematuro con el terreno.
2. Descenso por debajo de la altitud mínima en una aproximación de no precisión en Birmingham, sin referencias visuales adecuadas, que hizo que el avión golpeara el terreno o la pista antes de tiempo, como en el UPS 1354.
3. Aterrizaje duro por una tasa de descenso excesiva en el enderezamiento debido a velocidad mal gestionada o configuración tardía.
4. Cizalladura del viento o ráfagas en la aproximación final que hicieron perder sustentación cerca del suelo y provocaron un impacto fuerte.
5. Salida o desviación de pista por pista mojada, hidroplaneo o frenado deficiente que hizo que el avión chocara con obstáculos o terreno al final de la pista.
6. Error en la configuración del sistema de gestión de vuelo o del perfil de descenso que dejó al avión más bajo de lo previsto en la aproximación.
7. Mala visibilidad por niebla, lluvia o noche que impidió a la tripulación ver la pista a tiempo para corregir la trayectoria.
8. Falla mecánica del tren de aterrizaje (colapso o no extensión completa) que convirtió el aterrizaje en un golpe estructural.
9. Combustible escaso al final del trayecto transatlántico que presionó a la tripulación a aterrizar sin abortar una aproximación inestable.
10. Uso de una pista con ayudas limitadas (sin ILS operativo) que obligó a una aproximación más exigente y propensa al error.

### Lista R14-ecbbc4
1. La tripulación, fatigada tras un vuelo transatlántico nocturno con solo dos pilotos, realizó una aproximación inestabilizada y el avión tocó tierra antes de la pista; el impacto fue absorbido por el tren de aterrizaje y la estructura, por lo que nadie resultó herido.
2. El avión aterrizó largo y rápido en una pista mojada, no logró detenerse antes del final y se salió por el extremo, golpeando las luces de aproximación y deteniéndose en el césped, lo que causó daños pero no lesiones.
3. Una pata del tren de aterrizaje principal falló por fatiga del metal al tocar, el ala golpeó la pista y el avión se deslizó sobre un costado; la baja velocidad y altura del impacto evitaron heridos.
4. Durante el flare, la tripulación sobre-rotó el avión y la cola golpeó la pista, produciendo un daño estructural en la sección trasera pero sin heridos debido a la baja energía del contacto.
5. Una cizalladura del viento en los últimos cien pies hizo perder sustentación al avión, que cayó bruscamente sobre la pista; la estructura resistió el golpe y los cinturones de seguridad protegieron a los ocupantes.
6. El avión sufrió una colisión con aves en la aproximación final, lo que dañó el morro y un motor; la tripulación aterrizó de inmediato con un golpe seco, pero sin heridos.
7. Un fallo hidráulico impidió desplegar completamente los flaps, forzando una aproximación a mayor velocidad y un aterrizaje duro que dañó el fuselaje, aunque no causó lesiones.
8. El avión entró en la estela turbulenta de un reactor más grande en final, sufrió una sacudida violenta y aterrizó de forma descontrolada, impactando contra la pista sin heridos.
9. Los frenos fallaron tras el aterrizaje, el avión no pudo reducir la velocidad y se salió de la pista, golpeando un terraplén; la baja velocidad al impacto evitó víctimas.
10. El piloto no compensó correctamente el viento cruzado, el ala tocó el suelo durante el aterrizaje y el avión se salió de la pista, causando daños pero no lesiones.

### Lista R14-2937e5
1. La fatiga acumulada de la tripulación tras un vuelo transatlántico nocturno desde Irlanda provocó una aproximación inestabilizada, con descenso rápido y un aterrizaje duro que dañó el tren principal, pero los ocupantes no sufrieron heridas gracias a los cinturones y la absorción de energía de los asientos.
2. Una cizalladura del viento a baja altura en la final hizo perder sustentación al avión, que cayó bruscamente y golpeó la pista con una velocidad vertical excesiva, causando daños estructurales pero sin lesiones porque el impacto fue absorbido por el tren de aterrizaje.
3. La pista mojada por lluvia intensa redujo la eficacia de los frenos y el avión sufrió una excursión lateral tras el aterrizaje, saliéndose a terreno blando y golpeando un obstáculo, pero la baja velocidad y la desaceleración gradual evitaron heridas.
4. El tren de aterrizaje de morro colapsó por fatiga del material al tocar tierra, haciendo que el morro impactara contra la pista y se arrastrara, aunque la estructura de la cabina resistió y no hubo heridos.
5. Un impacto de ave en uno de los motores durante la aproximación redujo la potencia y obligó a un aterrizaje inmediato y duro, pero el avión se detuvo sin salirse de la pista y sin lesionados.
6. La estela turbulenta de un avión pesado que aterrizó antes hizo que el avión se inclinara bruscamente y perdiera altura, golpeando la pista con un ala y el tren, lo que dañó la aeronave pero no causó heridas.
7. Un error de calibración del altímetro hizo que la tripulación descendiera por debajo de la senda de planeo y el avión golpeara árboles antes de la pista, como en UPS 1354, pero la baja velocidad y la masa reducida evitaron víctimas.
8. Una ráfaga descendente (microburst) alcanzó al avión a baja altura, forzando un contacto prematuro con el terreno antes de la pista; el tren de aterrizaje se hundió en el barro y el impacto fue absorbido sin heridos.
9. Un fallo mecánico en el sistema de frenos tras el aterrizaje impidió detener la aeronave a tiempo, que se salió por el extremo de la pista y golpeó la antena localizadora, pero la célula resistió y no hubo lesiones.
10. El piloto aplicó una corrección excesiva en el flare para compensar un descenso rápido, provocando un golpe de cola (tail strike) y un rebote que dañó la estructura trasera, pero los ocupantes no resultaron heridos.

### Lista R14-fe33b2
1. La tripulación voló una aproximación inestable y descendió por debajo de la senda de planeo, de modo que el avión rozó árboles o las luces de aproximación antes de la pista; el contacto progresivo disipó energía y la célula y los asientos absorbieron el golpe sin lesiones.
2. El avión tocó pista con una velocidad vertical excesiva y el tren principal colapsó, pero los asientos certificados para 16 g y los cinturones de seguridad evitaron que los ocupantes se golpearan.
3. Tras el aterrizaje, el avión se salió de pista por viento cruzado o fallo de frenos y se detuvo en terreno blando; la baja velocidad y la deformación del tren absorbieron la energía del impacto.
4. El tren de aterrizaje no se desplegó por un fallo hidráulico y el fuselaje se deslizó sobre la pista; la fricción desaceleró gradualmente el avión y la cabina permaneció intacta.
5. Los motores se apagaron por agotamiento de combustible en la aproximación final, el piloto planeó y aterrizó de emergencia en una zona blanda antes de la pista, y el impacto a baja velocidad no generó fuerzas lesivas.
6. Una bandada de aves dañó un motor crítico durante la aproximación, lo que obligó a un aterrizaje forzoso en el césped; la estructura resistió el golpe y los ocupantes iban bien sujetos.
7. El avión atravesó la estela turbulenta de un reactor pesado que lo precedía, rodó bruscamente y el ala tocó el suelo; el impacto fue localizado y los ocupantes, con cinturones, no sufrieron lesiones.
8. Un microestallido o cizalladura descendente empujó al avión contra la pista en los últimos metros, causando un golpe fuerte pero sin deformación de la cabina ni heridos.
9. Un dron colisionó con el morro o el ala durante la aproximación, causando daños estructurales que forzaron un aterrizaje inmediato; la energía del impacto fue baja y no alcanzó a los ocupantes.
10. Un sabotaje interno con un artefacto explosivo de baja potencia en la bodega dañó sistemas y provocó un aterrizaje de emergencia, pero la cabina presurizada y la distancia al artefacto evitaron lesiones.

### Lista R14-1adbf5
1. La aeronave descendió por debajo de la senda de planeo en la aproximación final a Birmingham, impactó con árboles o luces de aproximación antes de la pista —igual que en el accidente de UPS 1354— y, aunque sufrió daños, logró aterrizar sin que la desaceleración causara heridas a los 14 ocupantes.
2. Una cizalladura del viento a baja altura hizo que el avión tocara la pista con una tasa de descenso muy superior a la normal; la estructura y los asientos absorbieron el golpe y nadie resultó lesionado.
3. El tren de aterrizaje principal se hundió en el asfalto o falló un amortiguador al tomar tierra, produciendo un impacto seco contra la pista que dañó el avión pero no deformó la cabina.
4. Durante la aproximación final, el avión golpeó un ave en el morro o en un motor; el impacto se sintió como un golpe, activó la investigación, pero no penetró la cabina ni causó heridos.
5. En la carrera de aterrizaje, una rueda se salió del borde de la pista y golpeó las luces de balizamiento, generando daños en el tren de aterrizaje sin que la tripulación ni los pasajeros sufrieran lesiones.
6. El piloto realizó una rotación excesiva al aterrizar y la cola golpeó la pista (tail strike); el contacto fue absorbido por la estructura trasera sin comprometer la integridad de la cabina.
7. Una ráfaga descendente o microestallido hizo que un ala o un motor tocara el suelo antes que las ruedas, produciendo un golpe y daños localizados pero sin fuego ni heridos.
8. El avión chocó contra un vehículo de servicio o un objeto no identificado en la pista durante el aterrizaje o el rodaje, causando un impacto que se sintió a bordo pero sin lesiones.
9. Una falla hidráulica o de frenos tras el aterrizaje provocó que el avión se saliera del eje y golpeara un obstáculo lateral (señalización o banquina), deteniéndose sin lesionar a los ocupantes.
10. El vuelo atravesó una tormenta con granizo o turbulencia severa que abolló el fuselaje y se sintió como un golpe, pero la tripulación mantuvo el control y aterrizó sin heridos.

### Lista R14-ab6f9d
1. La fatiga de la tripulación tras el vuelo transatlántico desde Irlanda provocó una aproximación no estabilizada y un aterrizaje duro en Birmingham; el tren de aterrizaje y los asientos absorbieron la energía del golpe, por lo que nadie resultó herido.
2. El avión aterrizó largo y se salió de la pista, como en el accidente del UPS 1354 en ese mismo aeropuerto, pero la tripulación aplicó reversa y frenos a tiempo y se detuvo en el EMAS; la desaceleración gradual no generó fuerzas lesivas.
3. El tren de nariz colapsó al tocar la pista y la proa golpeó el asfalto, pero la baja velocidad y el diseño antifricción de la panza hicieron que el avión se deslizara sin transmitir una desaceleración brusca a la cabina.
4. Un microburst en la final hizo que el avión descendiera bruscamente y tocara con fuerza, pero los cinturones de seguridad y los asientos anti-impacto disiparon la energía del golpe.
5. La turbulencia de estela de un avión pesado que despegó antes sacudió violentamente al avión en vuelo, pero el piloto recuperó el control y los pasajeros estaban asegurados, evitando heridas.
6. Una bandada de aves grandes impactó el radomo y el ala durante la aproximación, causando una sacudida brusca, pero no penetró la cabina ni dañó los controles críticos, por lo que no hubo heridos.
7. Un error de cálculo de combustible en el vuelo transatlántico apagó ambos motores y el avión planeó hasta Birmingham, aterrizando con un golpe corto pero sin incendio; la baja velocidad de impacto evitó lesiones.
8. Una falla no contenida de un motor desprendió fragmentos que golpearon el fuselaje, pero no atravesaron la cabina ni los tanques, y la tripulación aterrizó de emergencia sin que nadie resultara herido.
9. Una explosión sónica de una aeronave militar supersónica que pasó cerca generó una onda de choque que sacudió al avión en vuelo y produjo un golpe estructural leve, pero los cinturones evitaron heridas.
10. Un ciberataque bloqueó los controles de vuelo y provocó un movimiento brusco del avión, pero el piloto usó controles manuales de emergencia y aterrizó con un golpe seco; los arneses evitaron lesiones.

### Lista R14-57ca78
1. Aterrizaje duro por aproximación inestable con viento cruzado: el avión tocó la pista con una velocidad vertical excesiva, transmitiendo una gran carga al tren de aterrizaje y al fuselaje, pero los pasajeros y tripulantes iban sujetos con cinturones y el impacto no superó los límites de tolerancia humana, por lo que no hubo heridos.
2. Excursión de pista por hidroplaneo en una pista encharcada: al aterrizar, los neumáticos perdieron contacto con el asfalto, el avión se deslizó fuera de la pista y golpeó señales y terreno blando, pero la desaceleración fue gradual y los ocupantes no sufrieron lesiones.
3. Colapso del tren de aterrizaje principal por fatiga del metal: al tomar contacto, una de las patas cedió y el avión impactó con el vientre y los motores contra la pista, pero la estructura de deformación programada y los asientos antitrauma absorbieron la energía, evitando heridas.
4. Impacto de una bandada de aves en la aproximación final que dañó un motor: la tripulación perdió potencia, realizó un aterrizaje forzoso y el avión golpeó el suelo más allá de la pista, pero los arneses y la posición de braceo evitaron lesiones.
5. Error del piloto por fatiga y descenso prematuro, similar al UPS 1354: una aproximación no estabilizada llevó a un aterrizaje duro y daños en la pista, pero los sistemas de retención evitaron heridos.
6. Cizalladura del viento o microestallido en la final: una corriente descendente empujó al avión contra la pista, causando un golpe seco, pero la estructura del avión y los asientos disiparon la energía sin causar lesiones.
7. Encuentro con turbulencia de estela de un avión pesado que precedió en la aproximación: la estela provocó un alabeo súbito y un contacto brusco con la pista, pero los ocupantes estaban asegurados y el impacto fue absorbido por el tren.
8. Fallo hidráulico que impidió la extensión del tren de aterrizaje: el avión realizó un aterrizaje de panza, golpeando la pista con el fuselaje y los motores, pero la baja velocidad y la resistencia estructural evitaron lesiones.
9. Colisión con un dron en la fase de aproximación: el impacto dañó el borde de ataque del ala y provocó un aterrizaje de emergencia con golpe en la pista, pero la cabina permaneció intacta y los ocupantes ilesos.
10. Impacto de basura espacial o meteorito pequeño que atravesó el fuselaje: el objeto golpeó el avión, causando un ruido fuerte y daños localizados, pero la tripulación aterrizó de inmediato y nadie resultó herido por la baja energía y la rápida despresurización controlada.

## Caso R04
Elementos clave:
- e1: Un ingeniero sin experiencia en la tarea abrió a la vez las dos válvulas que aislaban el Horno 5.
- e2: El doble paso dejó retornar gas craqueado inflamable al fogón encendido.
- e3: El gas se encendió y el horno estalló seis minutos después.
- e4: Una interfaz confusa y controles solo administrativos facilitaron el error.

### Lista R04-001bae
1. Una acumulación progresiva de coque dentro de los tubos radiantes aisló térmicamente la pared y elevó la temperatura del metal por encima del límite de fluencia de la aleación. El tubo debilitado se rajó a presión de operación y el etano y etileno fugados se encendieron en el firebox provocando la explosión el incendio y la liberación reportada.
2. Una válvula de alimentación se cerró o falló y dejó al horno sin flujo de proceso mientras los quemadores seguían aportando calor pleno. Sin el enfriamiento del gas interno los tubos se sobrecalentaron en minutos hasta reventar y descargar hidrocarburos que explosionaron al contacto con la llama.
3. Uno o varios quemadores sufrieron apagado de llama por alteración del gas combustible o del aire de tiro y el gas sin quemar se acumuló en la caja radiante. Una reignición retardada produjo una explosión en el firebox que rompió tubos adyacentes y desató el incendio prolongado con daños masivos al horno.
4. Quemadores desalineados o con puntas dañadas tras un mantenimiento proyectaron llama directamente contra una zona del serpentín y crearon un punto caliente persistente. Ese sobrecalentamiento localizado redujo la resistencia de la aleación hasta perforar el tubo y liberar etileno que alimentó la explosión.
5. Una obstrucción aguas abajo por ensuciamiento del intercambiador de quench o por una válvula cerrada por error elevó la presión dentro del serpentín radiante. La sobrepresión superó la resistencia del tubo más débil y lo hizo estallar liberando de golpe el inventario que explotó y ardió.
6. Un cordón de soldadura o un tramo de tubo con defecto de fabricación no detectado sufrió fatiga térmica por ciclos repetidos de operación y decoking. La grieta creció hasta atravesar la pared a presión y el chorro de hidrocarburo a alta presión se inflamó causando la explosión y el fuego.
7. Durante una maniobra de decoking con vapor y aire se produjo un error de secuencia que introdujo choque térmico u oxidación acelerada en un tubo ya carburizado y fragilizado. El tubo agrietado cedió al volver a carga con etano y la fuga encendida destruyó la estructura del horno.
8. La alimentación de etano entró contaminada con hidrocarburos más pesados o compuestos de azufre que aumentaron drásticamente la formación de coque y la corrosión bajo tensión. Ese deterioro acelerado provocó el taponamiento parcial y la rotura de un tubo con la consiguiente explosión de la nube liberada.
9. Un fallo de causa común en el sistema de control básico y en el sistema instrumentado de seguridad por error de configuración o manipulación cibernética inhibió los enclavamientos de corte por alta temperatura de tubo. Sin protección automática el horno entró en excursión térmica hasta la rotura del serpentín y la explosión del combustible liberado.
10. Un impacto externo como caída de herramienta pesada rayo o dron o una intervención intencional dañó una línea de alimentación o de combustible en el exterior del horno y generó una fuga masiva. La nube alcanzó los quemadores y detonó y el frente de llama y la sobrepresión rompieron el horno e iniciaron el incendio de 95 millones de daños.

### Lista R04-717b6c
1. Acumulación interna de coque en los tubos radiantes aisló térmicamente el flujo de etano, sobrecalentó el metal hasta la rotura por termofluencia y liberó hidrocarburos a alta presión y temperatura que se encendieron con los quemadores provocando la explosión y el incendio.
2. Fisura en la línea de gas combustible o en un quemador dentro de la caja del horno permitió la acumulación de gas no quemado que formó una mezcla explosiva y deflagró al alcanzar un piloto, y la onda rompió tubos adyacentes liberando etileno que alimentó el incendio.
3. Las soldaduras de los codos de salida y la línea de transferencia fallaron por fatiga térmica tras cientos de ciclos de operación-descoquizado, abriéndose bajo presión y liberando etano-etileno supercalentado que se autoignitó y causó la explosión.
4. Carburización prolongada a alta temperatura fragilizó los tubos de aleación alta en níquel y redujo su ductilidad hasta que una grieta pasante se propagó súbitamente y descargó el inventario que se encendió en la caja radiante.
5. Un taponamiento parcial del intercambiador de enfriamiento brusco aguas abajo elevó la presión en el serpentín radiante por encima de su diseño, reventando un tubo y proyectando una nube de etileno que explotó al contacto con las llamas.
6. Durante una maniobra de descoquizado o arranque se alimentó etano sin suficiente vapor diluyente a tubos muy calientes, lo que aceleró la coquización y la sobrepresión local hasta romper el tubo y liberar combustible que se incendió.
7. Un fallo del control de tiro y del exceso de aire generó combustión incompleta y acumulación de inquemados en la zona convectiva, donde una ignición retardada produjo la explosión que dañó la estructura y rompió líneas de proceso.
8. La inyección irregular de vapor o agua de descoquizado provocó choque térmico y tensiones cíclicas que agrietaron un tubo, y la fuga a alta velocidad se atomizó en la caja caliente encendiéndose violentamente.
9. Un instrumento de temperatura de metal o presión falló y el sistema de enclavamiento no cortó la alimentación ni el combustible, permitiendo que la excursión térmica continuara hasta la rotura catastrófica y el incendio posterior.
10. Corrosión externa bajo aislamiento o vibración dañó una tubería de alimentación fuera del horno, liberando etano que migró hacia la caja caliente donde encontró fuente de ignición y la deflagración resultante rompió el horno e inició el incendio costoso.

### Lista R04-aa9384
1. Ruptura de un tubo de radiación por sobrecalentamiento y coquización: el coque se acumuló en el interior del serpentín, redujo el flujo y el enfriamiento, y la pared alcanzó temperatura de fluencia hasta abrirse; el etano/etileno a presión escapó al cajón de fuego y se encendió, causando la explosión y el incendio.
2. Pérdida de la relación vapor/etano por falla de control: una válvula o medidor de vapor de dilución disminuyó el vapor, elevando la temperatura y la deposición de coque en los tubos hasta su ruptura, con ignición posterior del hidrocarburo liberado.
3. Falla de un quemador con llama impingente: un quemador desajustado o bloqueado dirigió la llama contra los tubos, creando un punto caliente local que adelgazó y perforó el metal, liberando etileno que se encendió dentro del horno.
4. Corrosión o erosión interna de tubos por contaminantes: compuestos ácidos o partículas en la alimentación redujeron el espesor de pared por debajo del mínimo, y la presión de proceso provocó una grieta que liberó hidrocarburo al firebox y originó el incendio.
5. Fuga en brida, colector o sello del serpentín: una junta o soldadura del circuito de etano/etileno falló y el hidrocarburo a presión se mezcló con los gases calientes del horno, encendiéndose de inmediato y dañando el equipo.
6. Error en la secuencia de decoquización: una válvula mal alineada o una purga incompleta permitió que aire se mezclara con hidrocarburo residual en el horno; al alcanzar la temperatura de ignición, la mezcla deflagró y provocó la explosión.
7. Entrada de aire durante el arranque tras una parada: la purga con vapor no eliminó todo el oxígeno del cajón de fuego antes de introducir etano, formando una atmósfera inflamable que se encendió al encender quemadores o por una superficie caliente.
8. Falla del sistema de parada de emergencia: sensores de temperatura o presión no detectaron el sobrecalentamiento, o las válvulas de corte no cerraron, permitiendo que la condición anómala progresara hasta la ruptura del tubo y la fuga masiva.
9. Choque térmico por inyección repentina de vapor o agua: durante una maniobra de emergencia, el contacto de fluido frío con tubos calientes causó agrietamiento térmico, ruptura y escape de etileno que se incendió en el horno.
10. Defecto de fabricación o soldadura en un tubo o colector: una soldadura defectuosa o inclusión falló bajo ciclos térmicos y presión, abriendo una grieta que liberó hidrocarburo al cajón de fuego, donde se encendió.

### Lista R04-ca54d2
1. Un tubo radiante envejecido por miles de horas a 850-900 °C sufrió termofluencia, carburización y adelgazamiento hasta fisurarse, liberando etano/etileno a alta presión en la caja de fuego caliente cuya ignición instantánea produjo la explosión, el incendio y la liberación de unas 5.100 libras.
2. Acumulación excesiva de coque en el interior del serpentín restringió el flujo y redujo el enfriamiento interno, elevando la temperatura de metal por encima del límite de diseño hasta romper el tubo y descargar hidrocarburos inflamados que explotaron contra los quemadores.
3. Una pérdida parcial del vapor de dilución por fallo de control elevó la presión parcial de etano y la temperatura de craqueo, acelerando la coquización y el sobrecalentamiento del tubo hasta su estallido con fuga masiva, deflagración e incendio del horno.
4. El apagado inadvertido de varios quemadores permitió la acumulación de gas combustible sin quemar en la caja de fuego, y su reignición retardada provocó una explosión en el hogar que fracturó los serpentines de proceso y liberó etileno que alimentó el incendio.
5. Una fuga en válvulas o líneas del tren de gas combustible acumuló una mezcla explosiva dentro del horno, que al alcanzar un quemador encendido detonó y dañó los tubos de etano, causando la rotura, la gran liberación y el incendio prolongado.
6. Un bloqueo o cierre erróneo de la válvula de alimentación mantuvo el aporte de calor con serpentín sin flujo suficiente, sobrecalentando el metal en seco hasta el colapso del tubo y la descarga súbita de hidrocarburos que explotaron.
7. Durante una operación de descoquización con vapor-aire se produjo una excursión exotérmica descontrolada por exceso de aire o de temperatura, sobrepresionando y rompiendo los tubos y proyectando gases calientes que explotaron e incendiaron la estructura.
8. La fisura por fatiga térmica y corrosión en un pigtail, codo de salida o colector de cruce sometido a ciclos de calentamiento-enfriamiento se abrió a plena presión, inyectando etileno sobrecalentado al exterior del serpentín que se inflamó y generó la explosión en la caja.
9. La entrada súbita de agua o condensado al serpentín caliente provocó vaporización instantánea y un pico de presión por golpe de vapor, que reventó el tubo y liberó la carga de proceso cuya combustión causó la explosión y el incendio.
10. El colapso o desplazamiento de soportes y guías por deformación térmica dejó que los tubos rozaran el refractario y se adelgazaran por abrasión y punto caliente, hasta perforarse y fugar hidrocarburos que ignitaron y destruyeron el horno, con daños que exigieron siete meses de reconstrucción.

### Lista R04-682027
1. La causa más probable es la ruptura de un tubo del horno por coquización y sobrecalentamiento local: el coque redujo el flujo interno y elevó la temperatura de pared hasta superar la resistencia del metal, de modo que el etano/etileno a presión escapó al hogar y se encendió con los quemadores, produciendo la explosión y el incendio.
2. Una pérdida de la relación vapor/etano por fallo del control de dilución hizo que el etano se craqueara con coque rápido y puntos calientes, lo que adelgazó y rompió un tubo; la fuga de hidrocarburo inflamable explica la explosión y la posterior liberación de etileno.
3. El desajuste de quemadores provocó llama impingement sobre los tubos del radiant, sobrecalentándolos hasta agrietarlos; la fuga de etano/etileno se mezcló con aire en la caja y se encendió, causando la explosión y el incendio.
4. Una falla en la válvula de alimentación o un golpe de ariete por entrada súbita de líquido o agua causó choque térmico y ruptura mecánica de un tubo; el hidrocarburo liberado encontró ignición en el hogar y generó la deflagración.
5. Durante la operación de decoking, una secuencia incorrecta de aire y vapor formó una mezcla inflamable o sobrepresión dentro de los tubos; la ignición rompió el tubo y liberó etileno y productos de combustión.
6. La corrosión o erosión por contaminantes del etano, como sales, azufre o CO2, adelgazó la pared de un tubo hasta fallar bajo presión; la fuga de hidrocarburo se inflamó y dio lugar a la explosión y al incendio.
7. Un fallo de refractario o del sello de un quemador permitió que gas combustible se acumulara en una bolsa y deflagrara, dañando los tubos y liberando etano/etileno que alimentó el incendio.
8. Una fuga previa de etileno por una brida o empaque en el área del horno fue encendida por electricidad estática o por una descarga atmosférica cercana, generando una nube inflamable que explotó y prendió fuego.
9. La autoignición de sulfuro de hierro pirofórico al ingresar aire durante una parada o mantenimiento encendió hidrocarburo residual; la deflagración resultante dañó el horno y liberó etileno y productos de combustión.
10. Un acto intencional de sabotaje o vandalismo, como bloquear una válvula de alivio o manipular instrumentos de control, provocó sobrepresión y ruptura del tubo; la liberación y el fuego explican las observaciones, aunque es la hipótesis menos probable.

### Lista R04-1c679b
1. Fuga de etileno o hidrocarburos dentro de la caja de fuego del horno de craqueo que formó una mezcla inflamable y se encendió, causando la explosión y el incendio posterior.
2. Ruptura de un tubo del serpentín de craqueo por sobrecalentamiento, carburización o fatiga térmica, liberando hidrocarburo al interior del horno caliente que ignició de forma explosiva.
3. Pérdida de llama en los quemadores con continuidad del suministro de gas combustible, que acumuló gas sin quemar en la cámara y luego se reencendió explosivamente.
4. Error durante una operación transitoria (arranque, decoquizado o cambio de alimentación) con secuencia de válvulas incorrecta que introdujo hidrocarburo o aire en la zona equivocada del horno.
5. Falla del sistema instrumentado de seguridad o del enclavamiento de quemadores que no cortó el combustible ante una condición anormal, permitiendo la acumulación de mezcla explosiva.
6. Purga insuficiente del horno antes del encendido de quemadores, dejando gas residual que explotó al reencender.
7. Falla de una brida, válvula o junta en la línea de alimentación o de salida del horno que liberó etileno a alta temperatura que autoignitó.
8. Desbalance de flujo entre serpentines que dejó un paso sin caudal y lo sobrecalentó hasta romper, liberando hidrocarburo en la caja de fuego.
9. Corrosión o erosión no detectada en tubos o colectores por inspección y mantenimiento deficientes, que terminó en ruptura bajo presión.
10. Falla de control de presión de tiro (ventiladores o damper) que generó presión positiva en el horno y retroceso de llama con explosión.

### Lista R04-89dfe7
1. Ruptura por fluencia lenta (creep) y sobrecalentamiento de un tubo del serpentín radiante adelgazado y aislado por depósito interno de coque, que se abrió a presión de proceso y liberó etano-etileno al hogar donde se inflamó causando explosión e incendio.
2. Falla de una soldadura circunferencial en tubo de aleación de alta temperatura HP/Nb debilitada por fatiga térmica cíclica y creep, que cedió súbitamente y proyectó un chorro de hidrocarburo a alta presión que explotó al contacto con los quemadores.
3. Taponamiento progresivo por coque del serpentín y del enfriador de gases (TLE) que elevó la presión interna del circuito hasta reventar un tubo, liberando de golpe el inventario de unas 5100 libras que alimentó la bola de fuego y los daños estructurales.
4. Fuga de gas combustible de alimentación a quemadores por brida, válvula o línea deteriorada que acumuló gas en la caja radiante confinada y al alcanzar concentración inflamable fue ignitada por un quemador piloto provocando la explosión mayor.
5. Pérdida transitoria de caudal de etano y vapor de dilución por fallo de control, bomba o válvula que dejó los tubos sin refrigeración interna, provocando sobretemperatura extrema, abultamiento y rotura múltiple con liberación masiva e incendio.
6. Combustión descontrolada durante una operación de descoquización con mezcla vapor-aire que generó exotermia y sobrepresión localizada, fracturando tubos con coque incandescente y expulsando revestimiento y paneles del horno.
7. Degradación metalúrgica por carburización, oxidación y fragilización de los tubos tras miles de horas a ~850-1100 °C, que redujo su resistencia a la rotura y causó estallido bajo presión normal de operación con fuga de etileno.
8. Apagón parcial de quemadores seguido de reencendido con acumulación de gas inquemado en el hogar, cuya deflagración deformó la estructura del horno y rompió un colector de proceso que aportó combustible al incendio secundario.
9. Rotura de soportes y guías del serpentín que permitió pandeo, vibración y roce de tubos calientes contra la estructura, adelgazando la pared hasta perforarla y generar un dardo de fuego que escaló a explosión de nube.
10. Cierre inadvertido o bloqueo de la válvula de salida del horno o del TLE que provocó un pico de presión del efluente caliente, fracturando el colector de salida y liberando etileno a alta temperatura que se autoignitó.

### Lista R04-0bbcfd
1. Sobrecalentamiento localizado de tubos del radiante por coqueo que redujo el flujo interno, elevando la temperatura de pared hasta fluencia y ruptura; el etano/etileno a presión escapó al cajón de combustión, se mezcló con aire y se encendió, generando la explosión y el incendio.
2. Falla de la relación aire/combustible en los quemadores por avería del control de tiro o de la válvula de gas, creando una atmósfera inflamable en el firebox que deflagró, dañó los tubos y liberó etileno.
3. Purga insuficiente o entrada de aire durante la decoquización: al abrir el horno con residuos calientes, se formó una mezcla etileno-aire dentro de la cámara que autoignició y provocó explosión local.
4. Corrosión por sales o ácido sulfhídrico en el metal de los tubos adelgazó la pared hasta perforación; la fuga de etano a alta presión se encendió por contacto con superficie caliente o llama, causando el incendio.
5. Fractura por fatiga térmica en el colector de salida debido a ciclos repetidos de calentamiento/enfriamiento por decoqueo, que abrió una grieta y permitió fuga de etileno hacia la zona de combustión.
6. Falla de una brida, sello o compensador de expansión en la línea de alimentación o salida, que liberó etileno a la atmósfera del horno y encontró una fuente de ignición, con explosión confinada parcialmente.
7. Golpe de ariete o condensación súbita en el sistema de quench por pérdida de vapor de dilución, que elevó la presión y reventó un colector, dispersando etileno que se incendió.
8. Ignición espontánea de sulfuro de hierro piróforo depositado en los tubos durante una parada o arranque, cuya deflagración local debilitó o perforó un tubo y permitió la fuga de etileno.
9. Arco eléctrico o fallo del sistema de encendido de quemadores que perforó la carcasa y encendió una fuga previa de etileno, actuando como fuente de ignición en el interior del horno.
10. Manipulación remota no autorizada o ciberataque a lazos de control que anuló alarmas y forzó sobrefuego, provocando el fallo del tubo y la posterior explosión.

### Lista R04-c5c0a5
1. Acumulación excesiva de coque en el interior del serpentín radiante por alargar la campaña entre descoquizados redujo la transferencia de calor y elevó la temperatura de pared hasta producir creep y adelgazamiento, lo que reventó un tubo y liberó etano/etileno a ~850°C que autoignicionó causando deflagración e incendio de inventario.
2. Fuga de gas combustible por un sello de quemador degradado o brida floja acumuló gas no quemado en una zona mal ventilada del firebox y su ignición retardada provocó la explosión en la caja de fuego, cuya onda rompió tubos de proceso adyacentes y alimentó el incendio secundario.
3. Pérdida parcial de caudal de etano y vapor de dilución por fallo de bomba o cierre inadvertido de una válvula mantuvo los quemadores a plena carga sobre tubos casi secos, sobrecalentándolos en minutos hasta el colapso y la liberación súbita que explotó.
4. Exotermia descontrolada durante una operación de descoquizado con vapor-aire por exceso de aire o fallo del control de temperatura quemó el coque demasiado rápido y superó el límite metalúrgico de los tubos, rompiéndolos y dejando escapar hidrocarburos que deflagraron.
5. Defecto preexistente en una soldadura de tubo de aleación HP Cr-Ni agravado por carburización, fatiga térmica cíclica y creep propagó una grieta hasta rotura súbita a presión normal, generando un chorro a alta presión que se encendió al contacto con refractario caliente.
6. Obstrucción aguas abajo por taponamiento de coque en la línea de transferencia o válvula de efluente cerrada por error elevó la presión del serpentín y la válvula de alivio atascada o mal tarada no alivió, provocando estallido por sobrepresión interna y posterior bola de fuego.
7. Ingreso inadvertido de agua o condensado al serpentín caliente que se vaporizó instantáneamente con expansión de ~1600 veces generó un pico de presión y choque térmico que fisuró varios tubos y liberó el inventario que explotó al inflamarse.
8. Válvula de control de combustible atascada en abierto combinada con analizadores de O2 mal calibrados sobrealimentó el firebox muy por encima de la temperatura de diseño, ablandando tubos y soportes hasta pandeo y rotura con fuga encendida.
9. Fallo de modo común de la instrumentación y del sistema instrumentado de seguridad por mala configuración tras mantenimiento o interferencia cibernética congeló las lecturas de temperatura de pared y bloqueó el disparo automático, permitiendo operar a ciegas hasta el fallo catastrófico.
10. Daño mecánico externo por caída de herramienta, maniobra de izaje próxima o acto intencional como impacto de dron perforó una línea de proceso o de fuel a alta temperatura, creando la fuga inicial cuya ignición inmediata produjo la explosión mayor y el incendio posterior.

### Lista R04-1d858d
1. La causa más probable fue la ruptura de un tubo del horno por sobrecalentamiento localizado al acumularse coque en su interior; el etano/etileno a alta presión escapó al cajón de fuego, se mezcló con los productos de combustión y se encendió, generando la explosión, el incendio y la liberación de unas 5.100 lb de etileno.
2. Una pérdida de la relación vapor/etano por falla de una válvula de dilución elevó la temperatura de pared de los tubos, aceleró el coqueo y provocó una ruptura por fluencia que liberó hidrocarburos inflamables al interior del horno.
3. Un bloqueo por coque o polímero en la línea de transferencia aguas abajo elevó la presión del lado proceso hasta superar la resistencia de un tubo o colector, causando una fuga de etileno que se inflamó de inmediato.
4. Un fallo de llama con purga insuficiente en los quemadores permitió que gas combustible se acumulara en el cajón de fuego; al reencenderse, la deflagración dañó los tubos de proceso y liberó etileno, que alimentó el incendio posterior.
5. La instrumentación de temperatura o el control de combustión fallaron y los quemadores sobrecalentaron la sección radiante por encima del límite metalúrgico, deformando y rompiendo los tubos, con ignición inmediata del etano/etileno liberado.
6. Corrosión o erosión interna redujo el espesor de un tubo o colector hasta que falló a alta temperatura y presión, liberando una nube de hidrocarburo que encontró una fuente de ignición en el propio horno.
7. Durante la decoquización, una alineación incorrecta de válvulas permitió el ingreso de hidrocarburo a una sección con aire caliente, formando una mezcla explosiva que detonó y dañó el horno, con liberación posterior de etileno.
8. Fatiga térmica por ciclos de arranque y parada generó grietas en los tubos del horno, que terminaron en una fuga a presión de etano/etileno y su ignición dentro del cajón de fuego.
9. La entrada de aire por fallos en sellos, mirillas o juntas del cajón de fuego creó una atmósfera inflamable con hidrocarburo fugado, y una chispa o superficie caliente provocó la explosión y el incendio.
10. Contaminantes en la alimentación, como azufre o cloruros, fragilizaron el metal de los tubos por ataque químico a alta temperatura, causando una fractura súbita y la consiguiente fuga e ignición.

### Lista R04-4b6bd6
1. Ruptura de un tubo del horno por sobrecalentamiento localizado causado por depósitos de coque en su interior: el coque aisló el metal, elevó la temperatura de pared hasta provocar fluencia y ruptura, y el gas de craqueo rico en etileno escapó al cajón de fuego donde se encendió.
2. Fuga de gas combustible en el manifold o en un quemador del horno: el gas se acumuló en el cajón de fuego, alcanzó una fuente de ignición y deflagró, dañando los tubos de proceso y liberando etileno.
3. Decoqueo mal controlado: la inyección de aire/vapor encontró hidrocarburos residuales y generó una reacción exotérmica fuera de control que sobrepresurizó y rompió el tubo, liberando etileno inflamable.
4. Pérdida súbita del flujo de etano o de vapor de dilución: los tubos quedaron sin refrigeración, se sobrecalentaron en segundos y fallaron, vertiendo gas de craqueo al interior del horno.
5. Impingement de llama por un quemador desalineado o bloqueado: una llama dirigida contra la pared del tubo creó un punto caliente extremo, adelgazó el metal y provocó la ruptura con fuga de etileno.
6. Obstrucción por coque en la línea de transferencia o en el intercambiador de calor aguas abajo: la restricción elevó la presión del proceso hasta reventar un tubo o cabezal, liberando etileno que se incendió.
7. Corrosión o erosión a alta temperatura en tubos o colectores: el espesor de pared se redujo progresivamente hasta que la presión de proceso provocó la ruptura y la salida de etileno.
8. Falla del lazo de control de temperatura o de la relación combustible/aire: el horno operó con sobrefuego generalizado, los tubos superaron su límite térmico y se rompieron, liberando hidrocarburos.
9. Falla de una brida o junta de expansión en la línea de gas de craqueo por fatiga térmica: la fuga de etileno a presión encontró una fuente de ignición cercana y originó la explosión y el incendio.
10. Deterioro del refractario que permitió el paso directo de gases calientes sobre los tubos: se creó un punto caliente no detectado que debilitó el metal hasta la ruptura y la liberación de etileno.

### Lista R04-71f5c7
1. Ruptura de un tubo de pirólisis por sobrecalentamiento localizado y coque: el coque adherido aisló el metal, elevó su temperatura hasta perder resistencia y, al reventar el tubo, el etano/etileno a presión escapó al cajón de combustión, donde se encendió y generó la explosión y el incendio.
2. Relación vapor/hidrocarburo insuficiente o pérdida de vapor de dilución: al reducirse el enfriamiento y la presión parcial, se favoreció el craqueo excesivo, la formación de carbón y una fuga inflamable que se autoencendió dentro del horno.
3. Falla en la secuencia de encendido de quemadores: se acumuló gas combustible en la cámara antes de la ignición y la deflagración resultante produjo una onda de sobrepresión que rompió componentes del horno y liberó la corriente de etileno.
4. Ingreso de aire por sellos, mirillas o refractario dañado: se formó una mezcla inflamable en la caja de fuego a alta temperatura, causando una explosión interna que se combinó con la fuga posterior de etileno.
5. Corrosión o erosión acelerada de tubos por azufre, cloruros o hidrógeno a alta temperatura: la pared metálica se adelgazó hasta fallar de forma súbita, liberando etileno a presión que se incendió de inmediato.
6. Fallo de termopares o del lazo de control de temperatura: el horno operó por encima del límite seguro sin alarma, degradando los tubos hasta su ruptura y la consiguiente liberación de etileno.
7. Error humano en arranque, parada o cambio de carga: una purga incompleta o válvulas mal alineadas dejaron hidrocarburo atrapado que, al calentarse sin dilución, alcanzó autoignición y detonó dentro del horno.
8. Falla de una brida, junta o colector de salida en la sección caliente: se produjo una fuga de etileno a alta presión que formó una nube inflamable; su ignición causó el incendio y la explosión reportada.
9. Oxidación de sulfuro de hierro pirofórico al abrir equipos durante mantenimiento: el contacto con aire generó calor suficiente para encender depósitos residuales, y esa ignición inició la fuga y el incendio de etileno.
10. Hipótesis poco convencional de sabotaje o ciberataque: una manipulación maliciosa de válvulas o del sistema de control llevó al horno a una condición de sobrepresión térmica que terminó en la ruptura y la explosión.

### Lista R04-69e849
1. El coque se acumuló dentro de los tubos radiantes y actuó como aislante, por lo que la temperatura del metal subió hasta sufrir deformación por creep y romperse. La rotura liberó etano y etileno a la caja de fuego caliente, que se inflamaron y explotaron provocando el incendio mayor.
2. Una soldadura con defecto de fabricación o reparación en el serpentín se fisuró por fatiga de ciclos térmicos de operación y decokings. La fisura creció hasta rotura súbita que derramó hidrocarburo a alta presión sobre los quemadores, generando la deflagración.
3. Durante un decoking con mezcla vapor-aire se admitió exceso de aire o se dejó hidrocarburo residual, creando una mezcla combustible dentro de los tubos y la caja. La combustión descontrolada del coque sobrepresurizó y reventó los tubos, liberando gases que explotaron.
4. Se interrumpió o redujo el caudal de etano y vapor de dilución por fallo de bomba, cierre inadvertido de válvula o error de control, dejando los tubos sin enfriamiento interno mientras los quemadores seguían a plena carga. El sobrecalentamiento elevó la presión interna hasta estallar un tubo e incendiar la carga liberada.
5. Varios quemadores se apagaron por perturbación del gas combustible y el gas sin quemar se acumuló en la zona radiante sin detectarse. Una reignición retardada o el contacto con un quemador vecino encendido provocó la explosión en la caja de fuego que dañó el horno.
6. Una brida, válvula o fuelle de expansión de la alimentación o efluente se degradó y fugó etano y etileno al exterior del horno formando una nube inflamable. La nube alcanzó los quemadores o una superficie caliente y deflagró, y el chorro de fuego posterior causó daños extensos.
7. A alta temperatura el carbono difundió en la aleación de los tubos y los fragilizó por carburización, reduciendo drásticamente su resistencia a la presión. Un pico normal de operación bastó para fisurarlos y liberar unas 5.100 libras de etileno que se quemó en el incendio.
8. Un trozo grande de coque desprendido taponó un codo en U del serpentín y bloqueó el paso mientras la alimentación seguía entrando, disparando la presión local. El tubo estalló por sobrepresión hidrodinámica y el escape a alta velocidad se auto-inflamó en la zona caliente.
9. Entró agua o condensado inadvertidamente al serpentín a más de 800 grados por una purga o válvula de decoking mal alineada y se vaporizó instantáneamente con expansión de más de mil veces. El golpe de vapor reventó el tubo y la carga liberada se encendió, causando la explosión sin víctimas graves por estar la zona despejada.
10. Un fallo poco común del sistema instrumentado de seguridad, por mala calibración de termopares, bypass de enclavamiento durante mantenimiento o interferencia externa como rayo o manipulación cibernética, impidió el corte de fuego ante una excursión térmica. El horno siguió calentándose sin protección hasta la rotura catastrófica, cuya onda expansiva fue contenida en gran parte por la estructura, lo que explica la ausencia de muertos pese a los 95 millones en daños.

## Caso R07
Elementos clave:
- e1: El polvo de hoja de moringa importado de India llegaba contaminado con la cepa del brote de Salmonella Typhimurium.
- e2: La bacteria sobrevivía dentro de las cápsulas hasta el consumidor.
- e3: El consumo enfermó a 34 personas en 14 estados.

### Lista R07-b2db92
1. Un proveedor entregó polvo de moringa crudo ya contaminado con Salmonella Typhimurium y MOGO lo usó sin un paso de esterilización letal en dos lotes de cápsulas; al enfermar consumidores, la FDA vinculó esos lotes al brote y la empresa los retiró voluntariamente.
2. La línea de molienda o encapsulado tenía un biofilm de Salmonella Typhimurium que no se eliminó con la limpieza rutinaria, de modo que solo los dos lotes procesados en esa corrida quedaron contaminados y motivaron el retiro acotado.
3. El agua utilizada para riego, lavado o humidificación de la moringa estaba contaminada con Salmonella Typhimurium y el procesamiento posterior no la eliminó, concentrando el patógeno en las cápsulas de los lotes afectados.
4. El secado de la moringa se hizo al aire libre y sin barreras sanitarias, permitiendo que aves, roedores o insectos depositaran Salmonella Typhimurium en la hoja, que luego se encapsuló sin tratamiento suficiente.
5. Un trabajador infectado o portador asintomático de Salmonella Typhimurium manipuló la moringa durante el envasado sin higiene de manos adecuada, contaminando únicamente los lotes de esa jornada.
6. Se usó estiércol no compostado como fertilizante en el cultivo de moringa, lo que introdujo Salmonella Typhimurium en las hojas; la falta de un paso de reducción microbiana antes de encapsular permitió que llegara al producto final.
7. Hubo contaminación cruzada en almacenamiento o transporte con otros productos agrícolas o alimentos crudos contaminados con Salmonella Typhimurium, y los dos lotes de moringa absorbieron o compartieron el patógeno.
8. El tratamiento térmico o la irradiación de descontaminación no se validó correctamente y dos lotes no recibieron la dosis letal, por lo que Salmonella Typhimurium sobrevivió en las cápsulas y causó el brote.
9. MOGO reincorporó polvo de moringa recuperado o finas de lotes anteriores no conformes, que estaban contaminados con Salmonella Typhimurium, y esa práctica contaminó solo los dos lotes retirados.
10. La contaminación de febrero por Salmonella Newport y Kentucky nunca se erradicó de la cadena de suministro de moringa y una introducción posterior de Typhimurium en una fuente o lote distinto generó un segundo brote diferenciado por serovar.

### Lista R07-45ff37
1. Polvo de moringa de una cosecha/importación específica de primavera 2026 se contaminó en cultivo con agua de riego contaminada con heces que contenía S. Typhimurium y, al encapsularse sin tratamiento microbicida validado, sobrevivió y causó el brote de mayo limitado a los dos lotes fabricados con esa materia prima.
2. Hojas de moringa secadas al sol directamente sobre suelo o lonas en la finca proveedora fueron contaminadas por excrementos de aves y roedores portadores de S. Typhimurium, y la ausencia de lavado y tratamiento térmico posterior permitió que el patógeno llegara viable a las cápsulas retiradas.
3. El fabricante utilizó para los dos lotes retirados materia prima de un proveedor nuevo o alternativo con deficientes prácticas agrícolas y sin análisis microbiológico, introduciendo S. Typhimurium de origen distinto al de los serotipos Newport y Kentucky del brote de febrero.
4. Limpieza deficiente de mezcladoras, tolvas y encapsuladoras compartidas transfirió S. Typhimurium desde otro producto botánico contaminado procesado previamente hacia solo los dos lotes de moringa procesados ese día, concentrando allí la contaminación.
5. Sacos porosos de polvo a granel almacenados en bodega húmeda con actividad de roedores fueron contaminados por orina y heces con S. Typhimurium, afectando únicamente a los sacos utilizados para fabricar los dos lotes retirados.
6. La decisión de mantener el producto como crudo/natural sin etapa letal validada como vapor o irradiación permitió la supervivencia de Salmonella ambiental de bajo nivel, explicando brotes repetidos con serotipos distintos según la flora de cada cosecha en febrero y mayo.
7. Distribución heterogénea de la contaminación en el polvo a granel hizo que solo fracciones usadas para dos lotes concentraran dosis infectiva detectable de S. Typhimurium, por lo que el retiro voluntario se limitó a esos lotes aunque el lote de materia prima tuviera contaminación intermitente.
8. Aplicación de estiércol sin compostar o abono orgánico contaminado con S. Typhimurium en la parcela cosechada para la producción de primavera introdujo un serotipo diferente al de febrero, que provenía de otra parcela o temporada con contaminación por Newport y Kentucky.
9. Contaminación post-proceso durante el envasado por manos de manipuladores portadores o por agua de limpieza contaminada con S. Typhimurium selló el patógeno dentro de los frascos de solo dos lotes envasados en un turno específico sin afectar a otros lotes.
10. Biopelículas persistentes de Salmonella en equipos con reintroducciones repetidas de polvo crudo diverso permitieron un recambio de cepas tras una limpieza parcial, predominando Newport y Kentucky en febrero y siendo reemplazadas por Typhimurium que contaminó los dos lotes de mayo.

### Lista R07-ebe4be
1. Contaminación agrícola en origen sin etapa letal: la moringa de esa cosecha se secó al aire libre sobre suelos abonados/regados con agua fecal con Salmonella Typhimurium y se encapsuló sin irradiación ni tratamiento con vapor, por lo que la bacteria sobrevivió meses en el polvo de baja actividad de agua y causó el brote de mayo, distinto al de febrero.
2. Contaminación cruzada en maquiladora compartida: la encapsuladora procesó justo antes un vegetal/polvo contaminado y una limpieza deficiente dejó residuos en tolva, dosificadora y conductos, por lo que solo los dos lotes siguientes de MOGO arrastraron Typhimurium.
3. Reservorio ambiental persistente en planta: un biofilm o polvo contaminado con Typhimurium en equipos, sistema de aspiración o HVAC se desprendió intermitentemente durante la producción de esos dos días, lo que explica la afectación limitada a dos lotes y un serotipo diferente al de febrero.
4. Contaminación post-fabricación en almacén/distribuidor: excrementos de roedores o aves, o una filtración de agua contaminada, mojaron las tarimas de esos dos lotes y la humedad permitió la migración de Typhimurium a través de sellos y frascos hacia las cápsulas.
5. Cambio encubierto de materia prima tras la crisis de febrero: para reponer inventario MOGO compró polvo barato de otro proveedor/región con mala higiene fecal, contaminado con Typhimurium, y lo usó exclusivamente para fabricar esos dos lotes.
6. Contaminación heterogénea más amplia con detección parcial: el lote madre de polvo tenía Typhimurium en focos de muy baja concentración y el muestreo limitado solo dio positivo en dos lotes, por lo que el retiro voluntario de dos lotes subestima el alcance real aunque la FDA sí lo vincula al brote.
7. Fallo del proceso por reclamo “crudo/natural”: MOGO eliminó o redujo el tratamiento térmico/irradiación para etiquetar el producto como raw y el secado a baja temperatura no alcanzó letalidad para Salmonella, permitiendo que Typhimurium sobreviviera solo en la producción reciente.
8. Sesgo de vigilancia con atribución errónea: tras el brote de febrero por Newport/Kentucky se interrogó más por moringa y se analizó más ese producto, por lo que un conglomerado comunitario de Typhimurium por pollo/huevo en consumidores de moringa fue ligado por coincidencia epidemiológica a las cápsulas.
9. Falsificación con envase MOGO: un actor externo rellenó cápsulas con moringa adulterada y contaminada y las vendió con códigos de lote MOGO copiados, por lo que MOGO retiró esos dos códigos aunque la contaminación nunca estuvo en su línea oficial.
10. Sabotaje intencional dirigido: una persona con acceso a la mezcladora o al producto terminado y a un cultivo de laboratorio inoculó deliberadamente Typhimurium en esos dos lotes por venganza o para dañar a la empresa tras la crisis de febrero.

### Lista R07-5874ba
1. Un lote concreto de hoja de moringa se contaminó en campo por riego con agua con heces animales o abonado con estiércol con Salmonella Typhimurium y, como el polvo se seca al sol y se encapsula en crudo sin etapa letal validada, la bacteria sobrevivió hasta el consumidor, lo que explica que solo los dos lotes fabricados con esa materia prima enfermaran y que sea un serotipo distinto al de febrero.
2. MOGO usó para esos dos lotes una cosecha, finca o proveedor importador distinto al implicado en el brote de febrero por Newport y Kentucky, por lo que se introdujo una flora fecal diferente con predominio de Typhimurium solo en mayo.
3. En la planta de molienda y encapsulado, que trabaja para varios clientes, hubo limpieza y sanitización deficientes y residuos de polvo contaminado con Typhimurium quedaron en molino, tolvas o dosificadoras, contaminando por contacto cruzado únicamente la corrida de esos dos lotes.
4. Se omitió o se aplicó con parámetros insuficientes el tratamiento de reducción microbiana habitual para botánicos, como vapor, calor seco o irradiación, en esos dos lotes por error operativo o ahorro de costes, permitiendo que Typhimurium viable llegara a la cápsula mientras otros lotes sí fueron tratados.
5. Excrementos de aves, roedores o insectos en el patio de secado, centro de acopio o bodega en origen contaminaron directamente los sacos de hoja correspondientes a esa partida, inoculando Typhimurium de forma puntual sin afectar al resto de la producción.
6. Los sacos de esa partida sufrieron rehumedecimiento por secado incompleto, condensación, lluvia o humedad en transporte marítimo y almacenamiento, lo que evitó la die-off bacteriana y permitió la supervivencia y multiplicación localizada de Typhimurium solo en el material usado para esos dos lotes.
7. En los equipos se había formado un biofilm persistente y la limpieza parcial tras el brote de febrero eliminó a Newport y Kentucky pero dejó el nicho, que fue recolonizado por una cepa ambiental de Typhimurium, produciendo un segundo brote con el mismo vehículo pero distinto serotipo.
8. Cosechadores o manipuladores portadores asintomáticos de Typhimurium, sin lavado de manos, guantes ni instalaciones sanitarias, contaminaron manualmente la hoja o el polvo durante la selección, molienda o encapsulado de esa corrida concreta.
9. Polvo sobrante, devuelto o fuera de especificación contaminado con Typhimurium se reincorporó como retrabajo solo a la mezcla de esos dos lotes para no desperdiciar material, concentrando la dosis infectiva únicamente en ellos.
10. No fue la moringa sino un excipiente, aglutinante, desecante o el material de envase usado solo para esos dos lotes lo que llegó contaminado con Typhimurium e inoculó las cápsulas, por lo que epidemiológicamente aparecieron ligadas a moringa aunque el origen fue un insumo secundario.

### Lista R07-37b06e
1. Un lote específico de hoja de moringa importada se contaminó en campo por riego o fertilización con estiércol con Salmonella Typhimurium y, como la molienda y el encapsulado no tienen un paso letal validado, la bacteria sobrevivió en el polvo seco solo en los dos lotes fabricados con esa materia prima.
2. Un biofilm de Salmonella Typhimurium persistente en un molino, mezcladora o encapsuladora mal higienizada contaminó por contacto únicamente los dos lotes que pasaron por ese equipo en esa ventana de producción, mientras otros lotes salieron de una línea limpia.
3. La moringa se secó de forma insuficiente y se almacenó húmeda en sacos en origen, lo que permitió que una contaminación fecal ambiental inicial baja de Typhimurium se multiplicara hasta dosis infectiva solo en la partida usada para esos dos lotes.
4. Hubo contaminación cruzada post-proceso por plagas o polvo ambiental, como excrementos de roedores y palomas o arrastre de una planta vecina de harinas animales, que introdujo Typhimurium al producto a granel justo antes de encapsular esos dos lotes.
5. Tras el brote de febrero por Newport y Kentucky, el fabricante cambió de finca o región proveedora e introdujo inadvertidamente una cepa endémica distinta de Typhimurium de la nueva zona, lo que explica que el vehículo se repita pero el serotipo sea diferente.
6. Un certificado de análisis falsificado o un muestreo insuficiente permitió que materia prima contaminada entrara como negativa y se usara solo en esos dos lotes, sin detectarse hasta que aparecieron los casos humanos.
7. Las cápsulas vacías o excipientes estaban contaminados con Typhimurium y no el polvo de moringa, pero al analizar solo el producto terminado se atribuyó erróneamente a la moringa y pareció una repetición del problema de febrero.
8. El brote es en parte un artefacto epidemiológico: consumidores de productos saludables comparten exposición a moringa sin que sea causal, y un hallazgo incidental de bajo nivel en dos lotes hizo que casos esporádicos de Typhimurium se agruparan como brote distinto del de febrero.
9. Se reprocesaron o reempacaron remanentes del retiro de febrero mezclados con polvo nuevo y la manipulación adicional en ambiente no controlado sembró una contaminación secundaria con Typhimurium distinta a la original solo en dos lotes reetiquetados.
10. Hubo adulteración intencional post-distribución, donde alguien inoculó un cultivo de Typhimurium en frascos de esos dos lotes en tienda o bodega para extorsión o sabotaje, generando casos agrupados que imitan un defecto de fábrica y forzaron el retiro limitado.

### Lista R07-611639
1. La moringa usada en los dos lotes se contaminó en origen con Salmonella Typhimurium, porque las hojas se regaron o secaron en contacto con agua no tratada o estiércol animal, y el encapsulado en frío no eliminó la bacteria; al confirmarse el patógeno, MOGO retiró esos lotes y la FDA abrió el brote.
2. Un proveedor entregó polvo de moringa contaminado con Salmonella Typhimurium y MOGO lo incorporó sin un paso validado de reducción microbiana, de modo que solo los dos lotes fabricados con ese polvo quedaron implicados en el retiro y en la investigación.
3. La planta de encapsulado tuvo una contaminación cruzada por limpieza insuficiente entre lotes, y Salmonella Typhimurium persistente en tolvas o utensilios pasó al producto de dos lotes consecutivos, lo que motivó su retiro voluntario y luego el vínculo con casos.
4. La contaminación ocurrió después del tratamiento térmico: el pulido, la manipulación o el envasado de las cápsulas se hizo con agua, manos o equipos contaminados con Salmonella Typhimurium, afectando solo a los dos lotes procesados en ese turno.
5. MOGO hizo pruebas de rutina y encontró Salmonella Typhimurium en dos lotes, por lo que los retiró voluntariamente el 25 de mayo; la FDA abrió la investigación el 27 de mayo al recibir aislados clínicos que coincidían genéticamente con esas cápsulas.
6. Un biofilm o reservorio ambiental de Salmonella Typhimurium en un secador, cinta transportadora o zona de molienda liberó células intermitentemente y contaminó de forma esporádica el polvo usado en los dos lotes retirados.
7. La FDA pudo aclarar que era un brote distinto del de febrero porque la secuenciación genómica mostró que Salmonella Typhimurium de mayo no emparentaba con Newport/Kentucky; esto indica una introducción independiente de Typhimurium en la cadena de moringa, no una persistencia del mismo foco.
8. Un trabajador infectado o una práctica manual antihigiénica en el área de encapsulado introdujo Salmonella Typhimurium en dos lotes, y la empresa los retiró al detectar el riesgo antes de que la FDA confirmara el brote.
9. El almacenamiento inadecuado de producto terminado, con humedad, plagas o derrames en bodega, permitió que Salmonella Typhimurium contaminara dos lotes ya fabricados, lo que explica que el retiro se limitara a esos lotes.
10. Una falla puntual en un paso de descontaminación —irradiación, pasteurización o vapor— en un solo turno permitió que Salmonella Typhimurium sobreviviera en la materia prima de dos lotes, mientras que los demás lotes quedaron fuera del retiro.

### Lista R07-0b8024
1. Contaminación de la materia prima: el polvo de moringa se secó o regó con agua contaminada por heces animales portadoras de Salmonella Typhimurium, y ese material se usó en los dos lotes retirados, desencadenando el brote.
2. Contaminación cruzada en la encapsuladora: una biopelícula de S. Typhimurium persistió en tolvas o cuchillas y solo contaminó las dos tandas fabricadas después de una limpieza incompleta o un cambio de proveedor.
3. Ingrediente excipiente contaminado: un aditivo o cápsula vegetal, como almidón de arroz, traía S. Typhimurium y al mezclarse con la moringa sembró la contaminación en los dos lotes vinculados.
4. Agua de proceso contaminada: el agua usada para lavar o acondicionar el polvo antes de encapsular contenía S. Typhimurium, introduciendo el patógeno en ambas tandas retiradas.
5. Vector en almacén: roedores o insectos infectados defecaron sobre sacos abiertos de moringa en el almacén e introdujeron S. Typhimurium en los dos lotes que luego se retiraron.
6. Sabotaje intencional: un empleado o visitante contaminó deliberadamente el polvo o las cápsulas con S. Typhimurium, lo que explicaría que solo dos lotes y un serovar distinto al brote previo se vean implicados.
7. Falso positivo por contaminación de laboratorio: el retiro se activó por una prueba de Salmonella contaminada en el propio laboratorio, mientras la FDA vinculó casos por epidemiología sin aislar la cepa del producto.
8. Cambio de serovar por transferencia horizontal: una cepa de Salmonella Newport o Kentucky ya presente en la moringa adquirió fagos o plásmidos que alteraron sus antígenos y la hicieron tipificarse como Typhimurium, creando un brote aparentemente nuevo desde el mismo nicho.
9. Lote de cápsulas compradas a terceros: MOGO envasó cápsulas genéricas adquiridas a un fabricante que usó moringa contaminada con S. Typhimurium, y solo dos lotes de envasado llevaron ese material.
10. Reacción cruzada en pruebas rápidas: un test detectó antígenos comunes de Salmonella y clasificó como Typhimurium un contaminante distinto, pero la FDA confirmó después el serovar real en los casos, generando la aparente distinción con el brote de febrero.

### Lista R07-2f114f
1. La hoja de moringa de la cosecha usada en esos dos lotes se contaminó en campo por riego con agua con heces o fertilizante orgánico que portaba Salmonella Typhimurium y el secado al sol no alcanzó temperatura letal, por lo que la bacteria sobrevivió en el polvo y causó el brote al encapsularse sin otro tratamiento.
2. MOGO usó temporalmente un proveedor u origen distinto y más barato para esos dos lotes sin validación microbiológica, y esa materia prima venía contaminada con Typhimurium, lo que explica que solo esos lotes enfermaran y que sea un serotipo distinto al brote de febrero por Newport y Kentucky.
3. Hubo un fallo puntual en la etapa de reducción microbiana (vapor, calor o irradiación) por avería o tiempo-temperatura insuficiente durante la fabricación de esos dos lotes, por lo que la carga basal de Salmonella que normalmente se eliminaba sobrevivió viable hasta las cápsulas.
4. Se formó un biofilm persistente de Salmonella Typhimurium en la tolva, mezcladora o encapsuladora que se desprendió durante esos días de producción, contaminando solo esos dos lotes antes de que una limpieza posterior lo redujera.
5. Hubo contaminación cruzada en línea compartida por residuos de otro polvo botánico o suplemento contaminado con Typhimurium que no se limpió entre productos, transfiriendo el patógeno a la moringa de esos dos lotes.
6. El granel o polvo de esos lotes se rehumedeció por almacenamiento o transporte cálido-húmedo y condensación en bodega, lo que permitió que una contaminación inicial baja de Typhimurium se multiplicara hasta dosis infectiva solo en esos lotes.
7. Un manipulador portador asintomático contaminó el granel o las cápsulas durante el llenado, pesaje o control de calidad de esos dos lotes por higiene de manos deficiente, introduciendo Typhimurium tras la etapa de descontaminación.
8. La planta reprocesó mermas, polvo de colectores o devoluciones contaminadas con Typhimurium y las mezcló al granel de esos dos lotes para no perder material, concentrando el patógeno solo en esa producción.
9. Hubo intrusión de plaga (roedores, aves o insectos) en la bodega de materia prima o producto terminado que excretó Salmonella Typhimurium sobre sacos abiertos correspondientes a esos lotes, sin afectar a producción anterior del brote de febrero.
10. El material de envase (frascos, tapas o bolsas a granel) almacenado en condiciones insalubres se contaminó con Typhimurium y transfirió la bacteria a las cápsulas durante el envasado de esos dos lotes, que luego enfermaron a los consumidores.

### Lista R07-bf64e1
1. La moringa en polvo de esos dos lotes se secó a baja temperatura y se encapsuló sin un paso validado de reducción microbiana, por lo que Salmonella Typhimurium presente en la materia prima sobrevivió y alcanzó dosis infectante; el brote de febrero correspondió a otra partida contaminada con Newport y Kentucky.
2. El agua de riego o de lavado de la planta de moringa estaba contaminada con heces portadoras de S. Typhimurium y sembró el patógeno en la cosecha usada solo en dos lotes, que luego no recibieron un tratamiento letal; los serovares de febrero provinieron de otra fuente hídrica o predio.
3. Una línea compartida que también procesaba ingredientes de origen animal contaminó por contacto cruzado únicamente los dos lotes de cápsulas fabricados en esa ventana de producción; el brote anterior se originó en otra línea o turno con Newport/Kentucky.
4. Un biofilm de S. Typhimurium persistió en grietas de la tolva o de la encapsuladora y liberó células de forma intermitente, de modo que solo los dos lotes procesados tras una limpieza insuficiente quedaron contaminados; la contaminación de febrero tuvo otro serovar y otro punto de la planta.
5. Un operario infectado o portador asintomático de S. Typhimurium manipuló la moringa o las cápsulas sin higiene de manos adecuada y sembró el patógeno en dos lotes; el brote de febrero por Newport/Kentucky se debió a otro manipulador o a una materia prima distinta.
6. MOGO recibió un lote de polvo de moringa de un proveedor nuevo que ya venía contaminado con S. Typhimurium; solo dos lotes de cápsulas usaron ese polvo y por eso solo esos se retiraron, mientras que el brote de febrero usó otro proveedor con Newport/Kentucky.
7. El contaminante no estaba en la moringa sino en un excipiente o en la cápsula de gelatina/vegetal o en un antiaglomerante que portaba S. Typhimurium; al mezclarse contaminó solo los dos lotes que emplearon ese componente, y el brote de febrero involucró otro insumo con otros serovares.
8. Tras un tratamiento térmico correcto, los dos lotes se recontaminaron con agua no potable usada para enfriar, lavar o acondicionar el producto, agua que contenía S. Typhimurium; el brote de febrero fue una falla independiente con Newport/Kentucky.
9. Un reservorio ambiental cercano a la planta, como heces de aves o reptiles, polvo de desechos o drenajes, liberó S. Typhimurium que entró a la zona de envasado y contaminó solo dos lotes; los serovares de febrero entraron por otra ruta o en otro momento.
10. Un acto intencional de sabotaje añadió un cultivo de S. Typhimurium a dos lotes de moringa, lo que explica que el retiro se limitara exactamente a esos lotes y que la FDA hallara un brote nuevo distinto del de febrero; los serovares previos fueron un evento separado.

### Lista R07-92d252
1. El polvo de moringa de esos dos lotes se contaminó en origen agrícola por riego con agua con heces animales y secado al sol sin etapa letal validada, por lo que Salmonella Typhimurium sobrevivió solo en la cosecha usada para esos lotes.
2. Hubo contaminación cruzada en la maquiladora que encapsula para varias marcas porque antes procesó otro botánico contaminado y la limpieza entre producciones fue deficiente, transfiriendo Typhimurium solo a los dos lotes siguientes de MOGO.
3. Falló el tratamiento de reducción microbiana aplicado a esos lotes porque el equipo de vapor o irradiación operó con carga excesiva o parámetros insuficientes que dejaron puntos fríos, permitiendo la supervivencia de Salmonella eliminada en otros lotes.
4. MOGO cambió temporalmente a un proveedor de moringa no validado y más barato que seca a cielo abierto con acceso de aves y roedores, introduciendo Typhimurium ausente en su materia prima habitual.
5. Los dos lotes se contaminaron después de encapsulados por una infestación de roedores o filtración de agua en la bodega del distribuidor, donde envases con sellos defectuosos permitieron el ingreso de Salmonella.
6. La fuente no fue el polvo de moringa sino las cápsulas vacías de gelatina de origen animal fabricadas con mala higiene, por lo que Typhimurium venía en la cubierta y el brote se atribuyó erróneamente a la moringa.
7. La planta tiene un nicho persistente de Salmonella por mala higiene y recibió materias primas distintas en febrero y mayo, lo que explica dos brotes ligados a moringa pero con serovares distintos Newport/Kentucky y luego Typhimurium.
8. La asociación es epidemiológicamente espuria porque tras el retiro del 25 de mayo hubo sesgo de recuerdo y secuenciación reforzada de casos, creando un clúster aparente de Typhimurium endémico no causado realmente por las cápsulas.
9. Hubo error o contaminación cruzada en el laboratorio de referencia donde los aislamientos clínicos o del producto se contaminaron con una cepa control de Typhimurium, generando un vínculo molecular falso con los dos lotes.
10. Hubo sabotaje o adulteración intencional donde un tercero inoculó deliberadamente un cultivo de Salmonella Typhimurium en esos dos lotes durante almacenamiento o distribución para perjudicar a MOGO, lo que explicaría un retiro tan limitado y un serovar distinto al de febrero.

### Lista R07-31b6db
1. La materia prima de hoja de moringa en polvo se contaminó con Salmonella Typhimurium en origen (secado al aire libre con heces de animales o aves) y, al no tener paso de letalidad, pasó viva a las cápsulas.
2. El polvo de moringa no recibió tratamiento validado de reducción microbiana (vapor, irradiación) antes del encapsulado, permitiendo que la Salmonella sobreviviera en el producto seco.
3. Contaminación en la planta de encapsulado por equipos o ambiente contaminados que afectó solo ciertos lotes, explicando el retiro limitado a dos lotes.
4. Un proveedor común de polvo de moringa contaminado abasteció a múltiples marcas, lo que explica brotes repetidos ligados a moringa con distintos serotipos.
5. Agua contaminada usada en el lavado o procesamiento de las hojas antes del secado introdujo Salmonella en el material.
6. La Salmonella persiste largo tiempo en alimentos de baja humedad, por lo que la contaminación inicial se mantuvo viable durante almacenamiento y distribución.
7. Controles de calidad y pruebas microbiológicas insuficientes del proveedor y del distribuidor no detectaron la contaminación antes de la venta.
8. Contaminación por roedores, aves o insectos en almacenes de materia prima en el país de origen.
9. Manipulación por trabajadores infectados con higiene deficiente durante cosecha, molienda o envasado.
10. Una cepa distinta (Typhimurium) en un nuevo lote de materia prima indica una nueva fuente de contaminación independiente del brote de febrero, no una continuación del mismo.

### Lista R07-4f8976
1. La moringa se secó al aire libre y el polvo de hojas se contaminó con Salmonella Typhimurium procedente de heces de animales o aves; como solo dos lotes usaron esa partida, MOGO retiró únicamente esos dos y la FDA los vinculó al brote nuevo.
2. La planta no validó adecuadamente el tratamiento térmico o de irradiación del polvo; una carga baja de S. Typhimurium sobrevivió en dos lotes, que al consumirse causaron casos y motivaron la investigación federal.
3. El agua no potable usada para lavar o acondicionar la moringa introdujo S. Typhimurium; esa agua se empleó solo en la tanda que originó los dos lotes retirados, mientras los demás lotes usaron agua tratada.
4. Un biofilm de S. Typhimurium se formó en una grieta del molino o encapsulador y liberó células de forma intermitente; la limpieza incompleta permitió que solo los dos lotes siguientes quedaran contaminados.
5. La encapsuladora arrastró residuos de un producto anterior contaminado con S. Typhimurium; como la limpieza entre lotes fue deficiente, solo los dos lotes de moringa procesados después recibieron la dosis infectante.
6. El proveedor de cápsulas vacías entregó un lote contaminado con S. Typhimurium; MOGO usó esas cápsulas solo en dos lotes de moringa, lo que explica el retiro selectivo y que la FDA abriera investigación por un brote nuevo.
7. Un excipiente o relleno distinto de la moringa estaba contaminado con S. Typhimurium; solo dos lotes de cápsulas usaron ese insumo, y por eso el brote de mayo resultó serológico y epidemiológicamente distinto del de febrero por Newport y Kentucky.
8. Roedores o insectos contaminaron con heces una zona del almacén de materia prima; el polvo de moringa tomado de esa franja se usó solo en dos lotes, que fueron los únicos positivos a S. Typhimurium.
9. Un operario portador asintomático de S. Typhimurium manipuló el polvo sin guantes durante el envasado; la siembra quedó limitada a los dos lotes que tocó, y la cepa coincidió con la del brote investigado.
10. Las muestras de esos dos lotes se contaminaron en el laboratorio con S. Typhimurium o hubo un falso positivo por reacción cruzada; la FDA investigó por casos clínicos, pero la diferencia con el brote de febrero se debería a un error de tipificación o a muestras mal manipuladas.

### Lista R07-137dce
1. Un lote de materia prima de moringa en polvo llegó contaminado con Salmonella Typhimurium desde el proveedor y se utilizó solo en los dos lotes retirados; por eso MOGO pudo acotar el retiro a esos lotes.
2. El procesamiento de la moringa no aplicó una esterilización suficiente (por ejemplo, irradiación o vapor) y permitió que Salmonella Typhimurium sobreviviera en una tanda con alta carga microbiana, que luego se envasó en los dos lotes retirados.
3. La línea de llenado y capsulado albergaba un biofilm o residuo persistente de Salmonella Typhimurium en zonas de difícil limpieza, lo que contaminó únicamente la producción correspondiente a esos dos lotes.
4. Un ingrediente menor de la formulación, como un excipiente, diluyente o la cápsula de gelatina, estaba contaminado con Salmonella Typhimurium y se incorporó solo a los dos lotes retirados.
5. El agua usada para lavar o procesar la moringa estaba contaminada con Salmonella Typhimurium, lo que introdujo el patógeno en la materia prima destinada a esos dos lotes.
6. Un trabajador infectado o portador asintomático manipuló la moringa o las cápsulas durante el envasado y transmitió Salmonella Typhimurium a los dos lotes.
7. La materia prima se contaminó en el campo por contacto con heces de animales, riego con agua no tratada o polvo contaminado, y esa partida contaminada se destinó exclusivamente a los dos lotes retirados.
8. Las cápsulas o la moringa en polvo se contaminaron de forma cruzada durante el transporte o almacenamiento junto a otro producto que contenía Salmonella Typhimurium, afectando solo a los dos lotes expuestos.
9. Una limpieza incompleta después de mantenimiento redistribuyó Salmonella Typhimurium desde zonas sucias hacia la línea de producto terminado, contaminando solo la campaña de los dos lotes retirados.
10. El brote de febrero por Salmonella Newport y Kentucky y este de mayo por Typhimurium reflejan dos eventos de contaminación independientes en la cadena de moringa, probablemente por un cambio de proveedor o de lote de materia prima entre ambos períodos.