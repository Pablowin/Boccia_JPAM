"""Rutas del proyecto y medidas de la pista."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Se puede cambiar con la variable de entorno BOCCIA_DB (ejecutable, tests...).
PATH_DB = Path(os.environ.get("BOCCIA_DB", ROOT / "data" / "boccia.db"))
PATH_SCHEMA = Path(__file__).resolve().parent / "db" / "schema.sql"

# Medidas en centímetros. Origen: esquina izquierda de la línea de lanzamiento.
ANCHO = 600
LARGO = 1000
CRUZ = (300, 500)