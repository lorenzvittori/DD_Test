import numpy as np
import battle_engine as engine

#BLU
BLUE_ARCHI = "2 2"
BLUE_SPADE = "10"
BLUE_ASCE = "10"
#BONUS
ADD_BONUS = "20"

#ROSSO
RED_ARCHI = "10"
RED_SPADE = "10"
RED_ASCE = "1"
#BOSS
BOSS = ""



def parse_input(text):
    if not text:
        return np.array([])
    try:
        return np.array([int(i) for i in text.strip().split() if i.strip().isdigit()])
    except ValueError:
        return np.array([])

BlueArchers_list = parse_input(BLUE_ARCHI)
BlueSwordsmen_list = parse_input(BLUE_SPADE)
BlueAxemen_list = parse_input(BLUE_ASCE)

AddBonus = parse_input(ADD_BONUS)


if len(AddBonus) == 1:
    AddBonusValue = AddBonus[0]
else:
    AddBonusValue = 0
    
RedArchers_list = -parse_input(RED_ARCHI)
RedSwordsmen_list = -parse_input(RED_SPADE)
RedAxemen_list = -parse_input(RED_ASCE)

Boss_list = -parse_input(BOSS)

BlueArchers_list = BlueArchers_list[BlueArchers_list != 0]
BlueSwordsmen_list = BlueSwordsmen_list[BlueSwordsmen_list != 0]
BlueAxemen_list = BlueAxemen_list[BlueAxemen_list != 0]

RedArchers_list = RedArchers_list[RedArchers_list != 0]
RedSwordsmen_list = RedSwordsmen_list[RedSwordsmen_list != 0]
RedAxemen_list = RedAxemen_list[RedAxemen_list != 0]

Boss_list = Boss_list[Boss_list != 0]

Situation_Dict = {
    'archi': np.concatenate((BlueArchers_list, RedArchers_list)),
    'spade': np.concatenate((BlueSwordsmen_list, RedSwordsmen_list)),
    'asce': np.concatenate((BlueAxemen_list, RedAxemen_list)),
    'boss': Boss_list
}

OptSequence, OptResult = engine.best_result_from_dict(Situation_Dict, AddBonusValue)
print("Sequenza Ottimale:", OptSequence)
print("Risultato Finale:", OptResult)