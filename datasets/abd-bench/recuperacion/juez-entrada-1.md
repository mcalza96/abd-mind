Eres un juez ciego. Para cada caso tienes los ELEMENTOS CLAVE del mecanismo documentado y varias LISTAS de explicaciones candidatas, identificadas con códigos (no sabes quién ni cómo las generó). Para cada candidata y cada elemento decide si la candidata lo cubre:
- "si": la candidata afirma ese mismo eslabón causal (puede usar otras palabras, pero el mecanismo concreto es el mismo).
- "parcial": apunta a la misma zona o pieza pero sin el eslabón concreto (p. ej. "falla en el sistema de control del elevador" frente a "el tapón suelto trabó el elevador").
- "no": no lo menciona, o afirma algo distinto.
Cubrir el tema no basta: se exige el eslabón causal. Juzga cada candidata por sí sola.

Responde SOLO con JSON: {"listas": [{"codigo": "...", "juicios": [{"pos": 1, "e1": "si|parcial|no", "e2": "..."}]}]}, con un juicio por candidata, en el orden de la lista.

## Caso R12
Elementos clave:
- e1: La válvula del regulador quedó entreabierta y acumuló presión de vapor en los cilindros.
- e2: El inversor estaba fuera de la posición que impide el arranque.
- e3: El freno de aire no estaba bien aplicado porque la dotación no había sido instruida en ese sistema.
- e4: La máquina partió sola con el operario en medio.

### Lista R12-81cb8a
1. El maquinista abrió accidentalmente el regulador al acomodarse en la cabina o al accionar un inyector, y la locomotora avanzó lentamente hacia la otra mientras el operario estaba entre ambas; por la baja velocidad y el espacio libre, no lo aplastó, pero lo obligó a caminar entre las máquinas en movimiento y lo dejó muy afectado.
2. El freno de mano estaba mal aplicado o su trinquete se soltó, de modo que al liberar la presión de vapor la locomotora rodó por la ligera pendiente del andén 1 hacia la unidad que estaban acoplando, atrapando momentáneamente al operario en el hueco.
3. Una fuga interna en el regulador o en la válvula de arranque dejó pasar vapor residual a los cilindros aunque el mando estuviera cerrado, provocando un movimiento no ordenado al quitar los frenos; el desplazamiento fue lento y no causó daños, pero sorprendió al operario entre las locomotoras.
4. Al desconectar las mangueras de freno de vacío durante la maniobra de enganche se perdió el vacío y los frenos se liberaron, permitiendo que la locomotora se desplazara hacia la otra y el operario quedara entre ambas.
5. La otra locomotora aún tenía inercia o recibió un empuje residual y se movió primero, golpeando a la unidad que estaban acoplando; el operario, situado en el espacio de acople, quedó atrapado y tuvo que caminar entre las dos máquinas.
6. Un miembro de la tripulación retiró los calzos de las ruedas antes de confirmar que el personal había despejado el espacio de acople, y la locomotora rodó por gravedad hacia la otra, provocando el casi-accidente.
7. El encargado del enganche hizo una señal manual ambigua o fuera del código establecido, y el maquinista la interpretó como autorización para acercarse, por lo que abrió vapor mientras el operario aún estaba entre las máquinas.
8. Un silbato o una señal acústica de otra maniobra en el patio se confundió con la orden de movimiento para esa locomotora, que arrancó sin que el operario lo esperara y lo obligó a caminar entre ambas.
9. Una herramienta o pieza suelta cayó sobre el mecanismo del regulador o la barra de cambio de marcha y abrió parcialmente el paso de vapor, haciendo que la locomotora se moviera sin orden durante el enganche.
10. El operario, al conectar el acople o las mangueras, accionó inadvertidamente una válvula de purga o desbloqueo que liberó los frenos de una de las locomotoras, y esta rodó lentamente hacia la otra.

### Lista R12-0a6e5d
1. Error de comunicación en la maniobra de acople: el maquinista de la locomotora que se movió interpretó una señal manual o verbal dirigida a otro punto como autorización para avanzar, por lo que abrió el regulador mientras el voluntario aún estaba entre ambas máquinas.
2. Freno de estacionamiento liberado inadvertidamente: al preparar el acople, alguien soltó el freno de la locomotora sin comprobar que el operario había salido de la vía, y la máquina rodó por la ligera pendiente de la plataforma 1 hasta casi aprisionarlo.
3. Fuga en el sistema de freno de vacío o aire: una pérdida progresiva de presión redujo la fuerza de frenado de la locomotora acoplada, que se desplazó lentamente sin orden mientras el operario caminaba entre ambas.
4. Regulador o válvula de arranque no cerrados del todo: vapor residual siguió entrando a los cilindros y provocó que la locomotora diera unas vueltas de rueda, movimiento que sorprendió al voluntario situado entre las dos.
5. Confusión por señales gestuales en un entorno ruidoso: entre vapor, multitud y distancia, un gesto de alto o de acercar fue leído al revés, y el maquinista movió la locomotora justo cuando el operario cruzaba entre ambas.
6. Falla del trinquete o freno de estacionamiento por vibración: el traqueteo continuo del vapor y del evento zafó el mecanismo que sujetaba la locomotora, que quedó libre y rodó unos centímetros hacia la otra.
7. Empuje residual de vapor atrapado en los cilindros: al abrir las purgas o girar las ruedas para alinear el acople, vapor condensado atrapado empujó las bielas y produjo un movimiento breve e inesperado.
8. Acción de un tercero no autorizado: un voluntario novato o un miembro del público manipuló el freno o el regulador por error o curiosidad, liberando la locomotora mientras el operario estaba entre ambas.
9. Transmisión de movimiento desde la otra locomotora: la máquina a la que se acoplaban se movió primero por una orden legítima y, a través del enganche o las varillas, empujó o tiró de la otra, cerrando el espacio entre ambas sobre el voluntario.
10. Microdesplazamiento por asentamiento térmico o estructural: cambios de temperatura y peso del público hicieron que la vía o la locomotora se asentaran o expandieran, liberando una tensión mecánica que impulsó la máquina unos centímetros sin intervención humana.

### Lista R12-4ed3d2
1. El maquinista recibió o creyó recibir una señal manual o verbal de movimiento que no correspondía a la maniobra de acople, por lo que abrió el regulador y la locomotora avanzó mientras el voluntario estaba entre ambas.
2. Los frenos de vacío o de aire se fueron soltando lentamente por una fuga en el sistema, y la ligera pendiente del andén 1 hizo que la locomotora se deslizara sin orden durante el acople.
3. Una válvula de regulador desgastada o mal cerrada permitió que vapor residual entrara a los cilindros y produjera un avance lento e inesperado mientras el operario trabajaba entre las máquinas.
4. La locomotora que se acoplaba llegó con exceso de velocidad o sin control y golpeó a la otra, transmitiendo el movimiento y cerrando el espacio entre ambas sobre el voluntario.
5. No se colocaron calzas ni se aseguró el freno de mano antes de que el voluntario entrara entre las máquinas, de modo que cualquier vibración o pequeño movimiento posterior lo obligó a caminar entre locomotoras en movimiento.
6. El maquinista o el enganchador olvidó momentáneamente que había una persona entre las máquinas y realizó un movimiento rutinario de ajuste para completar el acople.
7. En el bullicio del evento de aniversario, una voz o un gesto del público fue interpretado como orden de movimiento por la tripulación, que accionó la locomotora sin confirmación.
8. Un miembro de la tripulación o un visitante curioso accionó por error la palanca de freno o el regulador al subir o bajar de la cabina, provocando el movimiento no ordenado.
9. Una válvula de admisión o el mecanismo de distribución se atascó y admitió vapor a un cilindro aunque el regulador estuviera cerrado, causando un tirón o un avance por creep.
10. Alguien abrió deliberadamente una válvula o soltó el freno como broma o sabotaje en medio del evento, haciendo que la locomotora se moviera sin orden y casi atrapando al voluntario.

### Lista R12-0e035b
1. El maquinista confundió un gesto o grito del personal del andén con la orden de arrimar para acoplar y abrió el regulador mientras el operario ya estaba entre las locomotoras, porque no existía un protocolo de señal formal con confirmación visual.
2. La locomotora que se movió estaba detenida en ligera pendiente con solo el freno de mano aplicado y, por fuga del regulador y condensación en cilindros típica en máquinas de vapor en reposo, inició una deriva lenta hacia la otra justo cuando el operario entraba a enganchar.
3. El operario entró entre las dos locomotoras antes de que ambas estuvieran totalmente detenidas, aseguradas y con el maquinista avisado, por costumbre de agilizar el enganche durante el evento con alta presión de horarios y público.
4. El maquinista soltó el freno de vacío para hacer un último acercamiento milimétrico al enganche y calculó mal la distancia y el tiempo de frenado de una locomotora pesada, por lo que no pudo detenerla antes de cerrar el hueco donde estaba el operario.
5. El conductor era un voluntario poco habituado a esa locomotora concreta y accionó por error el inversor o el regulador en sentido contrario al intentar mantenerla quieta, provocando un arranque inesperado hacia la otra máquina.
6. La tripulación operaba bajo fatiga, calor y ruido del evento aniversario con comunicaciones gritadas, y el maquinista actuó por anticipación creyendo que el enganchador ya había salido del hueco porque perdió contacto visual momentáneo.
7. Una orden por radio o silbato destinada a la segunda locomotora o a otra maniobra en el andén 1 fue escuchada e interpretada como propia por el maquinista, que inició el movimiento sin confirmación directa con el enganchador.
8. Un fallo mecánico en el varillaje del regulador o en el enclavamiento del inversor hizo que, por vibración, saltara de punto muerto a marcha adelante con los frenos ya aflojados para la maniobra, iniciando el movimiento sin acción del maquinista.
9. El maquinista sufrió una indisposición transitoria por calor, deshidratación o distracción en cabina y apoyó o tiró involuntariamente del regulador, moviendo la locomotora sin ser consciente hasta ver al operario caminando entre máquinas.
10. Una tercera persona no autorizada, como visitante o voluntario inexperto subido a la cabina por el ambiente festivo, manipuló un mando o liberó el freno como travesura o por curiosidad, provocando el movimiento sin orden del maquinista titular.

### Lista R12-edf0f4
1. El maquinista interpretó mal una seña manual del personal del andén como orden de aproximación y avanzó lentamente hacia la otra locomotora mientras el operario colocaba el enganche entre ambas, obligándole a caminar entre máquinas en movimiento para no quedar atrapado.
2. La locomotora que se movió no tenía el freno de estacionamiento ni el freno de vapor/vacío suficientemente aplicado y rodó por gravedad por la ligera pendiente del andén 1 hacia la otra locomotora durante el acoplamiento.
3. El regulador quedó ligeramente entreabierto por cierre incompleto o desgaste y dejó pasar vapor residual a los cilindros, lo que provocó un avance lento e imprevisto sin orden de tracción justo cuando se hacía el acople.
4. El fogonero o maquinista aflojó los frenos anticipadamente para facilitar el acople por compresión de topes, permitiendo que la locomotora avanzara más de lo previsto con el operario aún en el espacio intermedio.
5. Hubo confusión sobre qué locomotora debía moverse al haber dos locomotoras en la maniobra, y el maquinista de la locomotora equivocada inició el movimiento creyendo que la orden de aproximación era para él.
6. La palanca de inversión quedó puesta en marcha adelante en lugar de en punto muerto, de modo que cualquier pequeña apertura o fuga del regulador se tradujo inmediatamente en movimiento hacia la otra máquina.
7. La comunicación por radio y señas entre jefe de maniobra, maquinista y personal de tierra falló por el ruido, el vapor y la aglomeración del evento aniversario, por lo que la orden de alto no llegó o llegó tarde y la locomotora siguió avanzando.
8. El operario entró entre las locomotoras antes de que ambas estuvieran completamente detenidas y aseguradas porque asumió que la aproximación había terminado, y en ese momento una de ellas aún realizaba el ajuste final para enganchar.
9. El maquinista no veía al operario entre las locomotoras por el vapor, la caldera y el ángulo de visión desde la cabina en el andén 1, y continuó el empuje suave para cerrar el enganche de tornillo sin saber que había una persona en medio.
10. La presión operativa del evento aniversario con horarios ajustados y voluntarios adicionales llevó a omitir el briefing y la confirmación de zona despejada antes de entrar entre vehículos, por lo que se ordenó o permitió el movimiento sin verificar que era seguro.

### Lista R12-e9e028
1. El acoplador hizo una seña manual o gesto para posicionarse que el maquinista interpretó erróneamente como orden de avanzar, por lo que abrió el regulador mientras el operario seguía entre las locomotoras y este tuvo que desplazarse caminando entre las máquinas en movimiento.
2. El maquinista liberó el freno de vacío antes de tiempo al creer que el acoplamiento ya había terminado, por lo que la locomotora rodó unos metros hacia la otra mientras el operario aún estaba entre los topes.
3. El regulador de la locomotora de vapor quedó слегка entreabierto o con fuga interna y dejó pasar vapor residual a los cilindros, lo que generó un arranque lento e imprevisto justo durante la maniobra de acople en el andén 1.
4. La vía del andén 1 tiene ligera pendiente y la locomotora quedó detenida solo con freno parcial sin calzas, por lo que se desplazó por gravedad hacia la segunda locomotora mientras se realizaba el enganche.
5. El maquinista mantuvo el inversor en marcha adelante con el regulador apenas abierto para el acercamiento final, por lo que la tracción residual mantuvo la locomotora en movimiento continuo en lugar de detenerse totalmente para el acople.
6. Por la presión del evento de aniversario con público y horario ajustado, la tripulación omitió el procedimiento de parada asegurada y confirmación verbal antes de permitir la entrada entre máquinas, por lo que el operario entró mientras la locomotora aún podía moverse.
7. Las mangueras de freno de vacío entre ambas locomotoras aún no estaban conectadas y el freno solo actuaba en una máquina, por lo que la capacidad de frenado fue insuficiente para mantener detenida la maniobra y se produjo el desplazamiento.
8. Una densa nube de vapor y humo en el andén redujo la visibilidad de la cabina, por lo que el maquinista no vio que el operario seguía entre las locomotoras y avanzó creyendo la zona despejada.
9. El freno de mano o freno de estacionamiento de la locomotora no retuvo por desgaste o mal ajuste, por lo que tras detenerse inicialmente la máquina volvió a rodar lentamente hacia la otra durante el acople.
10. Otro tripulante o visitante en la cabina movió accidentalmente la palanca del regulador o del inversor al desplazarse, por lo que la locomotora se puso en marcha sin orden del maquinista mientras se acoplaba.

### Lista R12-97aae3
1. El operario quedó entre las dos locomotoras porque, durante la acoplación, la máquina que debía permanecer inmóvil recibió una orden verbal ambigua o no autorizada y su maquinista la puso en movimiento; al estar el voluntario entre ambas para guiar el enganche, quedó atrapado en el hueco.
2. La locomotora se desplazó sin orden porque sus frenos de mano o de aire no estaban aplicados por completo y la pendiente o la inercia del andén 1 vencieron la resistencia, haciendo que avanzara lentamente hacia la otra mientras el operario estaba entre ellas.
3. Al soltar el freno de vacío o al cerrar el regulador, una fuga o acumulación de vapor generó empuje residual en los cilindros, lo que movió la locomotora unos centímetros sin que el maquinista diera avance, sorprendiendo al operario que trabajaba en el enganche.
4. El enganche se estaba realizando con una persona entre vehículos como práctica habitual de la línea; al no colocarse un tope o calzo que inmovilizara una de las locomotoras, cualquier movimiento imprevisto de la otra redujo el espacio hasta casi aplastar al voluntario.
5. La orden de mover se transmitió por radio o señas en un entorno ruidoso por el evento de aniversario, y el maquinista entendió 'adelante' cuando el señalero indicaba 'alto' o viceversa; el movimiento no ordenado atrapó al operario en la zona de acoplado.
6. El voluntario, con poca experiencia en maniobras de acoplado, se colocó entre las locomotoras para ajustar el enganche sin verificar que la otra máquina estuviera bloqueada, y el movimiento inesperado lo obligó a caminar entre ambas para no ser aplastado.
7. Una falla mecánica en la válvula de freno o en el mando del regulador permitió que la locomotora se moviera por sí sola al acumular presión, sin que la orden de movimiento hubiera sido dada, mientras el operario estaba en el espacio entre ambas.
8. La locomotora que se acoplaba recibió un golpe o empujón de otra unidad o del tren de coches al maniobrar, transmitiendo el movimiento a la máquina vecina; el operario quedó entre las dos al cerrarse el espacio.
9. La supervisión de la maniobra fue insuficiente durante el evento, de modo que no se verificó que el personal estuviera fuera de la zona de peligro antes de autorizar cualquier movimiento; el maquinista movió sin confirmar y el voluntario quedó entre las locomotoras.
10. La presión por cumplir el programa del aniversario llevó a acortar los tiempos de acoplado y a omitir el bloqueo reglamentario de la locomotora; al no asegurar la máquina, un movimiento no planificado la desplazó contra la otra con el operario en medio.

### Lista R12-72dc1a
1. Fallo de comunicación durante el acople: el maquinista de la locomotora que se movía interpretó una señal verbal o gestual como autorización para avanzar, aunque no se había dado la orden, y accionó el regulador mientras el voluntario estaba entre ambas máquinas; el voluntario tuvo que caminar con el movimiento para no quedar atrapado.
2. Freno de estacionamiento no aplicado o liberado por vibración: la locomotora que iba a recibir el enganche tenía su freno de mano parcialmente suelto, y la vibración o el propio empuje del acople lo liberó, haciendo que rodara lentamente hacia la otra justo cuando el operario estaba en el hueco.
3. Pérdida parcial de vacío en el freno: una fuga en la tubería de vacío o un mal cierre de la válvula del freno hizo que la locomotora perdiera fuerza de frenado y se desplazara sola por la pendiente del andén 1, sorprendiendo al voluntario entre ambas máquinas.
4. Regulador de vapor mal cerrado: la válvula reguladora no quedó completamente cerrada y el vapor residual en los cilindros hizo avanzar la locomotora unos centímetros sin orden del maquinista, atrapando al voluntario entre las dos máquinas.
5. Ruido del evento enmascaró las órdenes: el bullicio del aniversario y los silbatos impidieron que el maquinista oyera la contraorden de alto, por lo que creyó que la señal de acople seguía en pie y movió la locomotora mientras el operario ajustaba el enganche.
6. El voluntario entró antes de la confirmación de inmovilización: el procedimiento exigía calzar y confirmar ambas locomotoras antes de que alguien bajara al hueco, pero el operario se adelantó y un movimiento residual de la otra máquina por slack action lo dejó entre ambas.
7. Señal de maniobra mal alineada: un cambio de agujas o una señal luminosa en el andén 1 estaba dispuesta para otro movimiento, y el maquinista la interpretó como autorización para avanzar hacia la locomotora, iniciando el desplazamiento sin orden directa.
8. Interferencia o comunicación cruzada por radio: la radio del maquinista captó una orden destinada a otra maniobra o un canal compartido, y el maquinista la tomó como propia, moviendo la locomotora mientras el operario estaba acoplando.
9. Fallo en el inversor/reversa: la palanca de reversa quedó fuera de neutro o se movió por la vibración del motor, de modo que al abrirse ligeramente el regulador por una causa menor la locomotora se desplazó sin que el maquinista hubiera ordenado el movimiento.
10. Vandalismo o intervención no autorizada: alguien ajeno a la tripulación liberó el freno o accionó el regulador en la cabina mientras el personal estaba fuera, provocando que la locomotora se moviera sin orden hacia la otra y el voluntario quedara entre ambas.

### Lista R12-9e9cd1
1. El conductor interpretó mal una señal manual del acoplador debido al ruido y la multitud del evento, creyendo que le ordenaba avanzar para cerrar la distancia, por lo que abrió el regulador mientras el operario ya estaba entre las locomotoras.
2. La locomotora que se movía tenía el freno de vacío liberado para permitir el acoplamiento suave y quedó en ligera pendiente en el andén 1, por lo que rodó por gravedad hacia la otra sin tracción activa.
3. El regulador de vapor tenía una fuga interna que dejaba pasar vapor residual a los cilindros aun con la palanca cerrada, lo que produjo un avance lento e imprevisto justo durante el acoplamiento.
4. El conductor liberó los frenos y dejó la palanca de inversión engranada hacia adelante antes de tiempo para preparar el acople, de modo que cualquier pequeña apertura o vibración inició el movimiento sin orden explícita.
5. El voluntario entró entre las locomotoras antes de que ambas estuvieran detenidas y aseguradas, violando el procedimiento de no interponerse hasta confirmación de parada, por lo que una maniobra de aproximación final ordenada correctamente lo sorprendió en medio.
6. Hubo confusión de roles entre las dotaciones de las dos locomotoras del evento aniversario, y el conductor de la segunda máquina asumió que el otro frenaría la composición mientras él empujaba, provocando un movimiento coordinado pero no comunicado al operario de tierra.
7. Un fallo de comunicación por radio por interferencia o batería agotada hizo que la orden de alto del inspector no llegara al maquinista, que continuó la maniobra de aproximación para acoplar.
8. La distracción y fatiga del maquinista voluntario por la presión del público y el horario del evento aniversario le llevó a anticipar la orden y mover la locomotora creyendo que ya había recibido autorización.
9. Un resbalón o enganchón físico en cabina hizo que el conductor resbalara sobre el piso aceitoso o que su ropa se enganchara en la palanca del regulador al asomarse para ver la señal, abriéndola involuntariamente y provocando el avance.
10. Una intervención no autorizada durante la confusión del evento hizo que un visitante subiera momentáneamente a la cabina y tocara los mandos, o que una señal de silbato histórica usada en la recreación del aniversario fuera interpretada por la dotación como una orden moderna de marcha.

### Lista R12-b93b91
1. El maquinista interpretó erróneamente una señal manual o sonora como orden de avanzar para cerrar el hueco de acoplamiento y aplicó vapor mientras el operario ya estaba entre las locomotoras, porque no existía confirmación verbal por radio antes de moverse.
2. La locomotora tenía el regulador con una ligera fuga de vapor y los frenos liberados para la maniobra, por lo que avanzó lentamente por sí sola hacia la otra locomotora sin orden del maquinista justo cuando se realizaba el enganche.
3. La vía del andén 1 tiene una ligera pendiente hacia el punto de acoplamiento y la locomotora no estaba calzada ni con el freno de estacionamiento totalmente aplicado, por lo que rodó por gravedad y cerró el espacio donde estaba el operario.
4. El maquinista accionó por error el regulador o la palanca de inversión en sentido contrario al intentar ajustar la posición para el enganche, lo que provocó un avance imprevisto mientras el operario manipulaba el acoplamiento entre topes.
5. Se permitió que el operario entrara al espacio entre ambas locomotoras antes de que las dos estuvieran detenidas, frenadas y confirmadas como inmóviles, por lo que cualquier pequeño movimiento de aproximación lo dejó atrapado entre máquinas en movimiento.
6. La presión por cumplir el horario del evento de aniversario con público presente llevó a apresurar la maniobra y omitir la parada de seguridad y la orden explícita de no moverse a los maquinistas antes de autorizar la entrada al hueco.
7. El operario voluntario y/o el maquinista tenían formación o experiencia limitada en acoplamiento de locomotoras a vapor, por lo que el operario se colocó en la zona de atrapamiento y el maquinista no mantuvo vigilancia continua del hueco.
8. Por el ruido de la multitud y de las máquinas del evento y la falta de comunicación por radio, la orden de detenerse no fue escuchada o llegó tarde al maquinista, que continuó el movimiento lento de aproximación con el operario en medio.
9. Durante el acoplamiento las mangueras de freno de vacío/aire aún no estaban conectadas, por lo que se produjo una pérdida temporal de capacidad de frenado que impidió detener a tiempo el lento desplazamiento de aproximación.
10. La segunda locomotora, que se suponía fija, también se desplazó ligeramente por tener frenos liberados o por el tirón al tensar el enganche, por lo que el hueco se cerró por ambos lados y el operario tuvo que caminar entre dos máquinas en movimiento para evitar ser aplastado.

### Lista R12-843762
1. La locomotora quedó sin frenos aplicados o con el regulador parcialmente abierto mientras el operario estaba entre ambas para acoplar, y se movió sin orden por vapor residual o pendiente.
2. Fuga del regulador (válvula de admisión) que dejó pasar vapor a los cilindros aunque estaba cerrado, haciendo avanzar la locomotora durante el acople.
3. Falla de comunicación entre el maquinista y el operario de acople (señales mal entendidas en un evento concurrido) que llevó a mover la máquina con el operario entre ambas.
4. Freno de mano o de vacío no aplicado o liberado prematuramente en la locomotora detenida, permitiendo que rodara por la pendiente del andén.
5. Inversor (reversa) dejado en marcha en lugar de punto muerto, de modo que el vapor acumulado movió la máquina al abrirse el regulador o drenar.
6. Ausencia o incumplimiento de un procedimiento de protección (bloqueo de la locomotora antes de ingresar entre vehículos) que permitió la exposición del operario.
7. Distracción o presión de horarios en el evento de aniversario con más movimientos y personal voluntario menos experimentado, que redujo la verificación de seguridad.
8. Maquinista que operó los mandos creyendo que el acople ya estaba completo, moviendo la máquina mientras el operario aún estaba entre ellas.
9. Cilindros con condensado y vapor residual que al expandirse generaron movimiento inesperado al abrir las válvulas de drenaje.
10. Capacitación y supervisión insuficientes del voluntariado en tareas de acople de locomotoras a vapor.

### Lista R12-d72f1a
1. El freno de estacionamiento de la locomotora no estaba aplicado o se soltó antes de tiempo: al estar en una ligera pendiente del andén 1, la máquina rodó sin orden hacia la otra y el operario, que estaba entre ambas ajustando el enganche, tuvo que caminar entre las locomotoras en movimiento.
2. Una fuga de vapor por el regulador desgastado permitió que vapor residual llegara a los cilindros e hiciera avanzar lentamente la locomotora sin que nadie accionara el mando; el movimiento sorpresivo la acercó a la otra máquina con el operario aún en medio.
3. El maquinista interpretó una señal verbal o un gesto del personal de patio como la orden de acercar la locomotora, por lo que abrió el regulador mientras el operario seguía entre las dos máquinas comprobando el enganche.
4. La otra locomotora, al maniobrar para acoplarse, calculó mal la distancia o el impulso y golpeó a la primera antes de que el operario despejara la zona, transmitiéndole movimiento y obligándolo a caminar entre ambas.
5. Una pérdida de vacío o una válvula defectuosa en el sistema de frenos liberó la retención de la locomotora, que quedó libre y se desplazó por gravedad o por el desnivel del patio justo durante el enganche.
6. Faltaron calzos o cuñas en las ruedas y el freno de mano no era eficaz, de modo que la vibración del vapor o el propio empuje del enganche hicieron que la locomotora se moviera sin orden con el operario entre ella y la otra máquina.
7. El ruido, el vapor y la multitud del evento de aniversario impidieron que el maquinista oyera la señal de alto o viera al operario entre las máquinas; creyendo que el espacio estaba libre, movió la locomotora para completar el acople.
8. Un movimiento involuntario del maquinista o de un ayudante al subir o bajar de la cabina golpeó la palanca del regulador, provocando un arranque accidental de la locomotora mientras el operario trabajaba en el enganche.
9. El mecanismo de inversión o el varillaje de la locomotora se desplazó por vibración o desgaste y quedó en una posición que permitió que el vapor residual moviera las ruedas, haciendo que la máquina avanzara lentamente sin orden.
10. El enganche automático o la barra de acople estaba desalineado y, al intentar encajarlo, una de las locomotoras retrocedió o avanzó bruscamente para que las piezas coincidieran, atrapando momentáneamente al operario entre ambas.

### Lista R12-2c0062
1. El maquinista confundió una seña manual dirigida a la otra locomotora o un gesto del público con la orden de avanzar y abrió el regulador mientras el operario estaba entre los topes, obligándole a caminar entre las máquinas para no quedar aplastado.
2. La locomotora quedó sin freno de estacionamiento aplicado y sin vacío suficiente en el andén 1, que tiene ligera pendiente, por lo que venció la resistencia de rodadura y rodó por gravedad hacia la otra justo durante el acoplamiento.
3. El regulador de la locomotora de vapor tenía desgaste o fuga interna que dejó pasar vapor residual a los cilindros, lo que produjo un avance lento e inadvertido sin que el maquinista accionara ningún mando.
4. Por la presión del programa del aniversario se intentó acoplar sin detener totalmente la maniobra de aproximación para no perder tiempo, dejando deliberadamente al operario entre locomotoras en ligero movimiento para enganchar sobre la marcha.
5. El voluntario, con poca formación en maniobras de doble tracción, entró al hueco entre locomotoras antes de confirmar la parada total y la autorización, quedando expuesto cuando el maquinista hizo un pequeño ajuste final de posición.
6. El ruido ambiental del evento con multitud, silbatos y vapor impidió oír la orden verbal o de radio de alto, por lo que el maquinista prolongó la aproximación final más allá del punto de parada previsto.
7. El maquinista conducía una locomotora visitante traída para la gala con disposición distinta de regulador, freno e inversor, y accionó por error el regulador creyendo que aplicaba o mantenía el freno.
8. La palanca del inversor no quedó enclavada en punto muerto y por vibración engranó marcha adelante, de forma que al purgar cilindros la locomotora arrancó sin orden explícita de movimiento.
9. El maquinista sufrió un mareo momentáneo por calor, humo o monóxido en la cabina y al perder el equilibrio se apoyó sobre el regulador, abriéndolo involuntariamente durante el acoplamiento.
10. Un visitante o voluntario no autorizado aprovechó que la cabina estaba abierta y accesible por el evento y manipuló el regulador o liberó el freno por curiosidad, provocando el movimiento a espaldas del maquinista titular.

## Caso R09
Elementos clave:
- e1: El cabezal de la bomba se fabricó fuera de tolerancia y el enchufe entraba forzado.
- e2: El ajuste forzado abría los terminales y dejaba la conexión suelta.
- e3: La unión floja ofrecía alta resistencia y se calentaba hasta derretirse.
- e4: El sobrecalentamiento podía prender fuego aun con el auto apagado.

### Lista R09-7837c1
1. Un conector del arnés de cableado quedó mal asentado o crimpado en fábrica, lo que eleva la resistencia de contacto y genera calentamiento local hasta carbonizar el aislamiento y provocar un incendio incluso con el vehículo apagado; por eso se ordena estacionar fuera de garajes para que un eventual fuego no se propague a la vivienda.
2. El arnés roza contra un borde metálico del vano motor o del tablero por falta de una grapa o protector, y la vibración desgasta el aislamiento hasta exponer el conductor y producir un cortocircuito a masa con sobrecalentamiento e ignición.
3. Agua de lluvia o lavado se filtra a un conector eléctrico mal sellado, causando corrosión electrolítica, seguimiento superficial y arcos que inflaman el plástico; la orden de no guardarlo en garaje busca evitar que ese fuego quede confinado junto a materiales combustibles.
4. Un lote de terminales o cables de un proveedor salió con crimpado deficiente o aislamiento más delgado, creando puntos calientes por resistencia excesiva que terminan en incendio; como el lote se distribuyó a varias plantas, el alcance supera el mercado estadounidense.
5. Durante el ensamblaje, una herramienta o robot pinzó un cable de la instalación, dejando el conductor parcialmente roto; con el uso, el punto dañado arquea de forma intermitente y calienta el aislamiento hasta encenderlo.
6. La protección de circuito, fusible o relé, no despeja una falla de sobrecorriente porque está sobredimensionada o mal calibrada, así que el cable actúa como fusible, se sobrecalienta y prende fuego; estacionar afuera reduce el riesgo de incendio estructural.
7. Un módulo electrónico con lógica o software defectuoso mantiene energizado un circuito después de apagar el vehículo, y ese consumo parásito continuo recalienta un conector hasta generar humo o llama.
8. El cableado pasa demasiado cerca del exosto o de otro componente que alcanza alta temperatura, y el calor cíclico degrada el aislamiento hasta que se produce un cortocircuito y un incendio.
9. Roedores atraídos por el aislamiento de origen vegetal muerden el arnés, dejan conductores expuestos y provocan cortocircuitos; la recomendación de estacionar afuera podría reducir la acumulación de nidos y daños en el garaje, aunque es una hipótesis poco convencional.
10. Un ataque o exploit remoto de ciberseguridad podría activar repetidamente relés o calefactores eléctricos fuera de su ciclo normal, causando sobrecalentamiento del cableado y fuego; se trataría de una causa intencional o de software muy improbable frente a un defecto físico del arnés.

### Lista R09-fad267
1. El mazo de cables del tablero quedó enrutado contra un borde metálico afilado y con la vibración se desgastó el aislamiento hasta exponer cobre. Ese cortocircuito a masa puede generar calor e incendio incluso con el vehículo apagado, por eso se ordenó estacionar fuera.
2. Una sección del cableado del vano motor quedó demasiado próxima al escape o al turbo y el calor fundió el aislamiento. Los conductores expuestos entran en contacto y se sobrecalientan hasta arder, lo que justifica prohibir el garaje hasta revisarlo.
3. El conector principal de alimentación salió de fábrica con terminales flojos o mal crimpados que aumentan la resistencia de contacto. Esa resistencia produce arco y calentamiento progresivo capaz de inflamar plásticos cercanos aun estacionado.
4. Los clips de sujeción del arnés se aflojaron o rompieron por vibración propia del uso todoterreno y el cable suelto roza con piezas móviles o calientes. El pelado resultante provoca cortocircuitos intermitentes con riesgo de fuego.
5. Agua, lodo y sal entraron en un conector del compartimento motor mal sellado y causaron corrosión entre pines. Esa corrosión crea caminos conductivos que generan cortocircuito y calentamiento sin necesidad de tener el encendido puesto.
6. Durante el ensamblaje un tornillo o grapa pellizcó o perforó el aislamiento del arnés contra la carrocería. El punto dañado queda como fuga latente a masa que con humedad o movimiento deriva en arco e incendio.
7. Un lote del proveedor tenía cobre de sección menor o aislamiento más delgado de lo especificado y se calienta en exceso bajo carga normal. La degradación térmica termina en cortocircuito en una población muy amplia de vehículos.
8. El circuito de remolque y accesorios quedó protegido con un fusible de amperaje superior al que soporta el cable. Ante una sobrecarga no se funde el fusible sino que se sobrecalienta el cable hasta prender fuego.
9. Un relé o módulo defectuoso mantiene energizado el circuito afectado después de apagar el motor. Al no desenergizarse, un fallo menor puede evolucionar de noche hasta incendio en garaje.
10. Polvo, grasa u hojas acumuladas sobre un cable dañado o sobrecalentado actúan como yesca. Un punto caliente o chispazo menor prende ese material y convierte el fallo eléctrico en llama sostenida capaz de alcanzar la vivienda.

### Lista R09-4f1bdb
1. Rozadura del mazo principal del vano motor contra un borde metálico o soporte de la batería por clips de sujeción sueltos o rotos, que pela el aislamiento y provoca cortocircuito a masa con arco e incendio incluso con el vehículo apagado.
2. Entrada de agua, lodo y sal por un pasamuros del cortafuegos o conector del centro eléctrico mal sellado en uso todoterreno, que corroe los pines y genera calentamiento por alta resistencia y microarcos que carbonizan el conector.
3. Circuito permanentemente alimentado con calibre infradimensionado para su carga real, como la preinstalación de remolque o de accesorios, que se sobrecalienta con uso prolongado y funde el aislamiento hasta el cortocircuito.
4. Error de encaminamiento en línea de montaje en ciertos años-modelo que dejó el cableado apoyado sobre el turbo, colector de escape o EGR, degradando térmicamente el aislante hasta exponer el cobre.
5. Fatiga por vibración y torsión propia del chasis de largueros del Wrangler/Gladiator en el tramo entre chasis y carrocería, que fisura aislamientos y engarzados y produce arcos intermitentes que inician fuego.
6. Cambio de proveedor a conductores de aleación aluminio-cobre con engarzado deficiente, donde la corrosión galvánica eleva la resistencia del empalme y crea un punto caliente que derrite el aislamiento circundante.
7. Mazo de fábrica para winch, luces auxiliares e interruptores AUX dejado energizado con extremos sin sellar bajo el capó, que al tocar la carrocería o al conectar accesorios de terceros genera un corto directo de alta corriente.
8. Protección con fusible o relé sobredimensionado respecto al cable que debía proteger, por lo que un roce o sobrecarga no abre el fusible y permite un arco sostenido capaz de prender el aislamiento.
9. Daño por roedores atraídos por aislamientos de base vegetal que muerden los mazos estacionados en exteriores, dejando conductores expuestos que hacen cortos aleatorios difíciles de reproducir en taller.
10. Lote de aislamiento falsificado o fuera de especificación con plastificante barato e inflamable que no se autoextingue, convirtiendo una pequeña falla eléctrica contenible en un incendio que obligó a ordenar estacionar fuera.

### Lista R09-9e24c2
1. Un arnés de cableado mal enrutado roza contra un componente metálico o filo de la carrocería, se desgasta el aislante y produce un cortocircuito capaz de iniciar un incendio incluso con el vehículo apagado.
2. Un circuito alimentado permanentemente por la batería (no protegido por fusible adecuado) puede sobrecalentarse y causar incendio con el vehículo estacionado, de ahí la orden de dejarlo afuera.
3. Ingreso de agua o humedad en un conector o arnés que genera corrosión y resistencia alta, con calentamiento localizado y riesgo de fuego.
4. Conector eléctrico mal ensamblado o con terminales flojos que provoca arco eléctrico y sobrecalentamiento.
5. Falla en un módulo o componente eléctrico (por ejemplo calefactor, bomba o módulo de carrocería) que permanece energizado y sobrecalienta el cableado asociado.
6. Defecto de fabricación de un proveedor de arneses que afecta a una gran franja de producción común a Wrangler y Gladiator en varias plataformas y mercados.
7. Cableado cercano al escape o a fuentes de calor del motor que se degrada térmicamente hasta perder aislamiento y causar cortocircuito.
8. Fusible de calibre incorrecto o ausente en un circuito, que no interrumpe la corriente ante un cortocircuito y permite que el cable se incendie.
9. Daño al cableado por vibración y flexión en uso todoterreno, propio de estos vehículos, que acelera el desgaste del aislante.
10. Falta de una solución definitiva al momento del retiro, por lo que la orden de estacionar afuera es una medida provisional ante un riesgo de incendio aún no corregido.

### Lista R09-9bc518
1. Un terminal mal engastado en el conector del arnés que alimenta la dirección o el ventilador crea alta resistencia; al pasar corriente se calienta, carboniza el plástico y puede iniciar un incendio, de ahí la orden de estacionar fuera hasta revisar el cableado.
2. El sellado deficiente del conector permite entrada de agua y sales; la corrosión eleva la resistencia eléctrica y genera calor localizado hasta fundir el aislamiento y encender materiales cercanos.
3. Un fusible o relé con curva o capacidad incorrecta no despeja una falla de cortocircuito en el circuito auxiliar; el conductor se sobrecalienta y actúa como fusible, provocando ignición.
4. Un error de software en el módulo de control mantiene energizado el circuito de dirección o ventilador después de apagar el motor; el consumo continuo recalienta el arnés y crea riesgo térmico incluso con el vehículo estacionado.
5. La vibración normal del vehículo hace que el arnés roce una arista metálica o un soporte; con el tiempo se desgasta el aislamiento, se exponen conductores y un arco eléctrico enciende grasa o plásticos.
6. La ruta de un cable de alimentación queda demasiado cerca de una fuente caliente, como turbo, EGR o escape; el calor radiante degrada el aislamiento en ciclos térmicos y termina en cortocircuito.
7. Un lote de arneses usó aislamiento o terminales fuera de especificación, frágiles o de baja temperatura de fusión, y fallan antes bajo carga, elevando la probabilidad de incendio en los VIN afectados.
8. Restos metálicos o contaminantes conductores quedaron atrapados dentro de un conector durante el ensamble; migran con la vibración, crean un puente de baja resistencia y recalentamiento local.
9. Roedores atraídos por el recubrimiento de origen vegetal del arnés mastican el aislamiento, exponen conductores y generan cortocircuitos; la inspección del cableado y la orden de estacionar fuera buscan mitigar el riesgo de incendio mientras se descarta o confirma este daño no cubierto por garantía.
10. El mazo de cables sospechoso se comparte entre plantas de EE. UU., Canadá y mercados de exportación, por lo que un mismo defecto de proveedor explica que el alcance pase de 1.076.999 unidades en EE. UU. a más de 1,3 millones en el mundo y que la orden de no guardarlos en garajes se globalice.

### Lista R09-a20037
1. El mazo de cableado roza contra el bastidor por clips de sujeción insuficientes, el aislamiento se desgasta y un circuito siempre energizado hace cortocircuito a masa que genera calor e incendio incluso apagado, lo que obliga a estacionar afuera.
2. Un error de enrutamiento en fábrica dejó el cableado demasiado cerca del colector de escape, el calor funde el aislamiento y provoca cortocircuito e ignición, por eso se ordena no guardarlos en garaje hasta revisarlo.
3. Conectores del vano motor mal sellados permiten entrada de agua y sal de carretera, la corrosión crea caminos de fuga y arcos eléctricos que pueden iniciar fuego con el vehículo estacionado, motivando el estacionamiento en exterior.
4. Un cable de calibre insuficiente para la corriente de accesorios y remolque se sobrecalienta bajo carga sostenida, derrite su aislamiento y prende plásticos cercanos, lo que explica la revisión del cableado en más de un millón de unidades que comparten plataforma entre Wrangler y Gladiator.
5. Un lote de cables con aislamiento defectuoso del proveedor se agrieta prematuramente con vibración y temperatura, deja cobre expuesto que hace contacto y arde, afectando a ambos modelos del mismo periodo de producción en EE.UU. y el resto del mundo.
6. Durante el ensamblaje algunos mazos quedaron pellizcados entre piezas metálicas de carrocería y chasis, el daño latente perfora el aislamiento con el tiempo y causa cortocircuito directo a batería siempre viva que puede incendiar el Jeep aparcado.
7. Fijaciones flojas permiten que el cableado cuelgue y roce con partes móviles o el neumático, el desgaste abre el conductor y las chispas prenden grasa o revestimientos, por lo que se pide estacionar afuera lejos de estructuras.
8. Un relé o módulo de distribución defectuoso se queda pegado y mantiene energizado un circuito que debería cortarse al apagar, el calentamiento continuo del cableado eleva el riesgo de fuego nocturno en garaje.
9. Una protección con fusible sobredimensionado no interrumpe a tiempo una sobrecorriente por fallo parcial, el cable actúa como resistencia calefactora hasta fundirse e iniciar incendio, requiriendo inspección y corrección en toda la flota afectada.
10. La vibración extrema por uso todoterreno fractura empalmes y terminales flojos del mazo compartido por ambos modelos, el falso contacto genera arco y puntos calientes que pueden provocar combustión espontánea tras estacionar.

### Lista R09-ebf8c4
1. Un lote de arneses del compartimiento del motor salió de fábrica con un conector no sellado en el circuito de alimentación; la humedad y la sal entran, corroen los pines y crean una resistencia de contacto que calienta el plástico hasta encenderlo aun con el vehículo apagado. El retiro 26V363 inspecciona ese arnés en EE. UU. y en las demás plantas que usaron el mismo proveedor, y la orden de estacionar afuera busca que un incendio espontáneo no alcance una vivienda o garaje.
2. El mazo de cables que pasa junto al soporte del asiento trasero o al riel del chasis roza con el uso y la vibración hasta exponer el conductor; al quedar en contacto con metal desnudo se produce un cortocircuito que funde el aislamiento y puede iniciar fuego incluso en reposo. La campaña global agrupa a todos los Wrangler y Gladiator con ese trazado, no solo a los 1.076.999 de EE. UU.
3. Una actualización defectuosa del módulo de control de carrocería mantiene energizado un circuito auxiliar después de apagar el vehículo; el relé queda pegado o el software no corta la alimentación, y el conector asociado se sobrecalienta hasta carbonizarse. Por eso se pide no guardarlos en garajes: el evento térmico puede ocurrir horas después de estacionar.
4. Una manguera de refrigerante o de lavaparabrisas con abrazadera defectuosa gotea sobre un conector del arnés situado en el vano motor; el líquido iónico puentea pines y corroe terminales, generando un cortocircuito que puede encender el vehículo estacionado. Stellantis extiende el retiro a más de 1,3 millones de unidades porque el mismo tendido de mangueras y arneses se usa en varias plantas.
5. Un perno de masa de la carrocería quedó pintado o mal apretado en ensamblaje; la conexión deficiente eleva la resistencia, disipa calor en el punto de unión y puede encender el recubrimiento y los cables cercanos cuando circula corriente por luces, bomba o calefacción. La inspección del arnés incluye revisar y limpiar esas masas, y el alcance mundial refleja el mismo proceso de pintura.
6. El arnés pasa demasiado cerca del colector de escape o del catalizador y los ciclos térmicos degradan el aislamiento hasta que el conductor toca el metal caliente; la corriente de fuga o el contacto directo encienden plásticos y residuos de aceite. La orden de estacionar afuera responde a que el calor residual tras apagar puede iniciar el fuego, y el alcance mundial refleja que el trazado es idéntico en todas las versiones.
7. Un cable positivo de la batería auxiliar o del sistema de 48 V queda demasiado cerca de un borde metálico y, con el tiempo, la vibración corta el aislamiento; como la batería sigue conectada aunque el motor esté apagado, el cortocircuito puede soldar el metal y provocar incendio. La orden de estacionar afuera reduce el riesgo de que el fuego se propague a una estructura.
8. El arnés de las luces traseras o del remolque se fabricó con un pin invertido respecto al conector hembra; al activar una función, la corriente retorna por una masa no prevista y el mazo se recalienta hasta fundirse. El retiro cubre todos los vehículos con ese conector porque el error es de diseño del proveedor y no de una planta.
9. Virutas metálicas o restos de soldadura quedaron atrapados dentro de un conector durante el ensamblaje; esas partículas crean un puente intermitente entre pines, generan arcos y carbonizan el plástico, y el fallo puede aparecer mucho después de la entrega. La campaña global se explica porque el mismo proveedor armó los mazos para todas las plantas.
10. El aislante de los cables está formulado con material de origen vegetal que atrae a roedores; los animales roen el arnés estacionado, exponen conductores y provocan un cortocircuito que enciende el vehículo. Aunque es poco convencional, un retiro masivo por cableado obligaría a inspeccionar y encintar o reemplazar mazos, y la recomendación de no guardarlo en garaje también dificulta el acceso de roedores.

### Lista R09-e83df0
1. El mazo de cables bajo el tablero o junto a la columna de dirección quedó sin sujeción adecuada y roza con un borde metálico, la vibración pela el aislamiento y los hilos expuestos hacen cortocircuito a masa con chispa y calor capaz de iniciar fuego incluso aparcado, por eso se ordena estacionar fuera.
2. Un conector del vano motor mal sellado deja entrar agua, lodo y sal de carretera, la corrosión crea puentes conductivos entre pines que generan arco eléctrico y calentamiento sostenido que funde plásticos e inicia incendio.
3. Un terminal de alta corriente del alternador, arranque o batería quedó flojo o mal crimpado en fábrica, la alta resistencia de contacto produce calentamiento por efecto Joule que derrite el aislamiento vecino y prende fuego al compartimento.
4. Durante el montaje un tornillo, grapa o panel del salpicadero pellizcó o perforó el arnés, el daño latente progresa con calor y vibración hasta producir un cortocircuito franco entre alimentación y chasis.
5. La toma de masa principal al chasis quedó floja o se oxidó, la corriente de arranque busca retorno por cables finos de señal que no están dimensionados para ello y se sobrecalientan hasta incendiarse.
6. El circuito de remolque y accesorios aprobados como winch y luces auxiliares demanda más corriente de la que soporta el calibre instalado, el uso prolongado sobrecalienta el cable y funde su aislamiento provocando corto e ignición.
7. Un fallo de software o relé pegado en el módulo de carrocería mantiene energizado el arnés tras apagar el motor, la corriente continua sin protección efectiva recalienta el cableado parado en garaje.
8. Una celda defectuosa en la batería de 12V o en el paquete híbrido 4xe entra en fuga térmica, el calor degrada el cableado adyacente que arde y se reportó inicialmente como fallo de cableado generalizado.
9. El aislamiento ecológico a base de soja atrae a roedores que roen los cables cuando el Jeep está guardado, el cobre expuesto hace arco al siguiente arranque y el fuego resultante explica casos dispersos en garajes.
10. Un lote de arneses con cobre reciclado de sección reducida y aislamiento más inflamable, introducido por un subproveedor no autorizado, falla de forma aleatoria por sobretemperatura y no cumple la especificación original.

### Lista R09-21a79e
1. El mazo de cables del cuadro de instrumentos quedo enrutado muy tenso contra un soporte metalico en la linea comun de Toledo para Wrangler y Gladiator; la vibracion pelo el aislamiento del cable de alimentacion permanente y el arco a masa puede iniciar un incendio incluso con el vehiculo apagado, por eso se ordeno estacionar afuera.
2. El conector del modulo de ABS y control de estabilidad quedo mal sellado y permite entrada de agua y sal; la corrosion genera un cortocircuito interno en un circuito alimentado siempre a 12V que se sobrecalienta en el vano motor aun estacionado y puede prender fuego.
3. El cable positivo de bateria a motor de arranque perdio o rompio su grapa de fijacion y vibra contra el bloque o el escudo termico; el roce expone el cobre y provoca un cortocircuito directo de alta energia capaz de incendiar el vano motor incluso apagado.
4. El arnes de fabrica para remolque quedo largo y sin fijacion suficiente y roza con el tubo de escape trasero; el calor funde el aislamiento y une el positivo permanente a masa, provocando fuego en la zona trasera aun despues de estacionar.
5. La caja de distribucion electrica delantera tiene terminales con par de apriete insuficiente que crean alta resistencia de contacto; ese punto se calienta, funde plastico y arnes vecino y puede iniciar combustion latente con el vehiculo parado.
6. El arnes de puerta delantera, sometido a desmontajes frecuentes tipicos de Wrangler y Gladiator, quedo pellizcado en la bisagra y conector pasamuros; el dano expone cables de alimentacion permanente que hacen arco y generan foco de incendio en la puerta.
7. El cableado de la direccion asistida electro-hidraulica quedo rozando una arista del chasis comun JL/JT; la perdida de aislamiento permite fuga de corriente permanente con chispas y calentamiento del aceite y plasticos cercanos hasta el incendio.
8. El circuito base previsto para interruptores auxiliares off-road comparte calibre con accesorios de alto consumo como winch y barras LED; si el cliente los instala sin rele-fusible adicional el cable se sobrecarga, se derrite y puede arder incluso tras apagar por calor residual.
9. Un lote de cables con aislamiento mas delgado y sensible al calor del V6 Pentastar comun a ambos modelos se agrieta con temperatura y vibracion; los conductores expuestos se tocan entre si o a masa y el cortocircuito alimentado por bateria origina fuego en parado.
10. Una logica defectuosa del modulo de carroceria deja enclavado el rele de desempañador, espejos y asientos calefactados tras quitar el contacto; la alimentacion continua sobrecalienta conectores no dimensionados para servicio permanente y funde el arnes hasta incendiarse.

### Lista R09-54195f
1. El conector eléctrico de la bomba de dirección asistida presenta terminales con alta resistencia de contacto; esa resistencia eleva la temperatura local hasta fundir el conector y encender plásticos o residuos cercanos, por eso Stellantis ordenó estacionar fuera de garajes hasta revisar el cableado.
2. El sello del conector de la bomba de dirección es insuficiente y permite entrada de agua, sal o vapor; la corrosión resultante puentea pines y genera arcos eléctricos que carbonizan el conector y pueden iniciar un incendio.
3. El mazo de cables de la bomba de dirección roza contra un soporte metálico del vano motor; el roce desgasta el aislamiento, expone el conductor y produce un cortocircuito a masa que sobrecalienta el cableado hasta incendiar el vehículo.
4. El relé de la bomba de dirección queda pegado en posición cerrada; mantiene alimentación continua al motor eléctrico incluso con el vehículo apagado, lo que sobrecalienta el bobinado y el conector, originando fuego.
5. El módulo de control de dirección no corta la corriente al apagar el motor; sigue energizando el circuito de la bomba y genera calor sostenido en el conector, por lo que el riesgo persiste mientras el Jeep está estacionado.
6. Un fusible de calibre incorrecto o una protección térmica insuficiente no interrumpe la corriente ante una falla; el cableado actúa como fusible, se recalienta y enciende el aislamiento o el líquido de dirección.
7. El terminal de masa del motor o del chasis está corroído y eleva la resistencia del circuito de retorno; los cables cercanos se calientan en exceso y pueden inflamar aceite, grasa o plásticos acumulados en el vano motor.
8. Una fuga del líquido de dirección asistida cae sobre el conector eléctrico de la bomba; el fluido conductivo o los vapores inflamables provocan un cortocircuito y un incendio localizado que obliga a no guardar el vehículo en interiores.
9. Una actualización de software o una calibración de fábrica defectuosa permite que la bomba de dirección consuma corriente en reposo o funcione de forma intermitente; el consumo anómalo recalienta el conector y exige la revisión del cableado.
10. Instalaciones eléctricas no autorizadas, como luces auxiliares o cabrestantes, se conectan al mismo circuito de la bomba de dirección; la sobrecarga añadida funde el conector y aumenta el riesgo de incendio incluso en vehículos apagados.

### Lista R09-f6e9f9
1. El conector eléctrico de la bomba de dirección asistida presenta resistencia de contacto elevada por un terminal mal crimpado; eso lo sobrecalienta, funde su aislamiento y puede iniciar un incendio incluso con el vehículo apagado, por lo que se ordena estacionar afuera.
2. Un cable de alimentación principal de la batería roza contra el bastidor del vehículo hasta pelarse, creando un cortocircuito directo a masa que calienta el conductor y enciende el recubrimiento plástico.
3. El arnés del compartimiento del motor queda atrapado entre la tapa de válvulas y un soporte metálico, y la vibración perfora el aislamiento, provocando un cortocircuito que puede prender aceite o suciedad acumulada.
4. La terminal de masa de la carrocería está floja o corroída, lo que eleva la resistencia eléctrica y genera calor localizado en el punto de unión hasta carbonizar y encender el aislamiento cercano.
5. El conector del ventilador de refrigeración se degrada por ciclos térmicos y permite un arco eléctrico intermitente que funde el plástico del conector y puede propagar llama al mazo de cables.
6. El cableado del asiento eléctrico o calefactable se pinza con el riel del asiento al deslizarlo, y el cortocircuito resultante sobrecalienta el arnés bajo el asiento hasta inflamar la espuma o la alfombra.
7. El módulo de control de carrocería sufre una falla interna por soldadura fría que envía corriente excesiva a un circuito de baja capacidad, sobrecalentando el cableado asociado hasta provocar incendio.
8. El conector del remolque en Gladiator acumula agua y sal, se corroe y crea un puente resistivo entre pines de alimentación, lo que funde el arnés trasero y genera riesgo de fuego.
9. El conector del alternador se afloja por vibración y calor, permitiendo un arco eléctrico que inflama residuos de aceite o grasa acumulados en el bloque del motor.
10. Un lote de arneses de cableado fue fabricado con aislamiento de espesor insuficiente, de modo que el calor normal del motor lo degrada hasta exponer los conductores y causar cortocircuitos.

### Lista R09-06b0d1
1. El conector eléctrico de la bomba de dirección asistida acumula humedad y sal, sus terminales se corroen, aumenta la resistencia de contacto y el calor generado carboniza el aislamiento hasta provocar un incendio incluso con el vehículo apagado; por eso se ordena estacionar afuera y revisar el cableado.
2. Un sello defectuoso en el conector de la bomba de dirección asistida permite el ingreso de agua de lluvia o lavado, lo que causa un cortocircuito entre pines que genera arcos eléctricos y enciende el plástico del conector.
3. El relé de alimentación de la bomba de dirección asistida queda pegado en posición cerrada tras apagar el motor, manteniendo corriente continua en un conector ya degradado que se sobrecalienta y prende fuego.
4. El mazo de cables de la dirección asistida roza contra una arista metálica del soporte de la bomba, desgasta el aislamiento y produce un cortocircuito a masa que genera arco eléctrico e ignición del material aislante.
5. La exposición crónica al calor del múltiple de escape vuelve quebradizo el aislamiento del cableado cercano a la bomba, facilitando un contacto directo con metal caliente que inicia el fuego.
6. Una masa floja del circuito de la dirección asistida en el larguero del chasis eleva la resistencia del retorno de corriente y hace que el conector actúe como fusible térmico, derritiéndose y encendiendo residuos de aceite o grasa.
7. Un error de software en el módulo de control de potencia no corta la alimentación del circuito de la bomba al apagar el vehículo, dejando el conector energizado y vulnerable a sobrecalentamiento.
8. Un terminal hembra flojo dentro del conector de la bomba produce microfretting, arcos eléctricos intermitentes y carbonización progresiva que termina en ignición del conector.
9. La contaminación del arnés con aceite o líquido de frenos permite que un cortocircuito menor encuentre material inflamable y se propague como incendio en el compartimiento del motor.
10. Un diodo o componente electrónico dentro del módulo de la bomba falla en corto, provocando una corriente inversa que recalienta el cableado asociado hasta desencadenar el incendio.

### Lista R09-e3e86c
1. El mazo principal quedó ruteado tenso sobre una arista metálica del bastidor y con clips que permiten vibración, por lo que el aislante se desgasta con los kilómetros hasta exponer el cobre y generar un cortocircuito a masa capaz de prender fuego incluso con el vehículo apagado.
2. El cable de alimentación de batería y alternador pasa demasiado cerca del múltiple de escape sin pantalla térmica suficiente, por lo que el calor continuo reblandece y funde el aislante y los conductores hacen arco e incendian el vano motor.
3. El conector del panel de instrumentos y columna tiene un sellado insuficiente para uso todoterreno, por lo que agua y lodo entran y crean corrosión y puentes conductores entre pines que se calientan hasta ignición en estacionamiento.
4. Un perno de masa del chasis quedó con par insuficiente en fábrica, por lo que la unión de alta resistencia genera calentamiento y microarcos bajo carga que carbonizan el aislante vecino y pueden iniciar fuego.
5. Un relé de la caja de distribución de potencia tiende a soldarse en posición cerrada por arco interno, por lo que mantiene alimentado un circuito de alta corriente tras apagar el motor y el recalentamiento sostenido obliga a estacionar afuera.
6. El proveedor sustituyó el cobre especificado por cable de sección menor o aluminio cobreado, por lo que bajo carga normal el conductor supera su temperatura nominal y degrada el aislante hasta el cortocircuito.
7. Un error lógico del módulo de carrocería no desenergiza accesorios tras el apagado, por lo que una corriente parásita continua recalienta cableado y conectores durante horas en garaje hasta el riesgo de incendio.
8. El sub-mazo para remolque y accesorios se empalmó sin fusible dedicado del calibre correcto, por lo que un corto en ese ramal no funde la protección y el cable se comporta como resistencia calefactora hasta fundirse y arder.
9. El aislante de base vegetal usado en esos años atrae a roedores, por lo que en garajes muerden los mazos y dejan hilos expuestos que al tocarse generan chispas e incendio, lo que motiva la orden de dejarlos a la intemperie.
10. Un lote de fundas, cintas y conectores con material falsificado o degradado carece del retardante de llama exigido, por lo que un punto caliente o chispa mínima normal no se autoextingue y se propaga en incendio generalizado.

## Caso R13
Elementos clave:
- e1: La reparación del pandeo no liberó la tensión térmica del riel soldado.
- e2: El desalineamiento persistió con 93 °F sin inspección ese día.
- e3: La vía se abrió al pasar el tren.
- e4: Un acople con un vacío interno de fábrica se quebró y agravó el descarrilamiento.

### Lista R13-cffb9f
1. Pandeo térmico recurrente: el 1 de julio se enderezó la vía pero no se alivió la compresión del riel soldado continuo; el 6 de julio el calor expandió el acero y, al estar confinado sobre el puente, se produjo un desplazamiento lateral súbito que descarriló los vagones.
2. Balasto suelto tras el calzado: el balasto añadido el 1 de julio no tenía consolidación suficiente para confinar lateralmente los durmientes, por lo que bajo el paso del tren la vía perdió trocha y alineación hasta descarrilar.
3. Velocidad restablecida demasiado pronto: al levantar la restricción de 10 mph el 1 de julio, el tren circuló a 25 mph sobre una vía aún inestable; las cargas dinámicas laterales superaron la resistencia y provocaron el descarrilamiento.
4. Esfuerzos de expansión del tablero del puente: la reconstrucción del tablero en mayo pudo no dejar libertad térmica suficiente, de modo que el puente empujó lateralmente la vía en un extremo y desencadenó el descarrilamiento.
5. Falla de soldadura en riel soldado continuo: una soldadura defectuosa o tensionada durante el enderezado se agrietó bajo las cargas repetidas, fracturando el riel y desalineando la vía lo suficiente para descarrilar.
6. Sujeciones flojas o durmientes mal apoyados: la reconstrucción del puente en mayo pudo dejar fijaciones sin apriete o durmientes sin contacto, permitiendo que el riel se moviera lateralmente y se perdiera la trocha.
7. Geometría residual defectuosa: el enderezado del 1 de julio corrigió el pandeo visible pero dejó irregularidades verticales y laterales; al pasar las ruedas, una pestaña montó el riel y se inició el descarrilamiento.
8. Asentamiento diferencial en transición vía-puente: el relleno o balasto junto al tablero reconstruido no estaba compactado uniformemente, creando un escalón que golpeó las ruedas y desestabilizó la vía.
9. Fuerzas longitudinales por frenado o manejo: una frenada o aceleración sobre el puente generó compresión en los vagones y esfuerzos que empujaron la vía lateralmente, precipitando el descarrilamiento en el punto debilitado.
10. Falla del tanque DOT-111 tras el descarrilamiento: el impacto y el arrastre de los vagones descarrilados perforaron o rasgaron el tanque DOT-111, liberando los 10.500 galones de hidróxido de sodio.

### Lista R13-bd0e31
1. El enderezado y calce del 1 de julio no liberó la compresión térmica del riel soldado continuo sino que lo forzó a su posición, por lo que con el calor del 6 de julio el riel volvió a pandear lateralmente bajo el tren y descarriló 21 vagones con rotura del tanque DOT-111.
2. El levante y calce de balasto sobre el puente dejó la vía recién perturbada sin consolidar y con baja resistencia lateral, por lo que las fuerzas laterales del tren a 25 mph desplazaron el panel de vía y provocaron el descarrilamiento.
3. La reconstrucción del tablero en mayo de 2025 cambió el anclaje y la temperatura neutral del riel soldado continuo al instalar fijaciones nuevas sin adecuada liberación de tensiones, acumulando compresión que estalló como pandeo bajo la carga dinámica del 6 de julio.
4. Quedó un quiebre residual de alineamiento tras enderezar el pandeo del 26 de junio, y ese kink agudo elevó la relación L/V hasta producir escalada de pestaña y caída de ruedas sobre el puente aunque no hubiera pandeo nuevo.
5. El tablero reconstruido se asentó o aflojó en durmientes, largueros y tirafondos y generó alabeo y ensanchamiento de trocha sobre el puente, lo que permitió la caída de la rueda dentro del riel y el descarrilamiento en cadena con derrame de hidróxido de sodio.
6. Los ciclos de pandeo-enderezado fatigaron el riel o una soldadura aluminotérmica, y el 6 de julio se fracturó al paso del tren dejando una abertura que enganchó las pestañas y descarriló los vagones.
7. El contraste de rigidez entre la vía calzada y blanda sobre el puente y los accesos rígidos excitó balanceo armónico y hunting en vagones vacíos o ligeros, que oscilaron hasta salirse del riel a velocidad autorizada.
8. El descarrilamiento se inició por falla del material rodante, como cojinete sobrecalentado, rueda rota, eje quebrado o fuerzas longitudinales de compresión por frenado, y el daño a la vía y el derrame son consecuencia y no causa del pandeo previo.
9. El relleno del estribo o el drenaje alterado por la obra de mayo y el recale retuvo agua y creó un punto blando con defecto de nivel transversal al entrar al puente, provocando vuelco por balanceo y salida de los 21 vagones.
10. Como hipótesis poco convencional, la aspereza del 26 de junio no era pandeo térmico sino corrimiento incipiente de la estructura del puente o aflojamiento vandálico de fijaciones, y la reparación cosmética enmascaró la falla que colapsó el 6 de julio bajo el peso del tren.

### Lista R13-10e8e0
1. Recurrencia del pandeo por calor del riel soldado continuo sobre el puente la tarde del 6 de julio por compresion termica no liberada, que combó lateralmente la via bajo el tren y provoco el descarrilamiento de 21 vagones con rotura del tanque DOT-111.
2. Balasto recien calzado el 1 de julio sin consolidar ni estabilizar que dejo baja resistencia lateral, por lo que el trafico posterior aflojo la via y permitio su desplazamiento lateral bajo la carga del tren.
3. Enderezado del tramo pandeado sin cortar, liberar tensiones ni restablecer temperatura neutra, que dejo una deformacion residual que concentro esfuerzos y crecio con el calor hasta colapsar bajo el tren.
4. Interaccion adversa entre el riel soldado continuo y el tablero del puente reconstruido en mayo, cuya rigidez, anclaje o dilatacion diferentes concentraron los esfuerzos longitudinales sobre el puente y facilitaron la combadura.
5. Operacion hasta 25 mph tras levantar la restriccion de 10 mph sobre una via aun debil, cuyas mayores fuerzas dinamicas rueda-riel desencadenaron el pandeo dinamico y el descarrilamiento que a baja velocidad no se habria producido.
6. Falla o insuficiencia de fijaciones, durmientes, anclas y dispositivos contra dilatacion sobre el puente, que no contuvieron el movimiento longitudinal del riel por calor y permitieron un pandeo lateral subito.
7. Asentamiento diferencial del tablero reconstruido y de las calzas de balasto que genero defecto de nivel y trocha sobre el puente, provocando trepada de pestana o caida de rueda y el descarrilamiento en cascada.
8. Fractura de riel o de soldadura debilitada por el ciclo de pandeo de junio y enderezado de julio, que se rompio al paso del tren del 6 de julio, abrio la via y causo el descarrilamiento multiple y el derrame de hidroxido de sodio.
9. Defecto del material rodante como rueda agrietada, eje, rodamiento o bogie con caza inestable, que produjo el descarrilamiento sobre el puente de forma independiente al antecedente de via aspera del 26 de junio.
10. Movimiento estructural del puente como dilatacion de vigas, desplazamiento de apoyos o falla del tablero instalado en mayo, que deformo subitamente la geometria de la via bajo el tren y provoco el descarrilamiento y la perforacion del tanque.

### Lista R13-1603f3
1. El pandeo térmico reapareció porque la reparación del 1 de julio solo enderezó la vía y calzó balasto, sin aliviar las tensiones acumuladas del riel soldado continuo sobre el puente; el calor del 6 de julio volvió a expandir el riel y generó una desviación lateral que descarriló el tren.
2. El balasto recién calzado no alcanzó resistencia lateral suficiente antes de reabrir la vía, de modo que la carga del tren desplazó lateralmente la vía y provocó que las ruedas subieran por la pestaña del riel.
3. La reconstrucción del tablero en mayo de 2025 dejó una transición de rigidez o junta defectuosa en el puente; al paso del tren a 25 mph, esa discontinuidad amplificó las cargas dinámicas y deformó la vía hasta causar el descarrilamiento.
4. El riel soldado continuo carecía de anclajes o juntas de expansión adecuadas para el puente, por lo que la expansión térmica empujó longitudinalmente la vía y produjo un quiebre lateral en el momento del paso del tren.
5. Se levantó la restricción de 10 mph sin verificar completamente la geometría y las tensiones residuales tras el pandeo; un defecto remanente evolucionó durante los días siguientes y se manifestó como descarrilamiento el 6 de julio.
6. Una soldadura o grieta no detectada, originada por el pandeo previo o por la reconstrucción del puente, falló bajo el paso del tren; la rotura del riel guio las ruedas fuera de la vía y desencadenó el descarrilamiento.
7. El drenaje deficiente del tablero reconstruido retuvo agua y ablandó la base del balasto, permitiendo asentamientos diferenciales tras las variaciones térmicas; la geometría de la vía se degradó y el tren descarriló al pasar por el puente.
8. A 25 mph, la composición con tanques DOT-111 pesados y cargados de líquido generó balanceo y esfuerzos dinámicos que excedieron la resistencia lateral de la vía reparada, causando el desplazamiento de la vía y el descarrilamiento.
9. La interacción rueda-carril cambió por la rigidez del tablero reconstruido, favoreciendo hunting o desgaste irregular de la rueda; eso amplificó una irregularidad local y provocó que el tren descarrilara sobre el puente.
10. El programa de inspección entre el 1 y el 6 de julio no detectó una nueva deformación térmica o un asentamiento incipiente; cuando el tren llegó, la vía ya estaba fuera de tolerancia y el paso de los vagones consumó el descarrilamiento.

### Lista R13-ccce3b
1. Reaparición de un pandeo térmico en el riel soldado continuo: el enderezado y calzado del 1 de julio no confinó lateralmente el riel lo suficiente, y el calor del 6 de julio lo reexpansió sobre el puente formando un nuevo desplazamiento lateral que, al circular el tren a 25 mph tras levantarse la restricción, sacó las ruedas de la vía y provocó el descarrilamiento.
2. Reparación insuficiente y liberación prematura de la restricción: la cuadrilla alineó la vía pero no repuso la resistencia lateral del balasto ni verificó esfuerzos residuales, de modo que la primera circulación a velocidad autorizada generó cargas laterales que reabrieron el desalineamiento y descarrilaron los vagones.
3. Interacción riel-puente por el tablero reconstruido en mayo: el nuevo tablero modificó la rigidez y la expansión térmica del puente, acumulando esfuerzos longitudinales en el riel soldado continuo que se liberaron como un desplazamiento repentino de la vía al paso del tren, causando el descarrilamiento.
4. Defecto interno no detectado en el riel soldado continuo: una fisura o inclusión, agravada por el pandeo y el enderezado del 26 de junio al 1 de julio, se propagó hasta una rotura frágil bajo el tren el 6 de julio, creando una discontinuidad que guio las ruedas fuera de la vía y volcó los vagones.
5. Asentamiento diferencial del balasto nuevo: el calzado del 1 de julio se consolidó de forma desigual bajo las cargas, y el 6 de julio un punto blando en el puente cedió, generando un escalón o desnivel que provocó el descarrilamiento y la rotura del tanque DOT-111.
6. Falla de las fijaciones del riel al tablero: los clips o placas de anclaje instalados deficientemente en mayo se soltaron por vibración y ciclos térmicos, permitiendo que el riel se desplazara lateral o longitudinalmente sobre el puente hasta descarrilar al tren.
7. Daño previo en rueda o rodamiento por la vía áspera del 26 de junio: el paso por el pandeo a 10 mph pudo dañar un componente del vagón, que el 6 de julio falló en el puente, desalineando el eje y provocando el descarrilamiento en cadena.
8. Carga dinámica del hidróxido de sodio líquido: el tanque DOT-111 parcialmente lleno sufrió sloshing y transferencia de peso al circular a 25 mph sobre el puente, alterando la carga por eje y facilitando que el carro descarrilara y luego derramara 10.500 galones.
9. Movimiento no reportado de la infraestructura del puente: un microsismo, socavación o ajuste del estribo movió el tablero, alterando la geometría de la vía justo antes del paso del tren, de modo que la tripulación no tuvo tiempo de detectar la anomalía y se produjo el descarrilamiento.
10. Sabotaje o vandalismo: alguien pudo haber removido sujeciones, cortado parcialmente un riel o colocado un obstáculo después del 1 de julio, y el impacto del tren contra esa condición provocó el descarrilamiento y la perforación del tanque.

### Lista R13-a3850f
1. Pandeo térmico recurrente por reparación sin liberar tensiones: el 1 de julio solo se enderezó la vía y se calzó balasto sin cortar ni destensionar el riel soldado continuo, por lo que el calor de la tarde del 6 de julio volvió a generar compresión excesiva que pandeó lateralmente la vía sobre el puente bajo el tren y causó el descarrilamiento.
2. Pérdida de resistencia lateral por balasto recién alterado: el alineado y calzado del 1 de julio dejó el balasto suelto sin consolidar ni estabilizar, y al levantar la restricción a 25 mph las cargas dinámicas laterales del tren empujaron la vía marginalmente estable fuera de alineamiento sobre el puente.
3. Confinamiento anómalo por el tablero reconstruido en mayo de 2025: el tablero nuevo con fijaciones más rígidas creó un punto fijo que impidió la libre dilatación del riel soldado, concentrando los esfuerzos de compresión térmica justo en el tramo del puente donde ya había ocurrido el pandeo del 26 de junio.
4. Irregularidad residual de alineamiento y nivel transversal: el enderezado dejó durmientes colgados sobre calces y un defecto combinado de alineación y alabeo que a 25 mph provocó escalada de pestaña o balanceo armónico de los vagones y el descarrilamiento en cascada de 21 vagones.
5. Ensanchamiento de trocha por falla de fijaciones en el puente: los ciclos térmicos y el tráfico posterior a la reconstrucción aflojaron tirafondos, clips y anclas del tablero, permitiendo que bajo carga la trocha se abriera lo suficiente para que una rueda cayera dentro y descarrilara el tren perforando el frágil tanque DOT-111.
6. Falla mecánica del material rodante independiente de la vía: una rueda rota, un eje quemado o un equipo arrastrando en uno de los vagones delanteros descarriló sobre el puente y destruyó la vía a su paso, dando la apariencia de causa de vía y rompiendo el tanque de hidróxido de sodio.
7. Fuerzas longitudinales excesivas del tren: una maniobra de frenado o manejo de holgura generó un pico de compresión que pandeó lateralmente a vagones ligeros o vacíos sobre la alineación recién movida y débil del puente, produciendo un descarrilamiento por tijera que arrastró a 21 vagones.
8. Asentamiento diferencial del acceso al puente reconstruido: el relleno de aproximación removido en la obra de mayo se consolidó con el tráfico creando un bache de transición, cuya amplificación dinámica descargó ruedas a la entrada del puente y provocó el descarrilamiento por alabeo.
9. Rotura de riel o soldadura defectuosa de la obra de mayo: una soldadura aluminotérmica o fisura interna dejada en la reconstrucción progresó por fatiga bajo ciclos térmicos y falló súbitamente el 6 de julio, generando un escalón que enganchó una pestaña y descarriló el convoy.
10. Intervención externa o error de coordinación entre operadora O1 y dueña O2: robo o aflojamiento intencional de anclas y fijaciones tras el 1 de julio, o levantamiento indebido de la restricción de 10 mph sin verificar temperatura neutra ni resistencia lateral, dejó una vía aparentemente normal que colapsó con el calor vespertino al paso del tren pesado.

### Lista R13-f477d5
1. Recidiva del pandeo térmico por reparación sin liberar tensiones: el 1 de julio solo se enderezó y calzó la vía sin cortar ni destensionar el riel soldado continuo, por lo que el esfuerzo compresivo residual con el calor máximo de la tarde del 6 de julio volvió a pandear lateralmente la vía bajo el tren y provocó el descarrilamiento.
2. Pérdida de resistencia lateral por balasto removido sin consolidar: el calzado de balasto del 1 de julio dejó el balasto flojo y sin compactar sobre el puente, lo que redujo drásticamente la resistencia al pandeo y permitió un pandeo dinámico al paso de los vagones pesados aunque la temperatura no fuera extrema.
3. Defecto inducido por la reconstrucción del tablero de mayo de 2025: la obra modificó el anclaje, la fijación y la temperatura neutra del riel soldado sobre el puente y generó movimiento diferencial entre puente y riel, que se manifestó como vía áspera el 26 de junio y como inestabilidad final el 6 de julio.
4. Asentamiento diferencial y traviesas en el aire en el acceso al puente: el calce sin bateo ni compactación adecuada creó huecos bajo las traviesas que se asentaron con el tráfico, generando bacheo y alabeo severo que hizo trepar la pestaña de la rueda y descarrilar en cadena a los 21 vagones.
5. Ensanchamiento de trocha por fallo de sujeciones sobre el puente: tirafondos, clips o durmientes debilitados por la obra de mayo y por el pandeo previo perdieron capacidad de retención, por lo que el esfuerzo lateral de los carros tanque cargados abrió la trocha y dejó caer las ruedas dentro de la vía.
6. Rotura de riel o de soldadura debilitada por el evento previo: una fisura o soldadura dañada durante el pandeo del 26 de junio y forzada al re-alinearla el 1 de julio se fracturó súbitamente bajo carga térmica y dinámica el 6 de julio, creando una discontinuidad que descarriló al tren.
7. Falla originada en el material rodante y no en la vía: un rodamiento sobrecalentado y agarrotado, un eje roto o una rueda con pestaña crítica en uno de los primeros vagones descarriló primero sobre el puente y arrastró a los siguientes, rompiendo el tanque DOT-111 y derramando el hidróxido de sodio.
8. Fuerzas dinámicas excesivas por velocidad o manejo del tren: tras levantarse la restricción de 10 mph el tren habría circulado próximo o superior a 25 mph con frenado o balanceo armónico sobre el puente, amplificando la desalineación residual hasta producir el descarrilamiento masivo.
9. Colapso parcial de la estructura del puente recién reconstruido: el fallo de largueros, apoyos o conexiones del tablero nuevo bajo el peso de los tanques produjo una pérdida súbita de soporte y geometría de la vía que descarriló los vagones y perforó el tanque.
10. Evento externo o ambiental poco convencional confundido con pandeo por calor: vandalismo con aflojamiento de fijaciones, obstáculo colocado en la vía, micro-sismo o socavación por crecida que movió levemente el estribo del puente y generó una desalineación brusca justo al paso del tren del 6 de julio.

### Lista R13-244c05
1. El 1 de julio se enderezó el riel y se calzó balasto sin liberar las tensiones térmicas acumuladas en el riel soldado continuo; al recalentarse la vía el 6 de julio, el riel volvió a pandearse en el puente, desalineó la vía y provocó el descarrilamiento.
2. El riel soldado continuo sobre el puente carecía de juntas de expansión o anclajes capaces de absorber la dilatación; la compresión térmica del 6 de julio venció la resistencia lateral del balasto y desplazó la vía, guiando las ruedas fuera del riel.
3. El tablero del puente reconstruido en mayo de 2025 introdujo una rigidez o deflexión distinta a la del resto de la vía; bajo el paso del tren, la flexión diferencial del tablero hizo que la vía perdiera alineación y que las ruedas descendieran fuera del riel.
4. La restricción de 10 mph se levantó el 1 de julio antes de verificar la estabilidad de la reparación; al circular de nuevo a 25 mph, las fuerzas laterales del tren sobre la vía recién calzada abrieron la geometría y causaron el descarrilamiento.
5. El calzado de balasto del 1 de julio dejó vacíos o compactación desigual bajo los durmientes del puente; con las cargas repetidas, los durmientes se asentaron diferencialmente, se perdió el soporte lateral y la vía se deformó hasta descarrilar.
6. Las sujeciones o anclajes del riel al tablero no se rehabilitaron o torque-aron adecuadamente tras la reconstrucción de mayo; el riel pudo desplazarse longitudinal y lateralmente con la temperatura y las cargas, creando una alineación irregular en el puente.
7. Una fisura o soldadura defectuosa preexistente en el riel soldado continuo, agravada por el pandeo del 26 de junio, se propagó hasta fracturar el riel el 6 de julio; la fractura desalineó la vía y desencadenó el descarrilamiento.
8. El drenaje deficiente del tablero reconstruido o la contaminación del balasto permitieron erosión y pérdida de confinamiento lateral en el puente; la vía quedó sin resistencia suficiente para soportar el empuje térmico y las cargas del tren.
9. Un defecto en el tren, como una rueda desgastada, eje o suspensión, o una fuerza de caza anormal interactuó con la vía áspera del puente; el movimiento lateral resultante hizo que un vagón saliera del riel y arrastrara a los demás.
10. El tanque DOT-111 era estructuralmente vulnerable a perforación y volcamiento; al descarrilar y apilarse los vagones, el tanque fue golpeado y se rompió, liberando los 10.500 galones de hidróxido de sodio.

### Lista R13-74a3a6
1. El 1 de julio se enderezó la vía y se calzó balasto, pero no se liberó ni se ajustó la temperatura neutra del riel soldado continuo; al elevarse de nuevo la temperatura en los días siguientes, la compresión térmica residual provocó un nuevo pandeo lateral en el puente que hizo trepar las ruedas y descarrilar los vagones.
2. El apisonado de balasto del 1 de julio pudo dejar un hombro de balasto insuficiente o mal compactado, de modo que la vía no tuvo resistencia lateral suficiente para contrarrestar la compresión térmica del riel soldado continuo; el carril se desplazó transversalmente bajo el tren y se produjo el descarrilamiento.
3. La reconstrucción del tablero del puente en mayo de 2025 cambió la rigidez y las condiciones de expansión del riel soldado continuo, concentrando fuerzas térmicas longitudinales en la transición puente-terraplén; esa zona cedió lateralmente al paso del tren y originó el descarrilamiento.
4. Una soldadura defectuosa o una fisura interna preexistente en el riel soldado continuo, no detectada tras el pandeo del 26 de junio, se propagó por fatiga bajo cargas repetidas hasta fracturarse junto al puente; la rotura desalineó la vía y provocó el descarrilamiento.
5. La reconstrucción del tablero en mayo de 2025 pudo dejar una irregularidad vertical o de alineación en la entrada del puente que descargó dinámicamente las ruedas y excitó los bogies; el primer vagón descarriló por pérdida de contacto y arrastró al resto.
6. El tren pudo circular por encima de la máxima autorizada de 25 mph o con una manipulación de frenos que generó fuerzas de compresión y cabeceo superiores a las previstas; esas fuerzas dispararon el pandeo latente o el fallo del balasto y descarrilaron los vagones.
7. Un defecto de rueda, eje o truck en uno de los vagones, como una rueda plana o un rodamiento gripado, hizo que ese vehículo se saliera de la vía sobre el puente; la cadena de choques desprendió el tanque DOT-111 y derramó el hidróxido de sodio.
8. La carga de hidróxido de sodio en el tanque DOT-111 se desplazó lateralmente por falta de mamparos o por llenado parcial, creando una carga asimétrica que aumentó el balanceo y la tendencia al descarrilamiento al pasar por la vía del puente.
9. El tablero reconstruido o un apoyo del puente sufrió un movimiento lateral o un asentamiento bajo la carga del tren y la expansión térmica, desplazando la vía fuera de alineación y provocando que los vagones cayeran.
10. Alguien manipuló la vía o colocó un obstáculo en el puente después del levantamiento de la restricción el 1 de julio, causando el descarrilamiento; la fecha y el punto son compatibles con un acto intencional no detectado.

### Lista R13-a3d41d
1. El pandeo por calor del 26 de junio solo se enderezó y calzó sin cortar el riel ni restablecer su temperatura neutra, por lo que la compresión térmica residual hizo que el riel soldado continuo volviera a pandear lateralmente bajo el calor y el paso del tren del 6 de julio y descarriló los vagones.
2. El alineado del 1 de julio dejó un quiebre lateral residual sobre el puente y al levantarse la restricción a 25 mph las fuerzas laterales rueda-riel sobre ese kink provocaron trepada de pestaña o vuelco del riel que inició el descarrilamiento.
3. El calce de balasto sobre el puente con tablero reconstruido en mayo dejó un apoyo blando, sin compactación ni confinamiento lateral, por lo que bajo el tren se produjo asentamiento diferencial y alabeo que hizo oscilar la caja y descarrilar los vagones.
4. La reconstrucción del tablero de mayo alteró la fijación y el anclaje del riel soldado continuo en el puente y sus accesos, concentrando esfuerzos longitudinales y reduciendo la resistencia al pandeo lateral que colapsó con el tren encima.
5. La intervención del 1 de julio removió y recolocó la vía sin restablecer el par de sujeciones y el anclaje contra el corrimiento, lo que permitió ensanchamiento dinámico de la trocha y caída de ruedas dentro del riel sobre el puente.
6. El riel debilitado por el pandeo previo desarrolló una fisura o rotura en una soldadura bajo alta tensión térmica y flexión sobre el puente, y una rueda cayó en la discontinuidad provocando el descarrilamiento en cadena de 21 vagones.
7. El calzado del 1 de julio dejó una transición brusca de rigidez y nivel entre el terraplén y el puente reconstruido, generando un impacto vertical y rebote que descargó ruedas y produjo descarrilamiento por levantamiento a 25 mph.
8. La circulación a la máxima autorizada de 25 mph inmediatamente después de la reparación sin periodo de asentamiento ni levantamiento escalonado de la restricción amplificó dinámicamente un defecto geométrico menor hasta el colapso lateral de la vía.
9. Un defecto del material rodante como bogie desalineado, pestaña desgastada o carga desplazada interactuó con la irregularidad residual del puente y provocó el montaje de pestaña del primer vagón, que arrastró a los 20 siguientes.
10. El derrame de 10.500 galones se produjo porque el tanque DOT-111, de chapa delgada sin protección reforzada contra perforación, fue punzonado al impactar contra la estructura del puente o contra otro vagón durante el descarrilamiento iniciado por la vía.

### Lista R13-33a9bb
1. La vía de riel soldado continuo volvió a pandearse por calor el 6 de julio porque la reparación del 1 de julio no restituyó la temperatura neutra del riel ni la resistencia lateral del balasto, y el tren descarriló sobre la deformación.
2. El tablero del puente reconstruido en mayo dejó una transición rígida y balasto insuficiente o no consolidado, reduciendo la resistencia lateral y favoreciendo el pandeo térmico.
3. Al enderezar la vía se añadió o se reacomodó riel sin ajustar la tensión (destress), dejando el riel en compresión excesiva que se liberó con las altas temperaturas de julio.
4. Levantar la restricción de 10 mph antes de que el balasto recién colocado se consolidara permitió que el paso de trenes desestabilizara la vía y causara el descarrilamiento.
5. Anclaje deficiente del riel al tablero del puente (fijaciones, anclas anticorrimiento) que permitió el desplazamiento longitudinal del riel y su acumulación de esfuerzos en el puente.
6. Dinámica del tren (fuerzas de tracción o frenado, manejo del maquinista) sobre una vía con alineación marginal que provocó levantamiento o desplazamiento de vagones.
7. Inspección posterior a la reparación insuficiente que no detectó desalineación remanente o reaparición del defecto antes del 6 de julio.
8. Falla de un componente de vagón (rueda, eje, rodamiento) coincidente que inició el descarrilamiento en la zona del puente.
9. Diferencias térmicas entre la estructura del puente y la vía de aproximación que generaron esfuerzos concentrados en los extremos del puente.
10. El tanque DOT-111, de diseño menos resistente, se perforó en el descarrilamiento y liberó el hidróxido de sodio, agravando las consecuencias del evento.

### Lista R13-2fae74
1. El enderezado del 1 de julio sin cortar y destensionar el riel soldado continuo dejó compresión térmica residual, que con el calor del 6 de julio repandeó la vía bajo el tren y descarriló 21 vagones.
2. El calce de balasto sobre el puente sin compactación ni hombro suficiente dejó baja resistencia lateral, por lo que el esfuerzo lateral del tren desplazó la vía ya debilitada por el pandeo previo.
3. El levantamiento total de la restricción de 10 a 25 mph fue prematuro sobre una reparación temporal, y la mayor velocidad aumentó las fuerzas dinámicas que colapsaron la alineación inestable.
4. La reconstrucción del tablero del puente en mayo de 2025 alteró la interacción vía-puente, concentrando dilatación y esfuerzos longitudinales en el riel soldado justo donde luego pandeó.
5. La temperatura neutra del riel quedó demasiado baja tras la obra de mayo y el realineado de julio, por lo que el calor estival generó compresión excesiva y un sun-kink recurrente.
6. Fijaciones, anclas o clips insuficientes o deteriorados sobre el puente permitieron el corrimiento longitudinal y lateral del riel bajo carga térmica y del tren hasta salirse de gálibo.
7. El calzado creó un punto duro y asentamiento diferencial sobre el tablero rígido, generando impactos verticales que provocaron escalada de pestaña y el descarrilamiento inicial.
8. El enderezado dejó un defecto residual de alineamiento que actuó como irregularidad, amplificando el movimiento de lazo de los vagones cargados hasta descarrilar en cadena.
9. El tráfico repetido a 25 mph entre el 1 y el 6 de julio produjo un desplazamiento lateral progresivo de la vía calzada, que culminó en colapso súbito bajo el tren del 6 de julio.
10. Una causa iniciadora ajena a la vía, como defecto de rueda, rodamiento o freno de un vagón, coincidió con el punto débil del puente y el amontonamiento posterior perforó el tanque DOT-111 derramando el hidróxido de sodio.

### Lista R13-3e3731
1. El enderezado del 1 de julio no restauró la temperatura neutral del riel soldado continuo: al volver el calor, la vía recuperó compresión axial en el mismo tramo del puente y volvió a pandearse, desplazando lateralmente los rieles y guiando las ruedas fuera de la vía.
2. La reparación dejó el balasto suelto o poco compactado alrededor de los durmientes, de modo que al circular el tren a 25 mph la vía perdió resistencia lateral, se corrió de alineación sobre el tablero y provocó el descarrilamiento.
3. El pandeo del 26 de junio dañó un riel o una soldadura sin que se reemplazara, dejando una fisura o un kink residual que se propagó bajo las cargas repetidas hasta romperse o deformarse el 6 de julio.
4. La reconstrucción del tablero en mayo modificó la rigidez y las juntas de expansión del puente, y la expansión térmica del tablero empujó la vía fuera de alineación hasta superar la pestaña de las ruedas.
5. La restricción de 10 mph se levantó tras una verificación insuficiente, de modo que el tren circuló a 25 mph sobre una geometría aún inestable; la mayor fuerza lateral dinámica bastó para completar el desplazamiento lateral del riel.
6. Faltaban o quedaron flojas las sujeciones y grapas en el tramo reparado, permitiendo que el riel basculara o se abriera la trocha bajo la carga, con caída de ruedas al interior de la vía.
7. El drenaje del puente se obstruyó y las lluvias posteriores al 1 de julio saturaron el balasto, reduciendo su cohesión y provocando un asentamiento diferencial que desalineó la vía en el momento del paso del tren.
8. Un vagón con rodamiento, truck o rueda defectuosos generó un movimiento anómalo que inició el descarrilamiento, y el derrame de hidróxido de sodio ocurrió después al volcarse el tanque DOT-111.
9. La interacción dinámica entre el tren a 25 mph, el riel soldado continuo y el tablero reconstruido produjo vibraciones que fueron aflojando progresivamente el balasto y desplazando la vía hasta un fallo súbito.
10. Un acto de sabotaje —retiro de clips, colocación de un obstáculo o corte parcial de riel— después del 1 de julio creó una discontinuidad que descarriló el tren; el pandeo previo sería solo un factor de oportunidad.