"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""

import streamlit as st
from api_client import ErreurApi, appeler_api

st.set_page_config(page_title="Incidents - VéloVille", layout="wide")
st.title("Gestion des Incidents")

if not st.session_state.get("jwt_token"):
    st.warning("Veuillez vous connecter sur la page d'accueil.")
    st.stop()

user_role = st.session_state.get("role")

# Visualisation des incidents
st.subheader("Liste des incidents")
col1, col2 = st.columns([2, 1])
with col1:
    commune_filtre = st.text_input("Filtrer par commune")
with col2:
    taille_page = st.number_input(
        "Taille de page", min_value=1, max_value=100, value=20, step=1
    )

# Requête initiale pour déterminer la limite de pages
params_init = {"page": 1, "taille_page": taille_page}
if commune_filtre.strip():
    params_init["commune"] = commune_filtre.strip()

try:
    data_init = appeler_api("GET", "/incidents", params=params_init)
    max_pages = max(1, data_init.get("pages", 1))

    page = st.number_input(
        "Page", min_value=1, max_value=max_pages, value=1, step=1
    )

    if page != 1:
        params_page = params_init.copy()
        params_page["page"] = page
        data = appeler_api("GET", "/incidents", params=params_page)
    else:
        data = data_init

    incidents = data.get("resultats", [])
    st.write(f"**Total :** {data.get('total', 0)} incident(s) (Page {page}/{max_pages})")
    st.dataframe(incidents, use_container_width=True)

    # Fonctionnalité réservée au rôle exploitant
    if user_role == "exploitant":
        st.divider()
        st.subheader("Mise à jour d'un statut d'incident")

        with st.form("form_statut"):
            incident_id = st.text_input("Identifiant de l'incident")
            nouveau_statut = st.selectbox(
                "Nouveau statut", options=["en_cours", "resolu"]
            )
            valider = st.form_submit_button("Mettre à jour")

        if valider:
            if not incident_id:
                st.warning("Veuillez renseigner un ID d'incident.")
            else:
                try:
                    res = appeler_api(
                        methode="PUT",
                        endpoint=f"/incidents/{incident_id}/statut",
                        json_data={"statut": nouveau_statut},
                    )
                    st.success(f"Statut de l'incident {incident_id} mis à jour avec succès !")
                    st.rerun()
                except ErreurApi as e:
                    st.error(str(e))

except ErreurApi as e:
    st.error(str(e))