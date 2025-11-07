import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Menú | Fame Focaccias", page_icon="📖", layout="wide")

st.title("📖 Menú de Focaccias")

data_path = Path("data/menu.json")
data = json.loads(data_path.read_text(encoding="utf-8")) if data_path.exists() else {}

st.caption("Precios en EUR. Ingredientes frescos y AOVE de calidad.")

for categoria, items in data.items():
    st.header(categoria)
    for item in items:
        with st.container(border=True):
            left, right = st.columns([4, 1])
            with left:
                st.subheader(item["nombre"])
                if item.get("descripcion"):
                    st.write(item["descripcion"])
            with right:
                st.markdown(f"### {item['precio']:.2f} €")
