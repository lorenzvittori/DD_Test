from random import choice, randint, choices, sample



N = 5

indeces = [i for i in range(N)]
pos_number = choice(indeces[1:])
pos_indeces = sample(indeces, pos_number)

print(indeces, pos_number, pos_indeces)