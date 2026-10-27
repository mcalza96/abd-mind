# 2026-10-27 · web · carga inicial de /portafolio

- **Agente y skills usadas:** opencode (Muse Spark), abduccion + red-abductiva
- **Pregunta:** ¿podemos agilizar la carga del portafolio?

## Lo sorprendente

Lo que había que explicar no era "la página pesa" sino **dónde** pesa: `getPortfolio` ya resuelve la cartera en UNA query (`lib/portfolio.ts:130`, json_agg) y `getCloses` en otra sola con `ANY` — no había N+1. La explicación obvia ("trae muchos datos") predecía una query pesada y no se sostuvo al mirar el código. El costo estaba repartido: un viaje a Neon de más, JS monolítico y payload.

## Hipótesis

| Hipótesis | Familia | Qué predecía distinto | Resultado de la comprobación |
|---|---|---|---|
| Trae demasiados datos (obvia) | medición ingenua | una query pesada o N+1 en el armado | refutada: 1 query cartera + 1 query cierres |
| Solo lento en dev / cold-start de Neon | nada que explicar (azar/tasa base) | rápido en navegación blanda, lento en primera carga | no separada: sin RUM ni PORTAFOLIO_TIEMPOS=1 en prod |
| Doble lectura de sesión | un tercero común (viajes, no consulta) | `loading.tsx` suma sesion+versionesLegales en paralelo a la página | sobrevive: se eliminó el `getUser` del loading |
| Waterfall servidor | el tiempo (orden) | `cronometro` mostraría cierres >> cálculo; getUser bloquea todo | sobrevive parcial: cierres dependen de `touched`, no paralelizables del todo |
| JS monolítico + payload | el umbral | TTFB ok pero hidratación larga; `curvas` 20×120 al cliente | sobrevive: split + diezmo aplicados, medido en chunks |
| globals.css 192 KB + layout | el gemelo | TODAS las páginas lentas, no solo /portafolio | sobrevive: no tocado (candados 8/9), siguiente candidato |
| Suspense único bloquea todo | una decisión | nada progresivo hasta tener cierres+cálculo | sobrevive parcial: mitigado, streaming real requeriría refactor |

## Evidencia

- `npx tsc --noEmit`: limpio tras el cambio.
- `npm run build`: verde; `/portafolio` sigue `ƒ` (dinámica, con sesión) como corresponde.
- Tests: 1950/1957 pasan. Los 7 fallos (TIT-2, UI-46, COM-22/28/32, AD-5, CON-10) son del trabajo en curso del árbol: con mis 4 archivos en `stash` el resultado es idéntico (1950 pass / 7 fail).
- Split verificado en `.next/static/chunks`: `Registrar` real en chunk async de 12227 bytes (`reg-cargos` count 0 en el chunk inicial), `MovementsPanel` real en chunk async de 15414 bytes (`Caja libre` count 0 en el inicial). El chunk inicial de Dashboard solo conserva el label "Registrar un movimiento".
- `curvas`: constante `MAX_PTS = 60` en `app/portafolio/page.tsx` (~20×60 en vez de ~20×120).
- `cashByCcy`: `Map` → `Record<string, number>` en el borde servidor→cliente (4 archivos).

## Conclusión

Varias causas a la vez, con aportes estimados: −1 roundtrip a Neon por carga (loading estático), ~−27 KB minificado del JS inicial (split Movimientos, medido), ~−50% del payload de `curvas`. Confianza media-alta (0.75): verificado en build/chunks/tipos, no en tiempos de prod. Cambiaría la conclusión: si con `PORTAFOLIO_TIEMPOS=1` en prod `sesion+cartera+cierres` sigue >1 s, el cuello es cold-start de Neon, no frontend.

## Predicciones

P-20261027-01, P-20261027-02

## Lo que aprendí del método

La comprobación barata que más separó no fue medir tiempos sino leer el manifest del build (`.next/server/app/portafolio/page_client-reference-manifest.js`) y los chunks: distingue "código que viaja" de "código que existe" sin RUM. La skill no pide esa comprobación explícita; la familia "el umbral" la cubre pero sin decir cómo medirla. Nada nuevo para propuesta (una sola nota).
