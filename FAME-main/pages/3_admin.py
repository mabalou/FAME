import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="🔒 Admin Fame", layout="wide")
st.title("🔒 Panel de gestión del menú")

# --- Contraseña ---
pwd = st.text_input("Contraseña", type="password", placeholder="Introduce la contraseña para editar el menú")
if pwd != st.secrets.get("admin_password", None):
    st.warning("Introduce la contraseña correcta para acceder.")
    st.stop()

st.success("Acceso concedido ✅")

# --- Carga del menú ---
menu_file = Path("data/menu.json")
if not menu_file.exists():
    st.error("No se encontró el archivo menu.json.")
    st.stop()

menu = json.loads(menu_file.read_text(encoding="utf-8"))

# --- Edición del menú ---
for section, items in menu.items():
    with st.expander(f"🍽️ {section}", expanded=False):
        for i, item in enumerate(items):
            st.markdown("---")
            item["nombre"] = st.text_input("Nombre", value=item.get("nombre", ""), key=f"nombre_{section}_{i}")
            item["precio"] = st.number_input("Precio (€)", value=float(item.get("precio", 0)), step=0.1, key=f"precio_{section}_{i}")
            item["descripcion"] = st.text_area("Descripción", value=item.get("descripcion", ""), key=f"desc_{section}_{i}")

        if st.button(f"➕ Añadir producto a {section}", key=f"add_{section}"):
            items.append({"nombre": "Nuevo producto", "precio": 0, "descripcion": ""})

# --- Añadir nueva sección ---
st.markdown("---")
nueva_sec = st.text_input("➕ Añadir nueva sección (nombre)", key="nueva_sec")
if st.button("Crear sección"):
    if nueva_sec and nueva_sec not in menu:
        menu[nueva_sec] = []
        st.success(f"Sección '{nueva_sec}' añadida ✅")
    else:
        st.warning("El nombre está vacío o ya existe.")

# --- Guardar cambios ---
if st.button("💾 Guardar cambios en el menú"):
    menu_file.write_text(json.dumps(menu, ensure_ascii=False, indent=2), encoding="utf-8")
    st.success("Menú actualizado correctamente ✅")

# --- Vista previa JSON ---
st.markdown("### 🧾 Vista previa actual del menú")
st.code(json.dumps(menu, ensure_ascii=False, indent=2), language="json")
