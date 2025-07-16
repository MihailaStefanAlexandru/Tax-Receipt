import json
import pandas as pd
import joblib
from web3 import Web3

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
    print(f"Alertă trimisă, tx hash: {tx_hash.hex()}")

model = joblib.load("model_pipeline.pkl")

bon_nou = pd.DataFrame([{
    "Total_suma": 141.45,
    "Număr_produse": 2,
    "procent_TVA": 19,
    "minute_emitere": 210,
    "metoda_plata": "numerar",
    "Comerciant_id": "C0126"
}])

rezultat = model.predict(bon_nou)[0]

import hashlib

def gen_tx_id(bon_df: pd.DataFrame) -> str:
    text = "".join(str(v) for v in bon_df.iloc[0].values)
    return hashlib.sha256(text.encode()).hexdigest()[:10]

if rezultat == 1:
    tx_id = gen_tx_id(bon_nou)
    reason = "Bon suspect detectat de model AI"
    trimite_alerta(tx_id, reason)
else:
    print("Bonul este valid.")
