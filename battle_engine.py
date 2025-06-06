import copy


ADVANTAGE_RULE = {
    'archi': 'asce',
    'asce': 'spade',
    'spade': 'archi'
}

class Army:
    def __init__(self, num: int, troop: str):
        self.num = int(num)
        self.troop = troop

    def __eq__(self, other):
        return self.num == other.num and self.troop == other.troop

    def __lt__(self, other):
        if self.num != other.num:
            return self.num < other.num
        return self.troop < other.troop
    
    def add_troop(self, n):
        self.num = self.num + n

    def __str__(self):
        return f"{self.num}({self.troop})"
    
    def copy(self):
        copied_num = copy.deepcopy(self.num)
        copied_troop = copy.deepcopy(self.troop)
        return Army(copied_num, copied_troop)

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

def permutazioni_uniche(arr):
    arr.sort()
    risultato = []
    usati = [False] * len(arr)

    def backtrack(permutazione_corrente):
        if len(permutazione_corrente) == len(arr):
            risultato.append(permutazione_corrente[:])
            return

        for i in range(len(arr)):
            if usati[i]:
                continue
            if i > 0 and arr[i] == arr[i - 1] and not usati[i - 1]:
                continue

            usati[i] = True
            permutazione_corrente.append(arr[i])
            backtrack(permutazione_corrente)
            permutazione_corrente.pop()
            usati[i] = False

    backtrack([])
    return risultato

def are_allies(Ax: Army, Ay: Army) -> bool:
    return Ax.num * Ay.num > 0

def allies_sum(Ax, Ay, bonus = 0):
    nx, ny = Ax.num, Ay.num
    tx, ty = Ax.troop, Ay.troop
    combined_num = nx + ny + bonus*(tx == ty)
    return Army(combined_num, tx if abs(nx) >= abs(ny) else ty)


single_combat_cache = {}

def single_connection(Ax: Army, Ay: Army, bonus = 0) -> Army:
    key = ((Ax.num, Ax.troop), (Ay.num, Ay.troop), bonus)

    if key in single_combat_cache:
        return single_combat_cache[key]

    nx, ny = Ax.num, Ay.num
    tx, ty = Ax.troop, Ay.troop

    if are_allies(Ax, Ay):
        result = allies_sum(Ax, Ay, bonus)
    
    else:
        vantaggio = advantage_order(Ax, Ay)
        if vantaggio:
            newX, newY = vantaggio
            nx, ny = newX.num, newY.num
            tx, ty = newX.troop, newY.troop
            if abs(nx * 1.5) >= abs(ny):
                end_num = int(nx + 2 * ny / 3)
                end_troop = tx
            else:
                end_num = int(3 * nx / 2 + ny)
                end_troop = ty
        else:
            end_num = nx + ny
            end_troop = tx if abs(nx) >= abs(ny) else ty
        result = Army(end_num, end_troop)

    single_combat_cache[key] = result
    return result


def Battle(stage: Stage, bonus = 0) -> Army:
    armies = stage.armies
    result = armies[0]
    for enemy in armies[1:]:
        result = single_connection(result, enemy, bonus)
    return result



def BattleResult(stage, bonus = 0) -> int:
    return Battle(stage, bonus).num



def somma_lineare(stage: Stage) -> int:
    battle_armies = [army.num for army in stage.armies]
    return sum(battle_armies)


def BestResultGenerator(Situation: dict, bonus = 0):
    stage = situation_to_stage(Situation)
    all_permutations = permutazioni_uniche(stage.armies)
    
    best_stage = None
    best_army = None
    best_score = float('-inf')

    for permutation in all_permutations:
        staged = Stage(permutation)
        outcome = Battle(staged, bonus)
        if outcome.num > best_score:
            best_score = outcome.num
            best_stage = staged
            best_army = outcome
            yield best_stage, best_army



def best_result_from_dict(Situation: dict, bonus = 0):
    stage = situation_to_stage(Situation)
    all_permutations = permutazioni_uniche(stage.armies)
    
    best_stage = None
    best_army = None
    best_score = float('-inf')

    for permutation in all_permutations:
        staged = Stage(permutation)
        outcome = Battle(staged, bonus)
        if outcome.num > best_score:
            best_score = outcome.num
            best_stage = staged
            best_army = outcome
    return best_stage, best_army


        
def best_result_from_stage(stage: Stage, bonus = 0):
    all_permutations = permutazioni_uniche(stage.armies)
    
    best_stage = None
    best_army = None
    best_score = float('-inf')

    for permutation in all_permutations:
        staged = Stage(permutation)
        outcome = Battle(staged, bonus)
        if outcome.num > best_score:
            best_score = outcome.num
            best_stage = staged
            best_army = outcome
    return best_stage, best_army


def best_result_from_stage_with_cut(stage: Stage, bonus = 0):
    all_permutations = permutazioni_uniche(stage.armies)
    
    best_stage = None
    best_army = None
    best_score = float('-inf')

    for permutation in all_permutations:
        staged = Stage(permutation)
        outcome = Battle(staged, bonus)
        if outcome.num > best_score:
            best_score = outcome.num
            best_stage = staged
            best_army = outcome
    return best_stage, best_army