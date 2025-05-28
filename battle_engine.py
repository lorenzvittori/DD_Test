import itertools
import copy

ADVANTAGE_RULE = {
    'archi': 'asce',
    'asce': 'spade',
    'spade': 'archi'
}

# Classe base per un'armata
class Army:
    def __init__(self, num: int, troop: str):
        self.num = num
        self.troop = troop
        
    def __eq__(self, other):
        return self.num == other.num and self.troop == other.troop

    def __str__(self):
        return f"{self.num}({self.troop})"

# Una sequenza di armate
class Stage:
    def __init__(self, armies):
        self.armies = list(armies)

    def add_army(self, army: Army):
        self.armies.append(army)

    def reverse(self):
        self.armies.reverse()

    def copy(self):
        return Stage(copy.deepcopy(self.armies))

    def __str__(self):
        return ' -> '.join(str(army) for army in self.armies)

# Converte un dizionario in un oggetto Stage
def situation_to_stage(situation_dict: dict) -> Stage:
    armies = [Army(num, troop) for troop in situation_dict for num in situation_dict[troop]]
    return Stage(armies)

def advantage_order(Ax: Army, Ay: Army) -> tuple | bool:
    tx = Ax.troop.strip().lower()
    ty = Ay.troop.strip().lower()
    if tx == 'neutral' or ty == 'neutral': 
        return False
    if tx == ty: 
        return False   
    if ADVANTAGE_RULE.get(tx) == ty:
        return (Ax, Ay)
    elif ADVANTAGE_RULE.get(ty) == tx:
        return (Ay, Ax)
    else:
        return False


# Controlla se due armate sono alleate
def are_allies(Ax: Army, Ay: Army) -> bool:
    return Ax.num * Ay.num > 0

# Combattimento tra due armate
def single_combat(Ax: Army, Ay: Army) -> Army:
    nx, ny = Ax.num, Ay.num
    tx, ty = Ax.troop, Ay.troop

    if are_allies(Ax, Ay):
        combined_num = nx + ny
        if abs(nx) >= abs(ny):
            return Army(combined_num, tx)
        else:
            return Army(combined_num, ty)
    else: #sono nemici
        vantaggio = advantage_order(Ax, Ay)
        if vantaggio:
            newX, newY = vantaggio
            nx, ny = newX.num, newY.num
            tx, ty = newX.troop, newY.troop
            if abs(nx * 1.5 ) >= abs(ny):   #vince X
                end_num = int(nx + 2 * ny / 3)
                end_troop = tx
            else: #vince Y
                end_num = int(3 * nx / 2 + ny)
                end_troop = ty
        else:
            end_num = nx + ny
            end_troop = tx if abs(nx) >= abs(ny) else ty
        return Army(end_num, end_troop)

# Esegue una battaglia sequenziale
def Battle(stage: Stage) -> Army:
    armies = stage.armies
    result = armies[0]
    for enemy in armies[1:]:
        result = single_combat(result, enemy)
    return result

def BattleResult(stage) -> int:
    return Battle(stage).num


def BestResult(Situation: dict):
    # Prepara le permutazioni di battaglia
    stage = situation_to_stage(Situation)
    all_permutations = set(itertools.permutations(stage.armies))

    # Esegui tutte le battaglie e salva i risultati
    battle_results = []
    for permutation in all_permutations:
        staged = Stage(permutation)
        outcome = Battle(staged)
        battle_results.append((staged, outcome))

    best_result = battle_results[0]
    best_outcome_num = best_result[1].num
    
    for stage, outcome in battle_results:
        if outcome.num > best_outcome_num:
            best_result = (stage, outcome)
            best_outcome_num = outcome.num
            
    return best_result
