"""Registro de lanzamientos sobre la pista.

Prototipo visual: el partido y las posiciones se guardan en st.session_state,
todavía no en la base de datos.
"""

import copy
import math

import streamlit as st

from componentes.estilo import aplicar_estilo, cabecera, marcador, tabla_secuencia, tarjeta_lanzamiento
from componentes.pista import (BOLAS_POR_COLOR, MODALIDADES, box_diana, boxes_de, pista_interactiva,
                               siguientes)

st.set_page_config(page_title="Registro de lanzamientos · Boccia", page_icon="🎯", layout="wide")
aplicar_estilo()

SIN_PUNTOS = {"R": 0, "A": 0}


# ── Estado ──────────────────────────────────────────────────────────────────
def nuevo_parcial(version: int = 0) -> dict:
    return {"base": [], "trabajo": [], "lanzada": None, "historial": [], "version": version,
            "puntos": dict(SIN_PUNTOS), "puntos_base": dict(SIN_PUNTOS)}


st.session_state.setdefault("modalidad", "Individual")
st.session_state.setdefault("rejilla", True)
st.session_state.setdefault("partido", {"parcial": 1, "resultados": []})
st.session_state.setdefault("registro", nuevo_parcial())


def se_movio(antes: dict | None, ahora: dict) -> bool:
    if antes is None:
        return False
    if antes["fuera"] or ahora["fuera"]:
        return antes["fuera"] != ahora["fuera"]
    return math.hypot(ahora["x"] - antes["x"], ahora["y"] - antes["y"]) > 0.01


def bolas_movidas(reg: dict) -> list[str]:
    """Bolas (distintas de la lanzada) que han cambiado respecto a la última foto confirmada."""
    previas = {b["id"]: b for b in reg["base"]}
    return [b["id"] for b in reg["trabajo"]
            if b["id"] != reg["lanzada"] and se_movio(previas.get(b["id"]), b)]


# ── Acciones de los botones ─────────────────────────────────────────────────
def siguiente() -> None:
    reg = st.session_state.registro
    if not reg["lanzada"]:
        return
    reg["historial"].append({
        "orden": len(reg["historial"]) + 1,
        "bola": next(b for b in reg["trabajo"] if b["id"] == reg["lanzada"]),
        "movidas": bolas_movidas(reg),
        "puntos": dict(reg["puntos"]),
        "foto": copy.deepcopy(reg["trabajo"]),
    })
    reg["base"] = copy.deepcopy(reg["trabajo"])
    reg["puntos_base"] = dict(reg["puntos"])
    reg["lanzada"] = None
    reg["version"] += 1


def cancelar() -> None:
    """Vuelve a la última foto confirmada, sin tocar nada más."""
    reg = st.session_state.registro
    reg["trabajo"] = copy.deepcopy(reg["base"])
    reg["puntos"] = dict(reg["puntos_base"])
    reg["lanzada"] = None
    reg["version"] += 1


def reiniciar_parcial() -> None:
    st.session_state.registro = nuevo_parcial(st.session_state.registro["version"] + 1)


def cerrar_parcial() -> None:
    partido, reg = st.session_state.partido, st.session_state.registro
    partido["resultados"].append({"parcial": partido["parcial"], **reg["puntos"]})
    partido["parcial"] += 1
    reiniciar_parcial()


def nuevo_partido() -> None:
    st.session_state.partido = {"parcial": 1, "resultados": []}
    reiniciar_parcial()


# ── Datos para pintar ───────────────────────────────────────────────────────
partido, reg = st.session_state.partido, st.session_state.registro
modalidad = st.session_state.modalidad
n_parciales = MODALIDADES[modalidad]["parciales"]
terminado = partido["parcial"] > n_parciales
parcial = min(partido["parcial"], n_parciales)

with st.container(key="cabecera"):
    cab_izq, cab_der = st.columns([3, 2], vertical_alignment="center")
    cab_izq.html(cabecera("Registro de lanzamientos"))
    controles = cab_der.container()     # se rellena después de leer la pista (ver abajo)

col_pista, col_panel = st.columns([5, 6], gap="large")

with col_pista:
    valor = pista_interactiva(
        base=reg["base"],
        trabajo=reg["trabajo"],
        lanzada=reg["lanzada"],
        boxes=boxes_de(modalidad, partido["parcial"], reg["base"], activo=not terminado),
        siguientes=siguientes(reg["base"]),
        orden=len(reg["historial"]) + 1,
        version=reg["version"],
        rejilla=st.session_state.rejilla,
        key="pista_registro",
    )

# Streamlit devuelve el último valor del componente aunque sea de antes de un
# Siguiente/Cancelar; solo se acepta si es de la versión actual.
if valor and valor.get("version") == reg["version"]:
    reg["trabajo"] = valor["bolas"]
    reg["lanzada"] = valor["lanzada"]
    reg["puntos"] = valor["puntos"]

en_juego = bool(reg["trabajo"]) or bool(partido["resultados"])
completo = not terminado and len(reg["base"]) == 1 + 2 * BOLAS_POR_COLOR and not reg["lanzada"]
lanzada = next((b for b in reg["trabajo"] if b["id"] == reg["lanzada"]), None)
blanca_pendiente = not any(b["color"] == "B" for b in reg["trabajo"])
totales = {c: sum(r[c] for r in partido["resultados"]) for c in ("R", "A")}

with controles:
    c1, c2 = st.columns([3, 2], vertical_alignment="center")
    c1.segmented_control("Modalidad", list(MODALIDADES), key="modalidad", required=True,
                         disabled=en_juego, label_visibility="collapsed",
                         help="Se fija al empezar el partido" if en_juego else None)
    c2.toggle("Rejilla de zonas", key="rejilla")

with col_panel:
    st.html(marcador(
        totales=totales,
        provisional=reg["puntos"],
        restantes={c: BOLAS_POR_COLOR - sum(b["color"] == c for b in reg["trabajo"]) for c in ("R", "A")},
        parcial=parcial,
        n_parciales=n_parciales,
        lanzamiento=len(reg["historial"]) + 1,
        resultados=partido["resultados"],
        terminado=terminado,
    ))

    with st.container(key="tarjeta_actual"):
        st.html(tarjeta_lanzamiento(
            lanzamiento=len(reg["historial"]) + 1,
            bola=lanzada,
            movidas=bolas_movidas(reg) if lanzada else [],
            puntos=reg["puntos"],
            box_blanca=box_diana(modalidad, partido["parcial"]) if blanca_pendiente else None,
            completo=completo,
            terminado=terminado,
            totales=totales,
        ))
        b1, b2 = st.columns(2)
        if terminado:
            b1.button("Nuevo partido", type="primary", icon=":material/add:", width="stretch",
                      on_click=nuevo_partido)
        elif completo:
            b1.button("Cerrar parcial", type="primary", icon=":material/flag:", width="stretch",
                      on_click=cerrar_parcial)
        else:
            b1.button("Siguiente", type="primary", icon=":material/arrow_forward:", width="stretch",
                      on_click=siguiente, disabled=lanzada is None)
        b2.button("Cancelar", icon=":material/undo:", width="stretch",
                  on_click=cancelar, disabled=reg["trabajo"] == reg["base"])

    with st.container(key="tarjeta_secuencia"):
        st.html(tabla_secuencia(reg["historial"]))

    a1, a2, _ = st.columns([1, 1, 2])
    a1.button("Reiniciar parcial", icon=":material/restart_alt:", type="tertiary",
              on_click=reiniciar_parcial, disabled=terminado)
    a2.button("Nuevo partido", icon=":material/add_circle:", type="tertiary", on_click=nuevo_partido)
