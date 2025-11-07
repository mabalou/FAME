import streamlit as st
from pathlib import Path
import base64

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🍞 Fame", layout="wide")

# Estado global
if "current_page" not in st.session_state:
    st.session_state.current_page = "Inicio"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "lang" not in st.session_state:
    st.session_state.lang = "es"

# Query params
qp = st.query_params
if qp.get("page"):
    st.session_state.current_page = qp["page"]
if qp.get("theme"):
    st.session_state.theme = qp["theme"]
if qp.get("lang"):
    st.session_state.lang = qp["lang"]

lang = st.session_state.lang
theme = st.session_state.theme
other_theme = "dark" if theme == "light" else "light"
other_lang = "gl" if lang == "es" else "es"

# Textos (ES/GL)
TEXTS = {
    "es": {
        "inicio": "Inicio", "menu": "Menú", "order": "🍕 Pide aquí!",
        "follow": "📸 Síguenos!", "maps": "📍 Encuéntranos aquí",
        "light": "☀️ Claro", "dark": "🌙 Oscuro", "lang_name": "🌐 Galego",
        "welcome": "🍞 Fame",
        "desc": "Artesanas • Frescas • Ingredientes de primera calidad<br>Descubre nuestras focaccias saladas y dulces, preparadas al momento con ingredientes locales.",
        "time": "Tiempo medio de pedido", "rating": "Valoración media",
        "made": "Hecho en", "location": "Santiago de Compostela",
        "footer": "© 2025 Fame — Sitio hecho con Streamlit",
    },
    "gl": {
        "inicio": "Inicio", "menu": "Carta", "order": "🍕 Pide aquí!",
        "follow": "📸 Séguenos!", "maps": "📍 Atópanos aquí",
        "light": "☀️ Claro", "dark": "🌙 Escuro", "lang_name": "🌐 Castellano",
        "welcome": "🍞 Fame",
        "desc": "Artesás • Frescas • Ingredientes de primeira calidade<br>Descubre as nosas focaccias salgadas e doces, preparadas ao momento con ingredientes locais.",
        "time": "Tempo medio do pedido", "rating": "Valoración media",
        "made": "Feito en", "location": "Santiago de Compostela",
        "footer": "© 2025 Fame — Sitio feito con Streamlit",
    },
}

# ---------- Ocultar UI nativa ----------
st.markdown("""
<style>
[data-testid="stSidebar"]{display:none}
header[data-testid="stHeader"],section[data-testid="stToolbar"]{display:none!important}
div.block-container{padding-left:3rem;padding-right:3rem;max-width:1500px}
</style>
""", unsafe_allow_html=True)

# Páginas
PAGES = {"Inicio": "Inicio", "Menú": "1_Menu"}

# ---------- Tema / Colores ----------
light_override = (
    ":root{"
    "--bg-color:#fcf9f7;"
    "--text-color:#1a1a1a;"
    "--menu-bg:rgba(255,255,255,.9);"
    "--menu-link:#b92e2e;"
    "--menu-active:#a11f1f;"
    "--switch-bg:#bbb;"
    "--switch-ball:#c94c4c;"
    "--metric-text:#1a1a1a;"
    "}"
) if theme == "light" else ""

# ---------- Construcción del menú ----------
menu_html = ""
for page_name, page_file in PAGES.items():
    active_class = "active" if st.session_state.current_page == page_name else ""
    label = TEXTS[lang]['inicio'] if page_name == "Inicio" else TEXTS[lang]['menu']
    menu_html += f'<a class="menu-link {active_class}" href="?page={page_name}&theme={theme}&lang={lang}" target="_self" onclick="closeMenu()">{label}</a>'

# ---------- CSS y cabecera ----------
st.markdown(f"""
<style>
:root{{
  --bg-color:#0e1117;--text-color:#fff;--menu-bg:rgba(20,20,20,.85);
  --menu-link:#c94c4c;--menu-active:#ff9999;--switch-bg:#444;--switch-ball:#ffb3b3;
  --metric-text:#fff;
}}
{light_override}

[data-testid="stAppViewContainer"]{{background:var(--bg-color);color:var(--text-color);
transition:background-color .3s,color .3s}}
[data-testid="stAppViewContainer"],p,label,h1,h2,h3,h4,h5,h6,span{{color:var(--text-color)!important}}

.header-bar{{position:fixed;top:0;left:0;right:0;z-index:9999;display:flex;flex-direction:column;
align-items:center;justify-content:center;padding:.6rem 2rem;background:var(--menu-bg);
backdrop-filter:blur(10px);box-shadow:0 4px 14px rgba(0,0,0,.2)}}
div.block-container{{padding-top:5.5rem!important}}

.menu-links{{display:flex;gap:1.8rem;flex-wrap:wrap;align-items:center;justify-content:center;margin-bottom:.4rem}}
.menu-link{{font-size:1.05rem;font-weight:600;text-decoration:none!important;color:var(--menu-link)!important;
border-bottom:2px solid transparent;transition:all .25s}}
.menu-link:hover,.menu-link.active{{color:var(--menu-active)!important;border-bottom:2px solid var(--menu-active)}}

.menu-btn{{background:var(--menu-link);color:#fff!important;font-weight:600;padding:6px 16px;border-radius:25px;
text-decoration:none!important;border:1px solid rgba(255,255,255,.15);transition:all .25s}}
.menu-btn:hover{{background:var(--menu-active);transform:translateY(-1px)}}

.tools{{display:flex;align-items:center;gap:18px;justify-content:center}}
.theme-toggle,.lang-toggle{{
    display:flex;align-items:center;gap:8px;background:var(--menu-bg);
    border-radius:30px;padding:6px 12px;border:1px solid rgba(255,255,255,.2);
    color:var(--menu-link)!important;text-decoration:none!important;
}}
.theme-toggle span,.lang-toggle span{{text-decoration:none!important}}
.switch{{position:relative;width:46px;height:24px;background:var(--switch-bg);border-radius:24px}}
.switch::before{{content:"";position:absolute;top:2px;left:2px;width:20px;height:20px;background:var(--switch-ball);border-radius:50%;transition:transform .25s}}
.switch.on::before{{transform:translateX(22px)}}

/* 📱 Móvil */
.menu-toggle {{display:none;}} /* 🔥 Oculto en escritorio */
@media (max-width: 768px) {{
  .header-bar {{align-items:flex-start;padding:0.8rem 1.2rem;}}
  .menu-toggle {{display:block;cursor:pointer;font-size:1.4rem;font-weight:700;
    color:var(--menu-link);user-select:none;margin-bottom:0.4rem;}}
  .menu-links {{display:none;flex-direction:column;align-items:flex-start;gap:0.6rem;
    width:100%;background:var(--menu-bg);padding:0.5rem 0;border-radius:10px;animation:slideDown .3s ease;}}
  @keyframes slideDown {{from{{opacity:0;transform:translateY(-8px);}}to{{opacity:1;transform:translateY(0);}}}}
  #menuChk:checked + label.menu-toggle + .menu-links {{display:flex;}}
  .menu-link,.menu-btn {{width:100%;text-align:left;padding-left:0.6rem;}}
  .tools {{width:100%;justify-content:space-between;margin-top:0.5rem;}}
  div.block-container {{padding-top:6.5rem!important;}}
}}
#menuChk {{display:none;}}
div[data-testid="stMetricValue"],div[data-testid="stMetricLabel"]{{color:var(--metric-text)!important}}
</style>

<script>
function closeMenu() {{
  const chk = document.getElementById('menuChk');
  if (chk) chk.checked = false;
}}
document.addEventListener('click', function(e) {{
  const menu = document.querySelector('.header-bar');
  const chk = document.getElementById('menuChk');
  if (chk && !menu.contains(e.target)) chk.checked = false;
}});
</script>

<div class="header-bar">
  <input type="checkbox" id="menuChk" />
  <label for="menuChk" class="menu-toggle">☰ Menú</label>

  <div class="menu-links">
    {menu_html}
    <a class="menu-btn" href="https://www.just-eat.es/restaurants-fame-santiago-de-compostela/" target="_blank" onclick="closeMenu()">{TEXTS[lang]['order']}</a>
    <a class="menu-btn" href="https://www.instagram.com/moitafame/" target="_blank" onclick="closeMenu()">{TEXTS[lang]['follow']}</a>
    <a class="menu-btn" href="https://maps.app.goo.gl/d72Zn8c7V4UaLkNa7" target="_blank" onclick="closeMenu()">{TEXTS[lang]['maps']}</a>
  </div>

  <div class="tools">
    <a href="?page={st.session_state.current_page}&theme={other_theme}&lang={lang}" target="_self" class="theme-toggle">
      <div class="switch {'on' if theme=='light' else ''}"></div>
      <span>{TEXTS[lang]['light'] if theme=='light' else TEXTS[lang]['dark']}</span>
    </a>
    <a href="?page={st.session_state.current_page}&theme={theme}&lang={other_lang}" target="_self" class="lang-toggle">
      <span>{TEXTS[lang]['lang_name']}</span>
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- NAVEGACIÓN ----------
selected = PAGES[st.session_state.current_page]
if selected != "Inicio":
    try:
        exec(Path(f"pages/{selected}.py").read_text(), globals())
        st.stop()
    except FileNotFoundError:
        st.error("Página no encontrada.")
        st.stop()

# ---------- CONTENIDO INICIO ----------
logo = Path("assets/FAME.png")
if logo.exists():
    img_b64 = base64.b64encode(logo.read_bytes()).decode()
    st.markdown(f"""
    <div style='text-align:center;margin-top:.2rem;'>
        <img src="data:image/png;base64,{img_b64}" width="340" style="border-radius:20px;"/>
        <h1 style='font-weight:800;margin-top:1rem;'>{TEXTS[lang]['welcome']}</h1>
        <p style='font-size:1.15rem;line-height:1.6em;max-width:850px;margin:auto;'>
          {TEXTS[lang]['desc']}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(TEXTS[lang]['time'], "15–20 min")
with c2:
    st.metric(TEXTS[lang]['rating'], "⭐️⭐️⭐️⭐️⭐️")
with c3:
    st.metric(TEXTS[lang]['made'], TEXTS[lang]['location'])

st.caption(TEXTS[lang]['footer'])
