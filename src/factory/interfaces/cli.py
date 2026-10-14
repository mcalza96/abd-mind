"""Línea de comandos `abd-mind`."""

import argparse
import sys
from collections.abc import Sequence

from factory import __version__
from factory.experiments.base import renderizar
from factory.experiments.registro import EXPERIMENTOS

# Subcomandos documentados en docs/arquitectura que llegan en fases posteriores.
PENDIENTES = {
    "serve": "fase 5 (servidor MCP)",
    "modelos": "fase 3 (roles LLM)",
    "doctor": "fase 3 (roles LLM)",
    "casos": "fase 4 (motor de casos)",
    "auditoria": "fase 4 (motor de casos)",
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="abd-mind", description="Motor de razonamiento abductivo")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)

    exp = sub.add_parser("experimento", help="ejecuta un experimento canónico")
    exp.add_argument("nombre", choices=[*EXPERIMENTOS, "todos"])

    for nombre, fase in PENDIENTES.items():
        sub.add_parser(nombre, help=f"no implementado: {fase}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.comando in PENDIENTES:
        print(
            f"'{args.comando}' aún no está implementado: {PENDIENTES[args.comando]}.",
            file=sys.stderr,
        )
        return 2

    nombres = list(EXPERIMENTOS) if args.nombre == "todos" else [args.nombre]
    exito = True
    for nombre in nombres:
        resultado = EXPERIMENTOS[nombre]()
        print(renderizar(resultado), end="\n\n")
        exito = exito and resultado.exito
    return 0 if exito else 1


if __name__ == "__main__":
    sys.exit(main())
