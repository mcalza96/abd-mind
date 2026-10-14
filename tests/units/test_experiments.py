import pytest

from factory.experiments.registro import EXPERIMENTOS
from factory.interfaces.cli import main


@pytest.mark.parametrize("nombre", sorted(EXPERIMENTOS))
def test_experimento_exitoso(nombre: str) -> None:
    resultado = EXPERIMENTOS[nombre]()
    fallidas = [c.descripcion for c in resultado.comprobaciones if not c.ok]
    assert resultado.comprobaciones
    assert fallidas == []


def test_cli_experimentos(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["experimento", "todos"]) == 0
    salida = capsys.readouterr().out
    assert "Resultado: ÉXITO" in salida
    assert "FALLA" not in salida


def test_cli_subcomando_pendiente(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["serve"]) == 2
    assert "fase 5" in capsys.readouterr().err


def test_cli_doctor_sin_red(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["doctor", "--sin-red"]) == 0
    salida = capsys.readouterr().out
    assert "sintetico v3" in salida and "finanzas v2" in salida
