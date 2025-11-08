import streamlit as st
import json
from pathlib import Path
from utils import registrar_visita, total_visitas
registrar_visita("Menú", st.session_state.theme, st.session_state.lang)


st.markdown("## 📖 Nuestra carta")

# Cargar el archivo JSON
data_file = Path("data/menu.json")
if not data_file.exists():
    st.error("No se encontró el archivo `data/menu.json`.")
    st.stop()

# Leer y parsear
try:
    menu = json.loads(data_file.read_text(encoding="utf-8"))
except json.JSONDecodeError:
    st.error("Error al leer el archivo JSON. Asegúrate de que tiene formato válido.")
    st.stop()

# Aplicar estilos visuales coherentes
st.markdown("""
<style>
.menu-section {
    margin-top: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(0,0,0,0.1);
}
.menu-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.6rem;
}
.menu-name {
    font-weight: 600;
    font-size: 1.05rem;
}
.menu-price {
    font-weight: 600;
    color: var(--menu-link);
    min-width: 70px;
    text-align: right;
}
.menu-desc {
    color: var(--text-color);
    opacity: 0.8;
    font-size: 0.9rem;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# Mostrar secciones e items
for section, items in menu.items():
    st.markdown(f"<div class='menu-section'><h3>{section}</h3>", unsafe_allow_html=True)
    for item in items:
        nombre = item.get("nombre", "")
        precio = item.get("precio", "")
        descripcion = item.get("descripcion", "")
        st.markdown(
            f"""
            <div class='menu-item'>
                <div>
                    <div class='menu-name'>{nombre}</div>
                    <div class='menu-desc'>{descripcion}</div>
                </div>
                <div class='menu-price'>{precio:.2f} €</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
