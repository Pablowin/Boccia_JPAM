from pathlib import Path

import streamlit as st


NOMBRE_PDF = "World-Boccia-Rules-2025-2028-v1.1-Spanish-Spain.pdf"
RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTAS_REGLAMENTO = (
    RAIZ_PROYECTO / "docs" / NOMBRE_PDF,
    RAIZ_PROYECTO / "data" / "raw" / NOMBRE_PDF,
    Path.home() / "Downloads" / NOMBRE_PDF,
)

st.set_page_config(
    page_title="Reglamento · Boccia JPAM",
    page_icon="📖",
    layout="wide",
)

st.title("Reglamento de boccia")
st.warning(
    "Aviso: la versión en inglés es la más actualizada y es la que se utilizará "
    "en caso de disputa o discusión sobre jugadas polémicas."
)
st.caption("Reglamento World Boccia 2025–2028, versión 1.1 en español.")

pdf_local = next((ruta for ruta in RUTAS_REGLAMENTO if ruta.is_file()), None)
if pdf_local is not None:
    st.pdf(pdf_local, height=900, key="reglamento_pdf")
else:
    st.info(
        "No se ha encontrado el PDF adjunto. Selecciónalo aquí para consultar "
        "el reglamento; también puedes colocarlo en la carpeta docs o data/raw."
    )
    pdf_subido = st.file_uploader(
        "Seleccionar el reglamento en PDF",
        type=["pdf"],
        accept_multiple_files=False,
    )
    if pdf_subido is not None:
        st.pdf(pdf_subido, height=900, key="reglamento_pdf_subido")