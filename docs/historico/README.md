# Histórico

Versiones anteriores del marco teórico, y todo lo del motor que se quitó el 2026-10-15 ([ADR-0017](arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)). **No son la referencia vigente** ([marco teórico](../marco-teorico/README.md)), pero se conservan porque registran la derivación y las decisiones, y porque el código del motor las citaba (`NN §x`; último commit con el motor: `44b51f694420cd3df004428e59c85fb000008c46`).

| Documento | Qué quedó vigente y dónde |
|---|---|
| 01 Problema y tesis | Reemplazado por la [tesis](../marco-teorico/tesis.md) |
| 02 Postulados | Reemplazado por los [principios](../marco-teorico/principios.md) |
| 03 Formalización, 04 Función objetivo, 09 Robustez, 11 Dominios abiertos, 12 Verdad, 13 Verificación comparativa | Resumidos en la [formalización](../marco-teorico/formalizacion.md) |
| 05 Experimentos canónicos | Siguen en el código (`experimentos`); su versión narrada es la [historia 1](../experimentos-mentales/01-el-cilindro.md) |
| 06 Arquitectura | Ver [arquitectura](arquitectura/README.md) |
| 07 Estado del arte | Desactualizado; lo reemplaza la investigación de literatura pendiente |
| 08 Decisiones y limitaciones | Las decisiones D1 a D21 siguen citadas en el código |
| 10 Caída de una acción | Lo retoma la [historia 6](../experimentos-mentales/06-la-accion-que-cae.md) |
| 14 Rumbo A + C | Superado por la [generación](../marco-teorico/generacion.md) |
| 15 Forma y material | Su versión estrecha es el [principio P6](../marco-teorico/principios.md#p6--contacto) |
| 16 Fundamentos | Resumido en los [principios](../marco-teorico/principios.md) |
| 17 Generación abductiva | Versión completa, con la evaluación externa. Lo vigente está en [generación](../marco-teorico/generacion.md) |

## Del motor (quitado el 2026-10-15)

| Carpeta | Contenido |
|---|---|
| [arquitectura/](arquitectura/README.md) | Arquitectura del motor, contrato MCP, despliegue, hoja de ruta y ADRs 0001–0017 |
| [hermes/](hermes/) | Skills anteriores (con MCP y de control), configuración de Hermes e instrucciones de la prueba A/B de EXP-017 |
