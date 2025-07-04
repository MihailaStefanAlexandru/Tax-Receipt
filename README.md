# Detectarea Fraudelor pentru Bonuri Fiscale

## Obiectiv general

Dezvoltarea unui model AI care clasifică bonurile fiscale în legitime sau potențial frauduloase pe baza caracteristicilor tranzacției.

## Tehnologii & instrumente:

| Biblioteca | Descriere | Utilizare | Link |
| ---------- | --------- | --------- | ---- |

## Set de date

Setul de date a fost generat folosind scriptul dataset.py astfel încât să respecte următorul format:

- Total_suma
- Număr_produse
- procent_TVA
- metodă_plată
- Oră_emitere
- Comerciant_id
- eticheta: fraudulent / non-fraudulent

## Etapele

1. [x] Importul și preprocesarea datelor
2. [x] Explorarea datelor (EDA):

    - Histogramă cu sume
    - Bonuri suspecte după oră
    - Corelații între număr produse și sumă

3. [x] Împărțirea setului de date (train/test)
4. [x] Antrenarea modelului
5. [x] Evaluare și interpretare
6. [x] Testare cu date noi
7. [x] Interfață simplă cu Streamlit/React

## Rezultat final

Un mic sistem AI care poate detecta tranzacții suspecte și care poate fi extins cu:

- logging în fișier JSON/CSV
- integrare cu un contract inteligent pentru înregistrare imaubila
- UI web pentru testare în timp real