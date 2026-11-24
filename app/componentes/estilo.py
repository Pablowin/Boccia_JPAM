"""Estilo visual común de la app: CSS global y piezas HTML reutilizables.

Las páginas llaman a ``aplicar_estilo()`` al principio y pintan las piezas con
``st.html(...)``. Los colores de marca están en las variables CSS de ``:root``.
"""

from html import escape

import streamlit as st

NOMBRES = {"B": "Blanca", "R": "Roja", "A": "Azul"}

CSS = """
<style>
:root {
  --bx-rojo: #D62828; --bx-azul: #1F4FC4; --bx-tinta: #0F1E33; --bx-texto: #16202B;
  --bx-suave: #64748B; --bx-borde: #E3E8EF; --bx-oro: #F5B700;
}
[data-testid="stMainBlockContainer"] { padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1480px; }
[data-testid="stHeader"] { background: transparent; }

/* ── Cabecera ── */
.st-key-cabecera { padding-bottom: 12px; margin-bottom: 4px; border-bottom: 1px solid var(--bx-borde); }
.bx-top { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; padding: 2px; }
.bx-brand { display: flex; align-items: center; gap: 14px; }
.bx-logo { position: relative; flex: none; width: 48px; height: 48px; border-radius: 13px;
  background: linear-gradient(160deg, #1B3254, var(--bx-tinta)); box-shadow: 0 6px 14px rgba(15,30,51,.25); }
.bx-logo i { position: absolute; border-radius: 50%; box-shadow: 0 1px 2px rgba(0,0,0,.35); }
.bx-logo .l1 { width: 17px; height: 17px; left: 8px; top: 20px;
  background: radial-gradient(circle at 35% 30%, #ff8080, #d62828 60%, #8a1212); }
.bx-logo .l2 { width: 17px; height: 17px; right: 8px; top: 20px;
  background: radial-gradient(circle at 35% 30%, #86b4ff, #1f4fc4 60%, #0d266b); }
.bx-logo .l3 { width: 11px; height: 11px; left: 18.5px; top: 9px;
  background: radial-gradient(circle at 35% 30%, #fff, #e8e8e8 70%, #bdbdbd); }
.bx-kicker { font-size: .72rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; color: var(--bx-suave); }
.bx-title { font-size: 1.65rem; font-weight: 800; line-height: 1.15; color: var(--bx-texto); }
.bx-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.bx-tag { font-size: .8rem; font-weight: 600; padding: 5px 12px; border-radius: 999px;
  background: #fff; border: 1px solid var(--bx-borde); color: var(--bx-texto); }
.bx-tag-vivo { color: #0E7A3E; border-color: #BFE5CE; background: #EDF8F1; }
.bx-tag-vivo::before { content: ""; display: inline-block; width: 7px; height: 7px; margin-right: 7px;
  border-radius: 50%; background: #16A34A; vertical-align: 1px; animation: bx-pulso 1.6s infinite; }
@keyframes bx-pulso { 50% { opacity: .3; } }

/* ── Marcador ── */
.bx-score { display: grid; grid-template-columns: 1fr auto 1fr; overflow: hidden; color: #fff;
  border-radius: 18px; box-shadow: 0 10px 26px rgba(15,30,51,.2); }
.bx-side { display: flex; flex-direction: column; gap: 2px; padding: 15px 20px 16px; }
.bx-side-R { background: linear-gradient(135deg, #E23636, #A51A1A); }
.bx-side-A { background: linear-gradient(225deg, #3168E3, #153A99); align-items: flex-end; text-align: right; }
.bx-side-k { font-size: .7rem; font-weight: 800; letter-spacing: .18em; opacity: .8; }
.bx-side-n { font-size: 1.05rem; font-weight: 700; }
.bx-total { font-size: 3.1rem; font-weight: 800; line-height: 1; margin-top: 6px; font-variant-numeric: tabular-nums; }
.bx-prov { font-size: .8rem; opacity: .92; }
.bx-dots { display: flex; gap: 5px; margin-top: 9px; }
.bx-dots i { width: 11px; height: 11px; border-radius: 50%; background: #fff; box-shadow: inset 0 -1px 2px rgba(0,0,0,.2); }
.bx-dots i.v { background: transparent; box-shadow: none; border: 1.5px solid rgba(255,255,255,.5); }
.bx-mid { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px;
  min-width: 158px; padding: 14px 22px; background: var(--bx-tinta); }
.bx-mid-k { font-size: .66rem; font-weight: 800; letter-spacing: .2em; opacity: .6; }
.bx-mid-n { font-size: 2rem; font-weight: 800; line-height: 1; }
.bx-mid-n span { font-size: 1rem; font-weight: 700; opacity: .5; }
.bx-mid-s { font-size: .78rem; opacity: .75; }
.bx-ends { display: flex; gap: 4px; margin-top: 7px; }
.bx-ends span { font-size: .68rem; font-weight: 600; padding: 2px 7px; border-radius: 6px; background: rgba(255,255,255,.1); }
.bx-ends span.act { background: var(--bx-oro); color: #1b1b1b; font-weight: 800; }

/* ── Tarjetas ── */
.st-key-tarjeta_actual, .st-key-tarjeta_secuencia {
  background: #fff; border: 1px solid var(--bx-borde); border-radius: 18px; padding: 18px 20px 16px;
  box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 6px 18px rgba(16,24,40,.06); }
.bx-card-h { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 12px; }
.bx-card-t { font-size: .74rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; color: var(--bx-suave); }
.bx-card-x { font-size: .8rem; color: var(--bx-suave); }
.bx-throw { display: flex; align-items: center; gap: 14px; }
.bx-throw-id { font-size: 1.3rem; font-weight: 800; color: var(--bx-texto); }
.bx-throw-sub { font-size: .86rem; color: var(--bx-suave); }
.bx-badge { margin-left: auto; padding: 5px 11px; border-radius: 999px; font-size: .78rem; font-weight: 700; white-space: nowrap; }
.bx-badge-ok { background: #EEF2F6; color: #475569; }
.bx-badge-aviso { background: #FFF4D6; color: #8A5A00; border: 1px solid #F5D78A; }
.bx-facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 16px 0 6px; }
.bx-facts div { padding: 9px 12px; border-radius: 12px; background: #F6F8FB; border: 1px solid #EDF1F6; }
.bx-facts span { display: block; font-size: .68rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--bx-suave); }
.bx-facts b { font-size: 1.05rem; color: var(--bx-texto); font-variant-numeric: tabular-nums; }
@media (max-width: 1200px) { .bx-facts { grid-template-columns: repeat(2, 1fr); } }
.bx-vacio { display: flex; align-items: center; gap: 14px; padding: 4px 0 10px; color: var(--bx-suave); font-size: .95rem; }
.bx-vacio b { color: var(--bx-texto); }
.bx-vacio .bx-ball { opacity: .9; }

/* ── Bolas ── */
.bx-ball { display: inline-flex; align-items: center; justify-content: center; flex: none;
  width: 24px; height: 24px; border-radius: 50%; color: #fff; font-weight: 800; font-size: 12px;
  box-shadow: inset -2px -3px 5px rgba(0,0,0,.25), 0 1px 2px rgba(0,0,0,.2); }
.bx-ball.R { background: radial-gradient(circle at 35% 30%, #ff8080, #d62828 55%, #8a1212); }
.bx-ball.A { background: radial-gradient(circle at 35% 30%, #86b4ff, #1f4fc4 55%, #0d266b); }
.bx-ball.B { background: radial-gradient(circle at 35% 30%, #fff, #eee 70%, #c4c4c4); border: 1px solid #b9ab98; }
.bx-ball.RA { background: linear-gradient(135deg, #e03131 0 50%, #1f4fc4 50% 100%); }
.bx-ball.lg { width: 50px; height: 50px; font-size: 21px; }

/* ── Tabla de secuencia ── */
.bx-tabla { width: 100%; border-collapse: collapse; font-size: .9rem; }
.bx-tabla th { padding: 0 8px 9px; text-align: left; font-size: .66rem; font-weight: 800; letter-spacing: .1em;
  text-transform: uppercase; color: var(--bx-suave); border-bottom: 1px solid var(--bx-borde); }
.bx-tabla td { padding: 8px; color: var(--bx-texto); border-bottom: 1px solid #F0F3F7; font-variant-numeric: tabular-nums; }
.bx-tabla tr:last-child td { border-bottom: 0; }
.bx-tabla td.n { width: 30px; color: var(--bx-suave); }
.bx-celda-bola { display: flex; align-items: center; gap: 9px; font-weight: 700; }
.bx-marc b { font-weight: 800; }
.bx-marc .R { color: var(--bx-rojo); } .bx-marc .A { color: var(--bx-azul); }
.bx-chip { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: .74rem; font-weight: 700;
  background: #FFF4D6; color: #8A5A00; }
.bx-gris { color: #A0AEC0; }
</style>
"""


def aplicar_estilo() -> None:
    st.html(CSS)


def fmt(v: float | None, sufijo: str = "") -> str:
    return "—" if v is None else f"{v:.2f}".replace(".", ",") + sufijo


def chip_bola(id_: str, color: str, grande: bool = False) -> str:
    texto = "" if color == "B" else escape(id_[1:])
    return f'<span class="bx-ball {color}{" lg" if grande else ""}">{texto}</span>'


def cabecera(titulo: str, etiquetas: list[str] = (), en_vivo: bool = False) -> str:
    tags = "".join(f'<span class="bx-tag">{escape(t)}</span>' for t in etiquetas)
    if en_vivo:
        tags += '<span class="bx-tag bx-tag-vivo">Registro en curso</span>'
    return f"""
    <div class="bx-top">
      <div class="bx-brand">
        <div class="bx-logo"><i class="l1"></i><i class="l2"></i><i class="l3"></i></div>
        <div><div class="bx-kicker">Boccia · Análisis de partido</div><div class="bx-title">{escape(titulo)}</div></div>
      </div>
      <div class="bx-tags">{tags}</div>
    </div>"""


def _puntos(n: int) -> str:
    return "Sin puntos en este parcial" if n == 0 else f"+{n} en este parcial"


def _bolitas(restantes: int, total: int = 6) -> str:
    return "".join('<i></i>' if i < restantes else '<i class="v"></i>' for i in range(total))


def marcador(*, totales: dict, provisional: dict, restantes: dict, parcial: int, n_parciales: int,
             lanzamiento: int, resultados: list[dict], terminado: bool) -> str:
    """Marcador del partido: total por lado, puntos provisionales del parcial y bolas que quedan."""
    ends = []
    for i in range(1, n_parciales + 1):
        hecho = next((r for r in resultados if r["parcial"] == i), None)
        if hecho:
            ends.append(f'<span>P{i} {hecho["R"]}–{hecho["A"]}</span>')
        else:
            ends.append(f'<span class="{"act" if i == parcial and not terminado else ""}">P{i}</span>')
    centro_n = "FIN" if terminado else f"{parcial}<span>/{n_parciales}</span>"
    centro_s = "Partido terminado" if terminado else f"Lanzamiento {min(lanzamiento, 13)} de 13"
    return f"""
    <div class="bx-score">
      <div class="bx-side bx-side-R">
        <div class="bx-side-k">ROJO</div><div class="bx-side-n">Lado rojo</div>
        <div class="bx-total">{totales["R"]}</div><div class="bx-prov">{_puntos(provisional["R"])}</div>
        <div class="bx-dots">{_bolitas(restantes["R"])}</div>
      </div>
      <div class="bx-mid">
        <div class="bx-mid-k">PARCIAL</div><div class="bx-mid-n">{centro_n}</div>
        <div class="bx-mid-s">{centro_s}</div><div class="bx-ends">{"".join(ends)}</div>
      </div>
      <div class="bx-side bx-side-A">
        <div class="bx-side-k">AZUL</div><div class="bx-side-n">Lado azul</div>
        <div class="bx-total">{totales["A"]}</div><div class="bx-prov">{_puntos(provisional["A"])}</div>
        <div class="bx-dots">{_bolitas(restantes["A"])}</div>
      </div>
    </div>"""


def tarjeta_lanzamiento(*, lanzamiento: int, bola: dict | None, movidas: list[str], puntos: dict,
                        box_blanca: int | None, completo: bool, terminado: bool, totales: dict) -> str:
    """Contenido de la tarjeta «Lanzamiento actual» (los botones los pone la página)."""
    cab = (f'<div class="bx-card-h"><span class="bx-card-t">Lanzamiento actual</span>'
           f'<span class="bx-card-x">{min(lanzamiento, 13)} de 13</span></div>')
    if terminado:
        r, a = totales["R"], totales["A"]
        ganador = "Empate" if r == a else f"Gana el lado {'rojo' if r > a else 'azul'}"
        return (f'<div class="bx-card-h"><span class="bx-card-t">Partido terminado</span></div>'
                f'<div class="bx-vacio"><div><b>{ganador}</b> · {r} – {a}</div></div>')
    if completo:
        return (cab + f'<div class="bx-vacio">{chip_bola("B", "B", True)}<div><b>Parcial completo.</b> '
                f'Resultado: rojo {puntos["R"]} – {puntos["A"]} azul. '
                f'Pulsa «Cerrar parcial» para pasar al siguiente.</div></div>')
    if bola is None:
        if box_blanca is not None:
            return (cab + f'<div class="bx-vacio">{chip_bola("B", "B", True)}<div><b>Empieza el parcial.</b> '
                    f'Arrastra la blanca desde el box {box_blanca} hasta el campo.</div></div>')
        return (cab + '<div class="bx-vacio"><span class="bx-ball RA lg"></span><div><b>Siguiente bola.</b> '
                'Arrástrala desde su box hasta el campo. Si choca con otras, recolócalas también.</div></div>')

    if movidas:
        badge = f'<span class="bx-badge bx-badge-aviso">Colisión · desplaza {escape(", ".join(movidas))}</span>'
    else:
        badge = '<span class="bx-badge bx-badge-ok">Sin colisión</span>'
    if bola["fuera"]:
        posicion = "Fuera"
    else:
        posicion = f'{fmt(bola["x"])} · {fmt(bola["y"])} m'
    box = f'B{bola["box"]}' if bola.get("box") else "—"
    return cab + f"""
      <div class="bx-throw">
        {chip_bola(bola["id"], bola["color"], True)}
        <div><div class="bx-throw-id">{escape(bola["id"])} · {NOMBRES[bola["color"]]}</div>
             <div class="bx-throw-sub">Lanzada desde el box {bola.get("box") or "—"}</div></div>
        {badge}
      </div>
      <div class="bx-facts">
        <div><span>Box</span><b>{box}</b></div>
        <div><span>Zona</span><b>{escape(bola.get("zona") or "—")}</b></div>
        <div><span>Posición</span><b>{posicion}</b></div>
        <div><span>A la blanca</span><b>{fmt(bola.get("dist"), " m")}</b></div>
      </div>"""


def tabla_secuencia(historial: list[dict]) -> str:
    """Tabla con los lanzamientos confirmados del parcial, del más reciente al primero."""
    cab = (f'<div class="bx-card-h"><span class="bx-card-t">Secuencia del parcial</span>'
           f'<span class="bx-card-x">{len(historial)} confirmados</span></div>')
    if not historial:
        return cab + '<div class="bx-vacio">Todavía no hay lanzamientos confirmados en este parcial.</div>'
    filas = []
    for h in reversed(historial):
        b = h["bola"]
        desplaza = (" ".join(f'<span class="bx-chip">{escape(m)}</span>' for m in h["movidas"])
                    or '<span class="bx-gris">—</span>')
        filas.append(f"""
          <tr>
            <td class="n">{h["orden"]}</td>
            <td><div class="bx-celda-bola">{chip_bola(b["id"], b["color"])}{escape(b["id"])}</div></td>
            <td>{f'B{b["box"]}' if b.get("box") else "—"}</td>
            <td>{escape(b.get("zona") or "—")}</td>
            <td>{fmt(b.get("dist"), " m")}</td>
            <td class="bx-marc"><b class="R">{h["puntos"]["R"]}</b> – <b class="A">{h["puntos"]["A"]}</b></td>
            <td>{desplaza}</td>
          </tr>""")
    return cab + f"""
      <table class="bx-tabla">
        <thead><tr><th>#</th><th>Bola</th><th>Box</th><th>Zona</th><th>A la blanca</th><th>Marcador</th><th>Desplaza</th></tr></thead>
        <tbody>{"".join(filas)}</tbody>
      </table>"""
