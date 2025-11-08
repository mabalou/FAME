import streamlit as st
import json
from pathlib import Path
from streamlit_sortables import sort_items

st.set_page_config(page_title="🔒 Admin Fame", layout="wide")

# --- Cargar CSS ---
css_path = Path("assets/style.css")
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- ENCABEZADO ----------------
st.title("🔒 Panel de gestión del menú")

# --- Botón para salir del modo admin ---
col_exit, _ = st.columns([1, 5])
with col_exit:
    if st.button("🚪 Salir del modo admin"):
        st.session_state.auth_ok = False
        st.success("Has salido del modo administrador 👋")
        st.rerun()

# --- Contraseña ---
pwd = st.text_input("Contraseña", type="password", placeholder="Introduce la contraseña para editar el menú")
if pwd != st.secrets.get("admin_password", None):
    st.warning("Introduce la contraseña correcta para acceder.")
    st.stop()

st.success("Acceso concedido ✅")

# --- Cargar archivo del menú ---
menu_file = Path("data/menu.json")
if not menu_file.exists():
    st.error("No se encontró el archivo menu.json.")
    st.stop()

menu = json.loads(menu_file.read_text(encoding="utf-8"))

# --- Estado temporal ---
if "menu_temp" not in st.session_state:
    st.session_state.menu_temp = menu
if "move_action" not in st.session_state:
    st.session_state.move_action = None
if "delete_action" not in st.session_state:
    st.session_state.delete_action = None

st.markdown("### 🧰 Edición del menú")

# 💾 Botón global para guardar todo
if st.button("💾 Guardar todo el menú"):
    try:
        menu_file.write_text(
            json.dumps(st.session_state.menu_temp, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        st.session_state["saved"] = True
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")

if st.session_state.get("saved", False):
    st.success("✅ Todos los cambios se han guardado correctamente.")
    st.session_state["saved"] = False

# --- Ordenar secciones ---
st.markdown("### 🧱 Ordenar secciones del menú")

sections = list(st.session_state.menu_temp.keys())
ordered_sections = sort_items(
    [f"🍽️ {s}" for s in sections],
    direction="vertical",
    key="sort_sections"
)

if [s.replace("🍽️ ", "") for s in ordered_sections] != sections:
    new_order = {s.replace("🍽️ ", ""): st.session_state.menu_temp[s.replace('🍽️ ', '')] for s in ordered_sections}
    st.session_state.menu_temp = new_order
    st.success("✅ Secciones reordenadas correctamente")
    st.rerun()

# --- Edición de productos ---
for section, items in st.session_state.menu_temp.items():
    with st.expander(f"🍽️ {section}", expanded=False):
        st.markdown("🖱️ Arrastra los productos para cambiar el orden:")

        # Drag & drop visual
        display_items = [
            f"🍕 {item['nombre']} — {item['precio']}€<br><small>{item['descripcion']}</small>"
            for item in items
        ]
        sorted_list = sort_items(
            display_items,
            direction="vertical",
            key=f"sortable_{section}"
        )

        # Si cambia el orden → actualizamos
        if sorted_list != display_items:
            new_order = []
            for item_html in sorted_list:
                nombre = item_html.split("—")[0].replace("🍕", "").strip()
                for obj in items:
                    if obj["nombre"] == nombre:
                        new_order.append(obj)
                        break
            st.session_state.menu_temp[section] = new_order
            st.success(f"✅ Orden actualizado en {section}")
            st.rerun()

        # ---------------- Edición detallada ----------------
        st.markdown("### ✏️ Editar productos")
        for i, item in enumerate(st.session_state.menu_temp[section]):
            st.markdown("---")
            item["nombre"] = st.text_input("Nombre", value=item.get("nombre", ""), key=f"nombre_{section}_{i}")
            item["descripcion"] = st.text_area("Descripción", value=item.get("descripcion", ""), key=f"desc_{section}_{i}")
            item["precio"] = st.number_input("Precio (€)", value=float(item.get("precio", 0)), step=0.1, key=f"precio_{section}_{i}")

            # --- Botón eliminar seguro ---
            if st.button(f"🗑️ Eliminar '{item['nombre']}'", key=f"del_{section}_{i}"):
                st.session_state.delete_action = (section, i)

        # --- Procesar eliminación después del render ---
        if st.session_state.delete_action:
            section, idx = st.session_state.delete_action
            if idx < len(st.session_state.menu_temp[section]):
                nombre = st.session_state.menu_temp[section][idx]['nombre']
                st.session_state.menu_temp[section].pop(idx)
                st.warning(f"Producto '{nombre}' eliminado de {section} ❌")
            st.session_state.delete_action = None
            st.rerun()

        # --- Añadir / guardar por sección ---
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"➕ Añadir producto a {section}", key=f"add_{section}"):
                st.session_state.menu_temp[section].append({
                    "nombre": "Nuevo producto",
                    "precio": 0,
                    "descripcion": ""
                })
                st.success(f"Producto añadido a {section} ✅")
                st.rerun()
        with col2:
            if st.button(f"💾 Guardar {section}", key=f"save_{section}"):
                try:
                    menu_file.write_text(
                        json.dumps(st.session_state.menu_temp, ensure_ascii=False, indent=2),
                        encoding="utf-8"
                    )
                    st.success(f"Sección '{section}' guardada correctamente ✅")
                except Exception as e:
                    st.error(f"No se pudo guardar '{section}': {e}")

# --- Vista previa ---
st.markdown("### 🧾 Vista previa actual del menú")
st.code(json.dumps(menu, ensure_ascii=False, indent=2), language="json")
