"""Écran Stations.

À compléter : tableau des stations filtrable par commune, pagination.
"""

import streamlit as st
from api_client import ErreurApi, appeler_api

st.set_page_config(page_title="Stations - VéloVille", layout="wide")
st.title("Gestion des Stations")

if not st.session_state.get("jwt_token"):
    st.warning("Veuillez vous connecter sur la page d'accueil.")
    st.stop()

# Filtres de recherche
col1, col2 = st.columns([2, 1])
with col1:
    commune_filtre = st.text_input("Filtrer par commune")
with col2:
    taille_page = st.number_input(
        "Taille de page", min_value=1, max_value=100, value=20, step=1
    )

# Première requête pour connaître le nombre total de pages
params_init = {"page": 1, "taille_page": taille_page}
if commune_filtre.strip():
    params_init["commune"] = commune_filtre.strip()

try:
    data_init = appeler_api("GET", "/stations", params=params_init)
    max_pages = max(1, data_init.get("pages", 1))

    # Le sélecteur de page est borné par max_pages
    page = st.number_input(
        "Page", min_value=1, max_value=max_pages, value=1, step=1
    )

    # Récupération des données de la page sélectionnée si différente de la page 1
    if page != 1:
        params_page = params_init.copy()
        params_page["page"] = page
        data = appeler_api("GET", "/stations", params=params_page)
    else:
        data = data_init

    resultats = data.get("resultats", [])
    total = data.get("total", 0)

    st.write(f"**Total :** {total} station(s) trouvée(s) (Page {page}/{max_pages})")

    if resultats:
        st.dataframe(resultats, use_container_width=True)
    else:
        st.info("Aucune station trouvée.")

except ErreurApi as e:
    st.error(str(e))