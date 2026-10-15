"""Page d'accueil Streamlit : connexion.

À compléter : formulaire identifiant / mot de passe, appel de POST /auth/login via
api_client, stockage du jeton et du rôle dans st.session_state,
message d'erreur en français en cas d'échec.

Lancement : streamlit run front/app.py
"""

import streamlit as st
from api_client import ErreurApi, appeler_api

st.set_page_config(page_title="VéloVille", layout="centered")

if "jwt_token" not in st.session_state:
    st.session_state["jwt_token"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

st.title("VéloVille")
st.caption("L'application de gestion des vélos en libre-service de la ville -- ver.1.0.0")

if st.session_state["jwt_token"]:
    st.success(
        f"Connecté en tant que **{st.session_state['username']}** (Rôle : `{st.session_state['role']}`)"
    )
    if st.button("Se déconnecter"):
        st.session_state["jwt_token"] = None
        st.session_state["role"] = None
        st.session_state["username"] = None
        st.rerun()
else:
    st.subheader("Authentification")
    with st.form("form_connexion"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        soumis = st.form_submit_button("Se connecter")

    if soumis:
        if not username or not password:
            st.warning("Veuillez remplir tous les champs.")
        else:
            try:
                res = appeler_api(
                    methode="POST",
                    endpoint="/auth/login",
                    json_data={"username": username, "password": password},
                    auth_requis=False,
                )
                st.session_state["jwt_token"] = res["access_token"]
                st.session_state["role"] = res["role"]
                st.session_state["username"] = username
                st.success(f"Connexion réussie ! Rôle : {res['role']}")
                st.rerun()
            except ErreurApi as e:
                st.error(str(e))