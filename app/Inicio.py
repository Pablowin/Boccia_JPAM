import streamlit as st


st.set_page_config(
    page_title="Boccia JPAM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Boccia JPAM")
st.subheader("Registro y análisis de partidos")
st.write(
    "Bienvenido. Desde aquí puedes acceder a las herramientas de registro, "
    "consulta y análisis del proyecto."
)

st.markdown("## Partido")
st.write("Prepara el partido y registra lo que ocurre en la pista.")
partido = st.columns(3)
with partido[0]:
    st.page_link(
        "pages/1_Jugadores.py",
        label="Jugadores",
        icon="👤",
        help="Consultar y gestionar jugadores.",
        width="stretch",
    )
with partido[1]:
    st.page_link(
        "pages/2_Nuevo_partido.py",
        label="Nuevo partido",
        icon="🏁",
        help="Configurar un partido.",
        width="stretch",
    )
with partido[2]:
    st.page_link(
        "pages/3_Registro_lanzamientos.py",
        label="Registro de lanzamientos",
        icon="📝",
        help="Anotar los lanzamientos de un partido.",
        width="stretch",
    )

st.markdown("## Consulta")
st.write("Explora los datos registrados y consulta el reglamento.")
consulta = st.columns(2)
with consulta[0]:
    st.page_link(
        "pages/4_Analisis.py",
        label="Análisis",
        icon="📊",
        help="Consultar el análisis de los partidos.",
        width="stretch",
    )
with consulta[1]:
    st.page_link(
        "pages/5_Reglamento.py",
        label="Reglamento",
        icon="📖",
        help="Leer el reglamento de boccia en español.",
        width="stretch",
    )

st.sidebar.title("Boccia JPAM")
st.sidebar.caption("Registro y análisis de partidos")