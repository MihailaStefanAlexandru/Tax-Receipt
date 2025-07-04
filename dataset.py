import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

nr_bonuri = 10000

metode_plata = ["numerar", "card", "tichete", "transfer"]
tva_posibil = [9, 19]
comercianti = [f"C{str(i).zfill(4)}" for i in range(1, 201)]

# comercianti considerati "risc ridicat"
comercianti_risc = set(random.sample(comercianti, 10))

# functie pentru generarea campului "Oră_emitere"
def genereaza_ore():
    ora_random = datetime(2025, 1, 1) + timedelta(seconds=np.random.randint(0, 86400))
    return ora_random.strftime('%H:%M:%S')

def verifica_frauda(bon):
    
    motive = []
    ora = datetime.strptime(bon["Oră_emitere"], "%H:%M:%S").time()

    if bon["Total_suma"] > 500 and bon["Număr_produse"] <= 2:
        motive.append("suma_mare_putine_produse")

    if ora >= datetime.strptime("00:00:00", "%H:%M:%S").time() and ora <= datetime.strptime("05:00:00", "%H:%M:%S").time():
        motive.append("emitere_noaptea")

    if bon["metoda_plata"] == "numerar" and bon["Total_suma"] > 300:
        motive.append("numerar_prea_mare")

    if bon["Comerciant_id"] in comercianti_risc:
        motive.append("comerciant_risc")

    if bon["procent_TVA"] == 5 and bon["Total_suma"] > 200:
        motive.append("tva_mic_suma_mare")

    return motive

# functie pentru generarea bonurilor
def genereaza_bon():

    numar_produse = np.random.poisson(5) + 1
    pret_mediu = np.random.uniform(5, 50)
    total = round(numar_produse * pret_mediu, 2)

    tva = np.random.choice(tva_posibil)
    metoda = np.random.choice(metode_plata)
    ora_emitere = genereaza_ore()
    comerciant = np.random.choice(comercianti)

    bon = {
        "Total_suma": total,
        "Număr_produse": numar_produse,
        "procent_TVA": tva,
        "metoda_plata": metoda,
        "Oră_emitere": ora_emitere,
        "Comerciant_id": comerciant
    }

    motive = verifica_frauda(bon)
    bon["eticheta"] = "fraudulent" if motive else "non-fraudulent"
    bon["motiv_frauda"] = ";".join(motive) if motive else ""
    
    return bon

# generare bonuri
bonuri = [genereaza_bon() for _ in range(nr_bonuri)]
df = pd.DataFrame(bonuri)

# salvare bonuri
df.to_csv("bonuri_fiscale.csv", index="False")

# salvare bonuri frauduloase separat cu motivul
df_fraud = df[df["eticheta"] == "fraudulent"]
df_fraud.to_csv("bonuri_frauduloase.csv", index=False)

print(f"Total bonuri frauduloase: {len(df_fraud)} / {nr_bonuri}")
print(df_fraud.head())