import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils import total_visitas

st.set_page_config(page_title="📊 Analítica Fame", layout="wide")
st.markdown("## 📈 Analítica de visitas")

# --- Verificación con contraseña ---
pwd = st.text_input("Contraseña", type="password", placeholder="Introduce la contraseña para ver las estadísticas")
if pwd != st.secrets.get("admin_password", None):
    st.warning("Introduce la contraseña correcta para acceder.")
    st.stop()

st.success("Acceso concedido ✅")

# --- Archivo de datos ---
csv_path = Path("data/visitas.csv")
if not csv_path.exists():
    st.warning("Todavía no hay visitas registradas.")
    st.stop()

# Leer CSV
df = pd.read_csv(csv_path)

# Limpieza mínima
if "fecha" not in df.columns:
    st.error("El archivo CSV no tiene el formato esperado.")
    st.stop()

# --- Métricas principales ---
col1, col2, col3 = st.columns(3)
col1.metric("👀 Total de visitas", len(df))
col2.metric("📄 Páginas distintas", df["pagina"].nunique())
col3.metric("🌍 Países únicos", df["pais"].nunique())

# --- Últimas visitas ---
st.markdown("### 🕒 Últimas 10 visitas")
st.dataframe(df.tail(10), use_container_width=True)

# --- Descarga del CSV ---
st.download_button(
    "⬇️ Descargar registros completos (CSV)",
    csv_path.read_bytes(),
    file_name="visitas_fame.csv",
    mime="text/csv"
)

# --- Gráficas ---
st.markdown("### 📊 Estadísticas visuales")

# 📅 Visitas por fecha
visitas_fecha = df.groupby("fecha").size()
plt.figure()
visitas_fecha.plot(kind="bar")
plt.title("Visitas por día")
plt.xlabel("Fecha")
plt.ylabel("Número de visitas")
st.pyplot(plt)

# ⏰ Visitas por hora
if "hora" in df.columns:
    df["hora_sola"] = df["hora"].astype(str).str[:2]
    visitas_hora = df.groupby("hora_sola").size()
    plt.figure()
    visitas_hora.plot(kind="bar", color="#c94c4c")
    plt.title("Visitas por hora del día")
    plt.xlabel("Hora")
    plt.ylabel("Número de visitas")
    st.pyplot(plt)

# 📍 Ciudades más frecuentes
if "ciudad" in df.columns:
    top_ciudades = df["ciudad"].value_counts().head(10)
    plt.figure()
    top_ciudades.plot(kind="barh", color="#a11f1f")
    plt.title("Ciudades más frecuentes")
    plt.xlabel("Número de visitas")
    st.pyplot(plt)

# 🗂️ Páginas más vistas
paginas = df["pagina"].value_counts()
plt.figure()
paginas.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["#c94c4c", "#b92e2e", "#ff9999"])
plt.title("Distribución por página")
st.pyplot(plt)

# --- Total de visitas (contador pequeño) ---
st.markdown(
    f"<div class='counter-badge'>👀 {total_visitas()} visitas</div>",
    unsafe_allow_html=True
)

# --- 🌍 MAPA INTERACTIVO DE VISITAS ---
import pydeck as pdk

if "coordenadas" in df.columns and df["coordenadas"].notna().any():
    try:
        coords = df["coordenadas"].dropna().str.split(",", expand=True)
        coords.columns = ["lat", "lon"]
        coords["lat"] = coords["lat"].astype(float)
        coords["lon"] = coords["lon"].astype(float)

        st.markdown("### 🌍 Mapa de visitas")
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=coords,
            get_position=["lon", "lat"],
            get_color=[185, 46, 46, 160],
            get_radius=20000,
        )
        view_state = pdk.ViewState(latitude=coords["lat"].mean(), longitude=coords["lon"].mean(), zoom=4)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    except Exception as e:
        st.warning(f"No se pudo generar el mapa: {e}")
