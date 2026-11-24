"""Pista de boccia interactiva para el registro de lanzamientos.

Es un componente de Streamlit hecho a mano (HTML + SVG + JavaScript, sin
compilar nada) que permite hacer clic y arrastrar las bolas desde su box hasta
la pista. El dibujo y la interacción están en ``pista_frontend/index.html``.

Formato de una bola: ``{"id": "R2", "color": "R", "box": 3, "x": 2.35,
"y": 4.1, "fuera": False, "zona": "3I45", "dist": 0.42}``, con x/y en metros
y el origen en la esquina izquierda de la línea de lanzamiento (igual que
``zona_a_xy``). ``dist`` es la distancia a la blanca.
"""

from pathlib import Path

import streamlit.components.v1 as components

BOLAS_POR_COLOR = 6

# Boxes de cada lado y número de parciales por modalidad.
# Por confirmar con el reglamento del proyecto (docs/reglamento.md).
MODALIDADES = {
    "Individual": {"boxes": {3: "R", 4: "A"}, "parciales": 4},
    "Parejas": {"boxes": {2: "R", 3: "A", 4: "R", 5: "A"}, "parciales": 4},
    "Equipos": {"boxes": {1: "R", 2: "A", 3: "R", 4: "A", 5: "R", 6: "A"}, "parciales": 6},
}

_FRONTEND = Path(__file__).parent / "pista_frontend"
_pista = components.declare_component("pista_boccia", path=str(_FRONTEND))


def box_diana(modalidad: str, parcial: int) -> int:
    """Box desde el que se lanza la blanca en cada parcial."""
    if modalidad == "Individual":
        return 3 if parcial % 2 else 4          # rojo en los impares, azul en los pares
    if modalidad == "Parejas":
        return 2 + (parcial - 1) % 4            # boxes 2, 3, 4, 5
    return 1 + (parcial - 1) % 6                # boxes 1 a 6


def boxes_de(modalidad: str, parcial: int, bolas: list[dict], activo: bool = True) -> list[dict]:
    """Estado de los 6 boxes: color, cuántas bolas le quedan y si guarda la blanca."""
    asignacion = MODALIDADES[modalidad]["boxes"]
    por_box = BOLAS_POR_COLOR // (len(asignacion) // 2)
    diana = box_diana(modalidad, parcial)
    blanca_pendiente = activo and not any(b["color"] == "B" for b in bolas)
    boxes = []
    for numero in range(1, 7):
        color = asignacion.get(numero)
        cupo = por_box if color else 0
        lanzadas = sum(1 for b in bolas if b.get("box") == numero and b["color"] == color)
        boxes.append({
            "numero": numero,
            "color": color,
            "cupo": cupo,
            "restantes": cupo - lanzadas if activo else 0,
            "diana": numero == diana,
            "blanca": blanca_pendiente and numero == diana,
        })
    return boxes


def siguientes(bolas: list[dict]) -> dict:
    """Id que recibirá la próxima bola de cada color (None si ya no quedan)."""
    res = {}
    for color in ("R", "A"):
        n = sum(b["color"] == color for b in bolas)
        res[color] = f"{color}{n + 1}" if n < BOLAS_POR_COLOR else None
    return res


def pista_interactiva(
    *,
    base: list[dict],
    trabajo: list[dict],
    lanzada: str | None,
    boxes: list[dict],
    siguientes: dict,
    orden: int,
    version: int,
    rejilla: bool = True,
    alto: int = 1000,
    key: str | None = None,
) -> dict | None:
    """Dibuja la pista y devuelve el estado de las bolas tras la última interacción.

    - ``base``: foto confirmada con el último «Siguiente» (para marcar bolas movidas).
    - ``trabajo``: posiciones actuales, aún sin confirmar.
    - ``lanzada``: id de la bola lanzada en este turno, o None.
    - ``boxes``: salida de :func:`boxes_de`.
    - ``siguientes``: salida de :func:`siguientes`.
    - ``version``: se incrementa cada vez que Python cambia el estado
      (Siguiente, Cancelar...). El componente solo se resincroniza entonces.

    Devuelve ``{"version", "lanzada", "bolas", "puntos": {"R", "A"}}``.
    Streamlit conserva el último valor entre reruns, así que hay que
    descartarlo si su ``version`` no coincide con la actual.
    """
    return _pista(
        base=base,
        trabajo=trabajo,
        lanzada=lanzada,
        boxes=boxes,
        siguientes=siguientes,
        orden=orden,
        version=version,
        rejilla=rejilla,
        alto=alto,
        key=key,
        default=None,
    )
