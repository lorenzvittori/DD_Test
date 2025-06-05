import battle_engine as engine
from random import choice, randint
import time

RED_TROOPS = ['archi', 'spade', 'asce', 'boss']
BLUE_TROOPS = ['archi', 'spade', 'asce']

MAX_DIMENSION = 9



def generate_Nstage(N, MAX_NUM_ARMY = 150):
    stage_generated = engine.Stage([])
    for _ in range(N):
        blue_or_red = choice([-1, 1])
        num_army = blue_or_red*randint(1, 120)
        if blue_or_red == 1:
            troop_army = choice(BLUE_TROOPS)
        else:
            troop_army = choice(RED_TROOPS)
        stage_generated.add_army(engine.Army(num_army, troop_army))
    return stage_generated

"""
for N in range(2, MAX_DIMENSION+1):
    print(f"Lunghezza {N}")
    for _ in range(5000):
        Nstage = generate_Nstage(N)
        cutted_result = engine.best_result_from_stage_with_cut(Nstage)[1].num
        real_result = engine.best_result_from_stage(Nstage)[1].num
        if not((cutted_result==real_result)): 
            cutted_result_stage, cutted_result_army = engine.best_result_from_stage_with_cut(Nstage)
            real_result_stage, real_result_army = engine.best_result_from_stage(Nstage)
            print(engine.Battle(cutted_result_stage), " | ", engine.Battle(real_result_stage))
            break
"""
  


tempi_f = []
tempi_g = []


N = 20
for _ in range(N):
    x = generate_Nstage(8)

    # Copia l'input per evitare effetti collaterali tra f e g
    x1 = x.copy()
    x2 = x.copy()

    # Tempo per f
    start_f = time.perf_counter()
    real_result = engine.best_result_from_stage_with_cut(x1)[1].num
    
    end_f = time.perf_counter()
    tempi_f.append(end_f - start_f)

    # Tempo per g
    start_g = time.perf_counter()
    cutted_result = engine.best_result_from_stage(x2)[1].num
    end_g = time.perf_counter()
    tempi_g.append(end_g - start_g)
    print(_)

# Risultati medi
media_f = sum(tempi_f) / N
media_g = sum(tempi_g) / N

print(f"Tempo medio with cut: {media_f:.6f} secondi")
print(f"Tempo medio normal: {media_g:.6f} secondi")
