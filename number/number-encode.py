import sys

num = int(sys.argv[1])

print('role(x).')
print('role(o).')
print('init(round(0)).')
print('init(control(o)).')

for i in range(1, num + 1):
    print(f'legal(o,choose({i})) :- true(control(o)).')


for i in range(1, num + 1):
    print(f'legal(x,guess({i})) :- true(control(x)).')

print('legal(o, noop) :- true(control(x)).')
print('legal(x, noop) :- true(control(o)).')

for i in range(1, num + 1):
    print(f'next(choose({i})) :- true(choose({i})).')

for i in range(1, num + 1):
    print(f'next(choose({i})) :- does(o,choose({i})).')

print('next(control(x)) :- true(control(o)).')
print('next(control(x)) :- true(control(x)).')

for i in range(1, num + 2):
    print(f'next(round({i})) :- true(round({i-1})).')

print(f'terminal :- true(round({num+1})).')

for i in range(1, num + 1):
    print(f'next(correct) :- true(choose({i})), does(x, guess({i})).')
    print(f'sees(x, ok) :- true(choose({i})), does(x, guess({i})).')

for i in range(1, num + 1):
    for j in range(1, num + 1):
        if i < j:
            print(f'sees(x, less({j})) :- true(choose({i})), does(x, guess({j})).')
    for j in range(num, 0, -1):
        if i > j:
            print(f'sees(x, great({j})) :- true(choose({i})), does(x, guess({j})).')


print(f'terminal :- true(correct).')

for i in range(2, num + 1):
    if i == 1:
        print(f'goal(x,100) :- true(correct), true(round({i})).')
    else:
        print(f'goal(x,{int(100/(num-1) * (num - i+1))}) :- true(correct), true(round({i})).')

print(f'goal(x, 0) :- true(round({num+1})).')
print('goal(x, 0) :- not true(correct).')
print('goal(o, 0).')
