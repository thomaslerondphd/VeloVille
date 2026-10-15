"""Écran Indicateurs.

À compléter : trois st.metric et trois tableaux issus des trois endpoints
/indicateurs. Aucun graphique.
"""

import streamlit as st
import pandas as pd
from api_client import ErreurApi, appeler_api

st.set_page_config(page_title="Indicateurs - VéloVille", layout="wide")
st.title("Indicateurs Métiers")

if not st.session_state.get("jwt_token"):
    st.warning("Veuillez vous connecter sur la page d'accueil.")
    st.stop()

# 1. Activité par jour
st.subheader("Activité des trajets par jour")
col_d1, col_d2 = st.columns(2)
with col_d1:
    date_debut = st.date_input("Date de début", value=None)
with col_d2:
    date_fin = st.date_input("Date de fin", value=None)

params_act = {}
if date_debut:
    params_act["date_debut"] = str(date_debut)
if date_fin:
    params_act["date_fin"] = str(date_fin)

try:
    res_act = appeler_api("GET", "/indicateurs/activite-par-jour", params=params_act)
    df_act = pd.DataFrame(res_act.get("donnees", []))
    if not df_act.empty:
        st.dataframe(df_act, use_container_width=True)
        st.line_chart(df_act.set_index("jour"))
    else:
        st.info("Aucune donnée d'activité disponible sur la période.")
except ErreurApi as e:
    st.error(f"Activité : {str(e)}")

st.divider()

# 2. Stations actives
st.subheader("Top des stations les plus actives")
col_s1, col_s2 = st.columns(2)
with col_s1:
    limite = st.slider("Nombre de stations", min_value=1, max_value=50, value=10)
with col_s2:
    tri = st.selectbox("Critère de tri", options=["tout", "departs", "arrivees"])

try:
    res_stat = appeler_api(
        "GET", "/indicateurs/stations-actives", params={"limite": limite, "tri": tri}
    )
    df_stat = pd.DataFrame(res_stat.get("donnees", []))
    if not df_stat.empty:
        st.dataframe(df_stat, use_container_width=True)
    else:
        st.info("Aucune donnée de station disponible.")
except ErreurApi as e:
    st.error(f"Stations actives : {str(e)}")

st.divider()

# 3. Incidents par statut
st.subheader("Répartition et résolution des incidents")
try:
    res_inc = appeler_api("GET", "/indicateurs/incidents-par-statut")
    delai = res_inc.get("delai_moyen_resolution_heures")

    if delai is not None:
        st.metric("Délai moyen de résolution", f"{delai} heures")
    else:
        st.metric("Délai moyen de résolution", "Aucun incident résolu")

    df_inc = pd.DataFrame(res_inc.get("donnees", []))
    if not df_inc.empty:
        st.table(df_inc)
    else:
        st.info("Aucun incident enregistré.")
except ErreurApi as e:
    st.error(f"Incidents : {str(e)}")