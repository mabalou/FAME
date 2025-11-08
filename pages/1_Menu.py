import streamlit as st
import json
from pathlib import Path
from utils import registrar_visita

# --- Cargar CSS ---
css_path = Path("assets/style.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Registrar visita
registrar_visita("Menú", st.session_state.theme, st.session_state.lang)

st.markdown("## 📖 Nuestra carta")

# Cargar datos del menú
data_file = Path("data/menu.json")
if not data_file.exists():
    st.error("No se encontró el archivo `data/menu.json`.")
    st.stop()

with open(data_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Selector de categoría (filtro)
categorias = list(data.keys())
categoria_sel = st.selectbox("Selecciona una categoría", categorias)

# Mostrar platos en tarjetas visuales
for plato in data[categoria_sel]:
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"### {plato['nombre']}")
            st.markdown(f"<p style='opacity:0.8'>{plato['descripcion']}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='font-size:1.1rem;font-weight:600;text-align:right;'>{plato['precio']} €</p>", unsafe_allow_html=True)
