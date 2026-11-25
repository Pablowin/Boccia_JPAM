"""Crea la base de datos. Uso, desde la raíz: python scripts/crear_db.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from boccia.config import PATH_DB  
from boccia.db.conexion import conectar, crear_tablas  

PATH_DB.parent.mkdir(parents=True, exist_ok=True)
crear_tablas()

with conectar() as con:
    tablas = [f["name"] for f in con.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
    bolas = con.execute("SELECT count(*) FROM bola").fetchone()[0]

print(f"Base de datos lista: {PATH_DB}")
print(f"Tablas ({len(tablas)}): {', '.join(tablas)}")
print(f"Bolas: {bolas}")