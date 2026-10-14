"""Línea de comandos `abd-mind`."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel

from factory import __version__
from factory.config import Config, ConfigRol, cargar_config, ruta_config
from factory.engine.auditoria import auditoria_markdown
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import ErrorCaso
from factory.engine.store import Store
from factory.experiments.base import renderizar
from factory.experiments.registro import EXPERIMENTOS, EXPERIMENTOS_LLM
from factory.organ.rule_engine import cargar_reglas, directorio_reglas
from factory.transition.stochastic.llm_client import ClienteLLM, ErrorLLM

# Subcomandos documentados en docs/arquitectura que llegan en fases posteriores.
PENDIENTES: dict[str, str] = {}


class _Ping(BaseModel):
    ok: bool


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="abd-mind", description="Motor de razonamiento abductivo")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=Path, help="archivo de configuración (YAML)")
    sub = parser.add_subparsers(dest="comando", required=True)

    exp = sub.add_parser("experimento", help="ejecuta un experimento canónico")
    exp.add_argument(
        "nombre",
        choices=[*EXPERIMENTOS, *EXPERIMENTOS_LLM, "todos"],
        help="'todos' ejecuta los experimentos sin LLM",
    )
    exp.add_argument("--sin-cache", action="store_true", help="no reutilizar respuestas guardadas")

    sub.add_parser("modelos", help="lista los modelos del proveedor")
    doctor = sub.add_parser("doctor", help="valida configuración, reglas y acceso a los modelos")
    doctor.add_argument("--sin-red", action="store_true", help="no llamar a los modelos")

    casos = sub.add_parser("casos", help="lista los casos guardados")
    casos.add_argument("--estado", choices=["abierto", "cerrado"])
    auditoria = sub.add_parser("auditoria", help="historia completa de un caso")
    auditoria.add_argument("caso_id")
    auditoria.add_argument("--formato", choices=["markdown", "json"], default="markdown")

    serve = sub.add_parser("serve", help="servidor MCP para Hermes u otro cliente")
    serve.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    serve.add_argument("--host", default="127.0.0.1", help="solo HTTP")
    serve.add_argument("--port", type=int, default=8765, help="solo HTTP")

    for nombre, fase in PENDIENTES.items():
        sub.add_parser(nombre, help=f"no implementado: {fase}")
    return parser


def _cliente(config: Config, sin_cache: bool = False) -> ClienteLLM:
    if sin_cache:
        config = config.model_copy(update={"cache_dir": None})
    return ClienteLLM(config, max_llamadas=config.presupuestos.llamadas_por_caso)


def _experimento(args: argparse.Namespace) -> int:
    if args.nombre in EXPERIMENTOS_LLM:
        config = cargar_config(args.config)
        resultado = EXPERIMENTOS_LLM[args.nombre](config, _cliente(config, args.sin_cache))
        print(renderizar(resultado))
        return 0 if resultado.exito else 1

    nombres = list(EXPERIMENTOS) if args.nombre == "todos" else [args.nombre]
    exito = True
    for nombre in nombres:
        resultado = EXPERIMENTOS[nombre]()
        print(renderizar(resultado), end="\n\n")
        exito = exito and resultado.exito
    return 0 if exito else 1


def _modelos(args: argparse.Namespace) -> int:
    config = cargar_config(args.config)
    configurados = {m for r in _roles(config) for m in r.modelos()}
    for modelo in _cliente(config, sin_cache=True).listar_modelos():
        print(f"{'*' if modelo in configurados else ' '} {modelo}")
    print("\n* = usado en la configuración")
    return 0


def _casos(args: argparse.Namespace) -> int:
    config = cargar_config(args.config)
    store = Store(config.base_datos)
    try:
        servicio = ServicioCasos(store, config)
        if args.comando == "auditoria":
            auditoria = servicio.auditoria(args.caso_id)
            if args.formato == "json":
                print(auditoria.model_dump_json(indent=2))
            else:
                print(auditoria_markdown(auditoria))
            return 0
        casos = servicio.listar_casos(args.estado)
        if not casos:
            print(f"No hay casos en {config.base_datos}")
        for c in casos:
            h = c.resumen.h_estrella
            mejor = f"H*: {h.id_hipotesis} {h.mecanismo[:50]}" if h else "sin H*"
            print(
                f"{c.caso_id:<10} {c.estado:<8} {c.dominio:<10} "
                f"obs={c.resumen.n_observaciones} vivas={c.resumen.n_hipotesis_vivas} "
                f"{mejor} · {c.descripcion[:40]}"
            )
        return 0
    finally:
        store.cerrar()


def _serve(args: argparse.Namespace) -> int:
    from factory.interfaces.mcp_server import app_http, crear_servidor, token_de_entorno

    config = cargar_config(args.config)
    for aviso in config.avisos():
        print(f"aviso: {aviso}", file=sys.stderr)
    token = ""
    if args.transport == "http":
        try:
            token = token_de_entorno()
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2
    store = Store(config.base_datos)
    try:
        servidor = crear_servidor(ServicioCasos(store, config))
        if args.transport == "stdio":
            servidor.run("stdio")
        else:
            import uvicorn

            try:
                app = app_http(servidor, token, args.host)
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                return 2
            print(f"abd-mind MCP en http://{args.host}:{args.port}/mcp", file=sys.stderr)
            uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
        return 0
    finally:
        store.cerrar()


def _roles(config: Config) -> list[ConfigRol]:
    r = config.roles
    return [r.cortex, *r.generadores, r.verificador, *r.linea_base]


def _doctor(args: argparse.Namespace) -> int:
    ok = True
    ruta = args.config or ruta_config()
    print(f"Configuración: {ruta}")
    config = cargar_config(args.config)
    for aviso in config.avisos():
        print(f"  aviso: {aviso}")

    print(f"Reglas: {directorio_reglas()}")
    for archivo in sorted(directorio_reglas().glob("*.yaml")):
        try:
            reglas = cargar_reglas(archivo.stem)
            print(f"  {reglas.dominio} v{reglas.version}: {len(reglas.reglas)} reglas")
        except Exception as e:  # el doctor informa cualquier error de carga
            ok = False
            print(f"  ERROR {archivo.name}: {e}")

    if args.sin_red:
        return 0 if ok else 1

    cliente = _cliente(config, sin_cache=True)
    print(f"Proveedor: {config.proveedor.base_url}")
    roles = {
        "cortex": config.roles.cortex,
        "verificador": config.roles.verificador,
        **{f"generador {i}": g for i, g in enumerate(config.roles.generadores, 1)},
    }
    probados: set[str] = set()
    for nombre, rol in roles.items():
        for modelo in rol.modelos():
            etiqueta = nombre if modelo == rol.modelo else f"{nombre} (fallback)"
            if modelo in probados:
                print(f"  {etiqueta}: {modelo} (ya probado)")
                continue
            probados.add(modelo)
            prueba = rol.model_copy(update={"modelo": modelo, "fallback": None})
            try:
                cliente.completar_json(prueba, "Responde en JSON.", 'Devuelve {"ok": true}.', _Ping)
                print(f"  {etiqueta}: {modelo} OK")
            except ErrorLLM as e:
                ok = False
                print(f"  {etiqueta}: {modelo} ERROR {e}")
    return 0 if ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.comando in PENDIENTES:
        print(
            f"'{args.comando}' aún no está implementado: {PENDIENTES[args.comando]}.",
            file=sys.stderr,
        )
        return 2
    try:
        if args.comando == "experimento":
            return _experimento(args)
        if args.comando == "modelos":
            return _modelos(args)
        if args.comando in ("casos", "auditoria"):
            return _casos(args)
        if args.comando == "serve":
            return _serve(args)
        return _doctor(args)
    except ErrorLLM as e:
        print(f"Error del proveedor LLM: {e}", file=sys.stderr)
        return 1
    except ErrorCaso as e:
        print(f"Error ({e.codigo.value}): {e.mensaje}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
