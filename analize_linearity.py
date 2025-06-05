import battle_engine as engine
from random import choice, randint, sample
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

def mean(l):
    return sum(l)/len(l)


def somma_lineare(stage: engine.Stage) -> int:
    battle_armies = [army.num for army in stage.armies]
    return sum(battle_armies)


def AB_approzimation(A, B, stage: engine.Stage) -> int:
    battle_armies = [army.num for army in stage.armies]
    pos_sum = 0
    neg_sum = 0
    for _ in battle_armies:
        if _ > 0:
            pos_sum = pos_sum + _
        else:
            neg_sum = neg_sum - _
    return A*pos_sum - B*neg_sum


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

def generate_two_Nstage(N, MAX_NUM_ARMY = 150):
    armies_generated = []

    indeces = [i for i in range(N)]
    pos_number = choice(indeces[1:])
    pos_indeces = sample(indeces, pos_number)
    
    for i in range(N): #0,__,N-1
        if i in pos_indeces:
            num_army = randint(1, 120)
            troop_army = choice(BLUE_TROOPS)
        else:
            num_army = -randint(1, 120)
            troop_army = choice(RED_TROOPS)
        armies_generated.append(engine.Army(num_army, troop_army))
    
    Normal_Stage = engine.Stage(armies_generated)
    j = choice(pos_indeces)
    new_army = armies_generated[j].copy()
    new_army.add_troop(1)
    armies_generated[j] = new_army
    Added_Stage = engine.Stage(armies_generated)
    return Normal_Stage, Added_Stage

"""
N = 6
difference_list = []
rapport_list = []
for _ in range(2000):
    first_stage, second_stage = generate_two_Nstage(N)

    first_result = engine.best_result_from_stage(first_stage)[1].num
    second_result = engine.best_result_from_stage(second_stage)[1].num

    print(_)
    if first_result != 0:
        difference_list.append(second_result - first_result)
        rapport_list.append(second_result/first_result)

print(f"Diff: {mean(difference_list)} | Rapp: {mean(rapport_list)}")
 """
 
N = 4
for _ in range(2000):
    Nstage = generate_Nstage(N)
    app_result = AB_approzimation(1.08,1,Nstage)
    real_result = engine.best_result_from_stage(Nstage)[1].num
    print(app_result - real_result)


  
  
  
    
"""
Nstage = generate_Nstage(6)
#aggiungi 1 alla prima truppa positiva
Nstage_plus = Nstage.copy()
for army in Nstage_plus.armies:
    if 




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
"""
    
    
    