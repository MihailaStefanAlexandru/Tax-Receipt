import streamlit as st
import joblib
import numpy as np

# incarcare model si scaller
model = joblib.load("model_rf.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Detectarea Fraudelor pentru Bonurile Fiscale")

st.markdown("Introduceți datele bonului pentru a prezice dacă este **fraudulos** sau nu.")

# input utilizator
total_suma = st.number_input("Total sumă (RON)", min_value=0.0, step=0.1)
numar_produse = st.number_input("Număr produse", min_value=1, step=1)
procent_tva = st.selectbox("Procent TVA", [9, 19])
ora_emitere = st.slider("Ora emiterii", 0, 23, 12)
minut_emitere = st.slider("Minutul emiterii", 0, 59, 30)
metoda_plata = st.selectbox("Metoda de plată", ["numerar", "card", "tichete", "transfer"])
comerciant_id = st.selectbox("Comerciant ID", [f"C{str(i).zfill(4)}" for i in range(1, 201)])

# mapare categorii
metoda_map = {"numerar": 0, "card": 1, "tichete": 2, "transfer": 4}
comerciant_map = {f"C{str(i).zfill(4)}": i for i in range(1, 201)}

# input array
input_raw = np.array([[
    total_suma,
    numar_produse,
    procent_tva,
    ora_emitere * 60 + minut_emitere,
    metoda_map[metoda_plata],
    comerciant_map[comerciant_id]
]])

input_scaled = input_raw

if st.button("Prezice bonul"):

    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]

    if pred == 1:
        st.error(f"Bonul este probabil fraudulos (probabilitate: {prob:.2f})")
    else:
        st.success(f"Bonul pare în regulă (probabilitate fraudă: {prob:.2f})")