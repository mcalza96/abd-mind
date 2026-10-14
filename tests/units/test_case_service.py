import json
import re
from pathlib import Path

import pytest

from factory.config import ConfigPresupuestos
from factory.contracts.case import EstadoHipotesis
from factory.engine.auditoria import auditoria_markdown
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import CodigoError, EntradaHipotesis, EntradaObservador, ErrorCaso
from factory.engine.store import Store
from factory.experiments.finanzas import finanzas_llm
from tests.units.falsos import JSON, TransporteFalso, config_prueba


def _sistema_y_usuario(cuerpo: JSON) -> tuple[str, str]:
    if "messages" in cuerpo:
        mensajes = cuerpo["messages"]
        return mensajes[0]["content"], mensajes[1]["content"]
    return cuerpo["instructions"], cuerpo["input"][0]["content"]


def _cortex(usuario: str) -> str:
    texto = usuario.split("<<<")[1].split(">>>")[0]
    frases = [f.strip() for f in re.split(r"(?<=\.)\s+", texto.strip()) if f.strip()]
    hechos = [f for f in frases if "recomend" not in f.lower()]
    opiniones = [f for f in frases if "recomend" in f.lower()]
    return json.dumps(
        {
            "hechos": [{"enunciado": h, "variables": []} for h in hechos],
            "opiniones": opiniones,
            "dudas": [],
        }
    )


def _verificador(usuario: str) -> str:
    hipotesis = re.search(r"Hipótesis: (.*)", usuario)
    observacion = re.search(r"Observación: (.*)", usuario)
    assert hipotesis and observacion
    h, o = hipotesis.group(1).lower(), observacion.group(1).lower()
    if "precios" in h:
        explica = "precios de lista" not in o
    elif "demanda" in h:
        explica = "volumen" in o
    elif "costos" in h:
        explica = "margen" in o
    elif "mezcla" in h:
        explica = True
    else:
        explica = False
    relacion = "explica" if explica else "contradice"
    return json.dumps({"justificacion": "regla de prueba", "relacion": relacion})


def _generador() -> str:
    return json.dumps(
        {
            "hipotesis": [
                {
                    "mecanismo_latente": "Cambio en la mezcla de ventas hacia menor margen",
                    "entidades_latentes": ["cambio_de_mezcla"],
                    "afirmaciones": [{"variable": "tendencia_volumen", "valor": "alza"}],
                    "predicados_de_consistencia": [],
                    "observaciones_explicadas": [],
                }
            ]
        }
    )


def responder(ruta: str, cuerpo: JSON) -> str:
    sistema, usuario = _sistema_y_usuario(cuerpo)
    if "córtex perceptivo" in sistema:
        return _cortex(usuario)
    if "verificador independiente" in sistema:
        return _verificador(usuario)
    if "generador de hipótesis" in sistema:
        return _generador()
    raise AssertionError(f"petición inesperada: {sistema[:60]}")


@pytest.fixture
def transporte() -> TransporteFalso:
    return TransporteFalso(responder)


def _servicio(ruta: Path | str, transporte: TransporteFalso, **presupuestos: int) -> ServicioCasos:
    config = config_prueba(
        presupuestos=ConfigPresupuestos(**presupuestos) if presupuestos else ConfigPresupuestos()
    )
    return ServicioCasos(Store(ruta), config, transporte=transporte)


def _vista(nombre: str, vista: str) -> EntradaObservador:
    return EntradaObservador(nombre=nombre, marco=f"vista {vista}", parametros={"vista": vista})


def _solido(solido: str) -> EntradaHipotesis:
    return EntradaHipotesis(
        mecanismo=f"Es un {solido}", afirmaciones={"solido": solido, "dimension": 3}
    )


def test_caso_sintetico_persiste_y_se_reconstruye(
    tmp_path: Path, transporte: TransporteFalso
) -> None:
    ruta = tmp_path / "casos.db"
    servicio = _servicio(ruta, transporte)
    caso = servicio.crear_caso("¿Qué objeto es?", "sintetico").caso_id
    assert caso == "caso_1"
    servicio.agregar_observacion(
        caso, _vista("Frontal", "frontal"), "rectángulo", valor="rectangulo"
    )
    servicio.agregar_observacion(caso, _vista("Cenital", "cenital"), "círculo", valor="circulo")
    ids = [
        h.id_hipotesis
        for h in servicio.proponer_hipotesis(
            caso, [_solido("esfera"), _solido("cilindro")], origen="usuario"
        ).hipotesis
    ]
    assert ids == ["h1", "h2"]
    mejor = servicio.mejor_explicacion(caso)
    assert mejor.h_estrella is not None and mejor.h_estrella.id_hipotesis == "h2"
    assert transporte.llamadas == []  # dominio con proyección: ni córtex ni verificador LLM

    # Otra instancia sobre el mismo archivo ve el mismo estado.
    reabierto = _servicio(ruta, transporte)
    info = reabierto.estado_caso(caso)
    assert info.evaluacion_vigente
    assert info.resumen.h_estrella is not None and info.resumen.h_estrella.id_hipotesis == "h2"

    evidencia = reabierto.nueva_evidencia(
        caso, _vista("Lateral", "lateral"), "triángulo", valor="triangulo"
    )
    assert evidencia.observacion.derrotadas == ["h1", "h2"]
    assert evidencia.h_estrella_anterior is not None
    assert evidencia.evaluacion.h_estrella is None and evidencia.evaluacion.expansion_sugerida

    retractacion = reabierto.retractar_evidencia(caso, evidencia.observacion.hechos[0].id)
    assert retractacion.reactivadas == ["h1", "h2"]
    assert retractacion.evaluacion is not None
    assert retractacion.evaluacion.h_estrella is not None
    assert retractacion.evaluacion.h_estrella.id_hipotesis == "h2"


def test_caso_financiero_con_cortex_y_verificador(
    tmp_path: Path, transporte: TransporteFalso
) -> None:
    ruta = tmp_path / "casos.db"
    servicio = _servicio(ruta, transporte)
    caso = servicio.crear_caso("Empresa X", "finanzas").caso_id
    r = servicio.agregar_observacion(
        caso,
        EntradaObservador(nombre="Analista A", marco="fundamental"),
        "El margen bruto cayó 4 pp. Recomendamos vender.",
    )
    assert [h.id for h in r.hechos] == ["o1.h1"]
    assert r.opiniones == ["Recomendamos vender."]
    assert r.observador_id == "analista_a"
    servicio.agregar_observacion(
        caso, EntradaObservador(nombre="Analista B"), "El volumen creció 18 %."
    )
    servicio.proponer_hipotesis(
        caso,
        [
            EntradaHipotesis(mecanismo="Reducción sostenida de precios para ganar cuota"),
            EntradaHipotesis(mecanismo="Crece la demanda del sector"),
            EntradaHipotesis(
                mecanismo="Dividendos sobre la caja",
                afirmaciones={"dividendos_pagados": 120, "caja_disponible": 80, "inventada": 1},
            ),
        ],
    )
    evaluacion = servicio.evaluar(caso)
    assert evaluacion.h_estrella is not None and evaluacion.h_estrella.id_hipotesis == "h1"
    assert [d.reglas for d in evaluacion.descartadas_por_reglas] == [["dividendos_bajo_caja"]]
    llamadas = len(transporte.llamadas)

    # Reevaluar y reconstruir no vuelve a verificar: los veredictos están guardados.
    servicio.evaluar(caso)
    _servicio(ruta, transporte).evaluar(caso)
    assert len(transporte.llamadas) == llamadas
    assert servicio.estado_caso(caso).llamadas == llamadas

    auditoria = servicio.auditoria(caso)
    assert auditoria.opiniones["analista_a"] == ["Recomendamos vender."]
    texto = auditoria_markdown(auditoria)
    assert "## Mejor explicación" in texto and "h1" in texto and "dividendos" in texto.lower()


def test_corregir_observacion(tmp_path: Path, transporte: TransporteFalso) -> None:
    servicio = _servicio(tmp_path / "c.db", transporte)
    caso = servicio.crear_caso("x", "sintetico").caso_id
    servicio.agregar_observacion(caso, _vista("Frontal", "frontal"), "cuadrado", valor="cuadrado")
    servicio.proponer_hipotesis(caso, [_solido("cilindro")])
    corregida = servicio.corregir_observacion(caso, "o1", valor="rectangulo")
    assert corregida.hechos[0].id == "o2" and corregida.derrotadas == []
    assert servicio.evaluar(caso).ranking[0].consiliencia_c == 1

    opinion = servicio.corregir_observacion(caso, "o2", es_opinion=True)
    assert opinion.hechos == [] and opinion.opiniones == ["cuadrado"]
    assert servicio.auditoria(caso).caso.resumen.n_observaciones == 0


def test_generar_hipotesis_y_limites(tmp_path: Path, transporte: TransporteFalso) -> None:
    servicio = _servicio(tmp_path / "c.db", transporte, hipotesis_vivas_max=2)
    caso = servicio.crear_caso("x", "finanzas").caso_id
    with pytest.raises(ErrorCaso) as sin_obs:
        servicio.generar_hipotesis(caso)
    assert sin_obs.value.codigo is CodigoError.SIN_OBSERVACIONES

    servicio.agregar_observacion(caso, EntradaObservador(nombre="A"), "El margen cayó.")
    generadas = servicio.generar_hipotesis(caso)
    assert generadas.hipotesis[0].origen == "motor:gen-responses"
    assert "modo: contrastivo" in generadas.avisos
    with pytest.raises(ErrorCaso) as limite:
        servicio.proponer_hipotesis(caso, [_solido("a"), _solido("b")])
    assert limite.value.codigo is CodigoError.LIMITE_HIPOTESIS


def test_presupuesto_del_caso(tmp_path: Path, transporte: TransporteFalso) -> None:
    servicio = _servicio(tmp_path / "c.db", transporte, llamadas_por_caso=1)
    caso = servicio.crear_caso("x", "finanzas").caso_id
    servicio.agregar_observacion(caso, EntradaObservador(nombre="A"), "El margen cayó.")
    with pytest.raises(ErrorCaso) as agotado:
        servicio.agregar_observacion(caso, EntradaObservador(nombre="B"), "El volumen creció.")
    assert agotado.value.codigo is CodigoError.PRESUPUESTO_CASO_AGOTADO


def test_errores_de_caso(tmp_path: Path, transporte: TransporteFalso) -> None:
    servicio = _servicio(tmp_path / "c.db", transporte)
    with pytest.raises(ErrorCaso) as dominio:
        servicio.crear_caso("x", "astrologia")
    assert dominio.value.codigo is CodigoError.DOMINIO_DESCONOCIDO
    with pytest.raises(ErrorCaso) as no_existe:
        servicio.evaluar("caso_99")
    assert no_existe.value.codigo is CodigoError.CASO_NO_ENCONTRADO

    caso = servicio.crear_caso("x", "sintetico").caso_id
    with pytest.raises(ErrorCaso) as sin_hip:
        servicio.agregar_observacion(caso, _vista("F", "frontal"), "círculo", valor="circulo")
        servicio.evaluar(caso)
    assert sin_hip.value.codigo is CodigoError.SIN_HIPOTESIS
    with pytest.raises(ErrorCaso) as sin_obs:
        servicio.retractar_evidencia(caso, "o9")
    assert sin_obs.value.codigo is CodigoError.OBSERVACION_NO_ENCONTRADA

    servicio.cerrar_caso(caso)
    with pytest.raises(ErrorCaso) as cerrado:
        servicio.evaluar(caso)
    assert cerrado.value.codigo is CodigoError.CASO_CERRADO
    assert [c.caso_id for c in servicio.listar_casos("cerrado")] == [caso]
    assert "sintetico" in servicio.listar_dominios()


def test_estado_de_hipotesis_en_auditoria(tmp_path: Path, transporte: TransporteFalso) -> None:
    servicio = _servicio(tmp_path / "c.db", transporte)
    caso = servicio.crear_caso("x", "sintetico").caso_id
    servicio.agregar_observacion(caso, _vista("F", "frontal"), "rectángulo", valor="rectangulo")
    servicio.proponer_hipotesis(caso, [_solido("cilindro")])
    servicio.agregar_observacion(caso, _vista("L", "lateral"), "triángulo", valor="triangulo")
    hipotesis = servicio.auditoria(caso).hipotesis[0]
    assert hipotesis.estado is EstadoHipotesis.DERROTADA and hipotesis.derrotada_por == ["o2"]


def test_experimento_finanzas_con_transporte_falso(transporte: TransporteFalso) -> None:
    resultado = finanzas_llm(config_prueba(), transporte)
    assert resultado.exito, [c.descripcion for c in resultado.comprobaciones if not c.ok]
