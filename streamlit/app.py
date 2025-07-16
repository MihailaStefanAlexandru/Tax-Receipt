import streamlit as st
import joblib
import numpy as np
import pandas as pd
import hashlib
import json
from web3 import Web3

# adrese si chei
CONTRACT_ADDRESS = "0x86cAA25a689384d15982c5A5e995518F8Af06167"
PRIVATE_KEY = "43873b9b2019681b66ed8b235ca1d9abdebcd1f02b7cb7dbecf4c15b6b6f089d"
WALLET_ADDRESS = "0x947cDfB33eCbcDC3980120D526E0cd81731c4A2A"
ganache_url = "http://172.17.240.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("Conectarea a esuat")

with open("FraudLog_ABI.json", "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def trimite_alerta(txId: str, reason: str):
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

    txn = contract.functions.reportFraud(txId, reason).build_transaction({
        'chainId': 1337,
        'gas': 300000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': nonce,
    })

    semnata = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(semnata.raw_transaction)
    return tx_hash.hex()

def gen_tx_id(bon_df: pd.DataFrame) -> str:
    text = "".join(str(v) for v in bon_df.iloc[0].values)
    return hashlib.sha256(text.encode()).hexdigest()[:10]

# incarcare model si scaller
model = joblib.load("model_pipeline.pkl")

st.title("Detectarea Fraudelor pentru Bonurile Fiscale")

st.markdown("Introduceți datele bonului pentru a prezice dacă este fraudulos sau nu.")

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
input = pd.DataFrame([{
    "Total_suma": total_suma,
    "Număr_produse": numar_produse,
    "procent_TVA": procent_tva,
    "minute_emitere": ora_emitere * 60 + minut_emitere,
    "metoda_plata": metoda_plata,
    "Comerciant_id": comerciant_id
}])

if st.button("Prezice bonul"):

    pred = model.predict(input)[0]
    prob = model.predict_proba(input)[0][1]

    if pred == 1:
        st.error(f"Bonul este probabil fraudulos (probabilitate: {prob:.2f})")

        tx_id = gen_tx_id(input)
        reason = "Bon suspect detectat de model AI"
        try:
            tx_hash = trimite_alerta(tx_id, reason)
            st.success(f"Alertă trimisă pe blockchain! Tx hash: {tx_hash}")
        except Exception as e:
            st.error(f"Eroare la trimiterea alertei: {str(e)}")

    else:
        st.success(f"Bonul pare în regulă (probabilitate fraudă: {prob:.2f})")