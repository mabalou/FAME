# auth.py
import streamlit as st

def check_password():
    """Verifica la contraseña y mantiene sesión activa hasta que se cierre la pestaña."""
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False

    if st.session_state.auth_ok:
        return True

    password = st.text_input("Introduce la contraseña", type="password")

    if password:
        if password == st.secrets["password"]:
            st.session_state.auth_ok = True
            st.success("✅ Acceso concedido")
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")

    return False


def logout():
    """Cierra sesión."""
    st.session_state.clear()
    st.success("🔒 Sesión cerrada")
    st.rerun()
