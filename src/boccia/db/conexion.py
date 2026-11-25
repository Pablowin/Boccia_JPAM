"""Conexión con la base de datos SQLite."""

import sqlite3
from contextlib import contextmanager

from boccia.config import PATH_DB, PATH_SCHEMA


@contextmanager
def conectar(ruta=PATH_DB):
    """Abre la base de datos, guarda los cambios al terminar y la cierra.

    Si algo falla, deshace todos los cambios.
    """
    con = sqlite3.connect(ruta)
    con.row_factory = sqlite3.Row               # permite fila["nombre_equipo"]
    con.execute("PRAGMA foreign_keys = ON")     # SQLite no las comprueba por defecto
    try:
        yield con
        con.commit()
    except BaseException:
        con.rollback()
        raise
    finally:
        con.close()


def crear_tablas(ruta=PATH_DB):
    """Crea las tablas que falten. No borra datos."""
    with conectar(ruta) as con:
        con.executescript(PATH_SCHEMA.read_text(encoding="utf-8"))