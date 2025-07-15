import streamlit as st

def login():
    st.title("Login")
    with st.form("Login_form"):
        user = st.text_input("Usuário:")
        pw = st.text_input("Senha:", type="password")
        dsn = st.text_input("String:")
        submitted = st.form_submit_button("Logar")

    if submitted:
        if not user or not pw or not dsn:
            st.error("Preencha todos os campos!")
        else:
            st.success(f"Bem-vindo, {user}!")
            st.session_state.user = user
            st.session_state.pw = pw
            st.session_state.dsn = dsn
    
    if "user" in st.session_state:
        st.write(f"Usuario atual: **{st.session_state.user}**")
        return st.session_state.user, st.session_state.pw, st.session_state.dsn
    
    return None, None, None
