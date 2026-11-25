-- Esquema de la base de datos de Boccia (SQLite).
-- Se puede ejecutar varias veces: no borra datos existentes.

CREATE TABLE IF NOT EXISTS equipo (
    id_equipo     INTEGER PRIMARY KEY,
    nombre_equipo TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS jugador (
    id_jugador      INTEGER PRIMARY KEY,
    nombre_jugador  TEXT NOT NULL,
    id_equipo       INTEGER NOT NULL REFERENCES equipo (id_equipo),
    anyo_nacimiento INTEGER
);

-- id_equipo1 es el rojo e id_equipo2 el azul.
CREATE TABLE IF NOT EXISTS partido (
    id_partido     INTEGER PRIMARY KEY,
    id_equipo1     INTEGER NOT NULL REFERENCES equipo (id_equipo),
    id_equipo2     INTEGER NOT NULL REFERENCES equipo (id_equipo),
    nombre_partido TEXT NOT NULL,
    CHECK (id_equipo1 <> id_equipo2)
);

CREATE TABLE IF NOT EXISTS parcial (
    id_parcial  INTEGER PRIMARY KEY,
    id_partido  INTEGER NOT NULL REFERENCES partido (id_partido) ON DELETE CASCADE,
    num_parcial INTEGER NOT NULL CHECK (num_parcial >= 1),
    UNIQUE (id_partido, num_parcial)
);

CREATE TABLE IF NOT EXISTS bola (
    id_bola TEXT PRIMARY KEY NOT NULL,
    color   TEXT NOT NULL CHECK (color IN ('B', 'R', 'A'))
);

-- Cada observación es un lanzamiento; id_bola es la bola que se lanza.
CREATE TABLE IF NOT EXISTS observacion (
    id_observacion INTEGER PRIMARY KEY,
    id_parcial     INTEGER NOT NULL REFERENCES parcial (id_parcial) ON DELETE CASCADE,
    id_jugador     INTEGER NOT NULL REFERENCES jugador (id_jugador),
    id_bola        TEXT NOT NULL REFERENCES bola (id_bola),
    box            INTEGER CHECK (box BETWEEN 1 AND 6),
    posicion_box   TEXT,
    extremidad     TEXT,
    UNIQUE (id_parcial, id_bola)    -- cada bola se lanza una vez por parcial
);

-- Foto de la pista tras el lanzamiento: una fila por cada bola lanzada hasta entonces.
-- Coordenadas del centro de la bola en CENTÍMETROS enteros. Origen: esquina izquierda
-- de la línea de lanzamiento. x e y vacías = bola fuera.
CREATE TABLE IF NOT EXISTS posicion (
    id_observacion INTEGER NOT NULL REFERENCES observacion (id_observacion) ON DELETE CASCADE,
    id_bola        TEXT NOT NULL REFERENCES bola (id_bola),
    x              INTEGER CHECK (x IS NULL OR (typeof(x) = 'integer' AND x BETWEEN 0 AND 600)),
    y              INTEGER CHECK (y IS NULL OR (typeof(y) = 'integer' AND y BETWEEN 0 AND 1000)),
    PRIMARY KEY (id_observacion, id_bola),
    CHECK ((x IS NULL) = (y IS NULL))
);

INSERT OR IGNORE INTO bola (id_bola, color) VALUES
    ('B', 'B'),
    ('R1', 'R'), ('R2', 'R'), ('R3', 'R'), ('R4', 'R'), ('R5', 'R'), ('R6', 'R'),
    ('A1', 'A'), ('A2', 'A'), ('A3', 'A'), ('A4', 'A'), ('A5', 'A'), ('A6', 'A');