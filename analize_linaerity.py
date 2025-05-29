import battle_engine as engine
from random import choice, randint
import matplotlib.pyplot as plt
import statistics


RED_TROOPS = ['archi', 'spade', 'asce', 'boss']
BLUE_TROOPS = ['archi', 'spade', 'asce']

MAX_DIMENSION = 9

DATA = {
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: []
}


def somma_lineare(stage: engine.Stage) -> int:
    battle_armies = [army.num for army in stage.armies]
    return sum(battle_armies)


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


for N in range(2, MAX_DIMENSION+1):
    for _ in range(10):
        Nstage = generate_Nstage(N)
        linear_sum = somma_lineare(Nstage)
        if linear_sum  != 0:
            real_sum = engine.best_result_from_stage(Nstage)[1].num
            DATA[N].append(real_sum/linear_sum)
        print(f"Done: {N}")



keys = sorted(DATA.keys())
values = [DATA[k] for k in keys]

print(DATA)

# Box plot
plt.figure(figsize=(10, 6))
plt.boxplot(values, labels=keys, showfliers=False)
plt.title('Box plot di DATA')
plt.grid(True)
plt.show()
    
    
    