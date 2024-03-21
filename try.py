role = ['x', 'o']

for r in range(0, 2):
    for i in range(1, 4):
        for j in range(1, 4):
            print(f'sees({role[r]},success) :- does({role[r]}, mark({i},{j})), true(cell({i}, {j}, b)).')
            print(f'next(cell({i},{j},{role[r]})) :- does({role[r]}, mark({i},{j})), true(cell({i}, {j}, b)).')
            print(f'next(control({role[1-r]})) :- does({role[r]}, mark({i},{j})), true(cell({i}, {j}, b)).')
            print(f'sees({role[r]},fail) :- does({role[r]}, mark({i},{j})), true(cell({i}, {j}, {role[1-r]})).')
            print(f'next(control({role[r]})) :- does({role[r]}, mark({i},{j})), true(cell({i}, {j}, {role[1-r]})).')
