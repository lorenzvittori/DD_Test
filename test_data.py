import csv
import battle_engine as engine

# Funzione per leggere CSV e creare Army
def load_armies_from_csv(filename):
    armies_per_row = []
    with open(filename, newline='') as csvfile:  
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader, start=1):
            if len(row) != 6:
                continue  # salta righe malformate
            try:
                # Parsing: ogni 2 elementi formano un'armata
                army1 = engine.Army(int(row[0].strip()), row[1].strip())
                army2 = engine.Army(int(row[2].strip()), row[3].strip())
                army3 = engine.Army(int(row[4].strip()), row[5].strip())
                armies_per_row.append((army1, army2, army3))
            except: continue
    return armies_per_row

def verify_combat(army1: engine.Army, army2: engine.Army, army3: engine.Army):
    result = engine.single_combat(army1, army2)
    match = result == army3
    if not(match):
        print(f"Dati: {army1} + {army2} -> {army3}")
        print(f"Calcolo: {army1} + {army2} -> {result}")
        print("----------")
        return
    else: print("ok")
    

list_of_test = load_armies_from_csv("result_tester.csv")
print("-------------------------------------------------------")
    
for el in list_of_test:
    verify_combat(*el)
    