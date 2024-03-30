import sys

n = int(sys.argv[1])
m = int(sys.argv[2])
r = int(sys.argv[3])

combine = []

print('role(x).')
print('role(o).')
print()
print('init(control(o)).')
print('init(round(0)).')
print()
print('legal(o,noop) :- true(control(x)).')
print('legal(x,noop) :- true(control(o)).')
print()
print('next(control(x)) :- true(control(x)).')
print('next(control(x)) :- true(control(o)).')

print('next(round(0)) :- true(round(0)), true(control(o)).')
print('next(round(1)) :- true(round(0)), true(control(x)).')

for i in range(2, r + 1):
    print(f'next(round({i})) :- true(round({i-1})).')

print()

def generate_combination(place, curr:list):
    if place == 0:
        combine.append(curr.copy())
        return 

    for i in range(1, n + 1):
        curr.append(i)
        generate_combination(place - 1, curr)
        curr.pop()    

tmp = []
generate_combination(m, tmp)


for curr in combine:
    print(f'legal(o, select({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')) :- true(control(o)).')
    print(f'next(picked({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')) :- ', end='')
    print(f'does(o, select({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')).')
    print(f'next(picked({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')) :- ', end='')
    print(f'true(picked({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')).')
    print(f'legal(x, guess({curr[0]}', end='')
    for i in range(1, len(curr), 1):
        print(f',{curr[i]}',end='')
    print(')) :- true(control(x)).')
print()
for xguess in combine:
    for yguess in combine:
        if xguess == yguess:
            print(f'sees(x, match({m},{0})) :- ', end='')
            print(f'true(picked({xguess[0]}', end='')
            for i in range(1, len(xguess), 1):
                print(f',{xguess[i]}',end='')
            print(')), ', end='')
            print(f'does(x, guess({xguess[0]}', end='')
            for i in range(1, len(xguess), 1):
                print(f',{xguess[i]}',end='')
            print(')).')
            print(f'next(correct) :- ', end='')
            print(f'true(picked({xguess[0]}', end='')
            for i in range(1, len(xguess), 1):
                print(f',{xguess[i]}',end='')
            print(')), ', end='')
            print(f'does(x, guess({xguess[0]}', end='')
            for i in range(1, len(xguess), 1):
                print(f',{xguess[i]}',end='')
            print(')).')
        else:
            x = {}
            y = {}
            match = 0
            color = 0
            for i in range(len(xguess)):
                if xguess[i] == yguess[i]:
                    match += 1
                else:
                    if xguess[i] not in x:
                        x[xguess[i]] = 1
                    else:
                        x[xguess[i]] += 1
                    if yguess[i] not in y:
                        y[yguess[i]] = 1
                    else:
                        y[yguess[i]] += 1
            
            #print(x, y)
            for xx in x.keys():
                color += min(x[xx], y.get(xx, 0))
            
            print(f'sees(x, match({match},{color})) :- ', end='')
            print(f'true(picked({yguess[0]}', end='')
            for i in range(1, len(yguess), 1):
                print(f',{yguess[i]}',end='')
            print(')), ', end='')
            print(f'does(x, guess({xguess[0]}', end='')
            for i in range(1, len(xguess), 1):
                print(f',{xguess[i]}',end='')
            print(')).')

print()
print('terminal :- true(correct).')
print(f'terminal :- true(round({r})).')
print('goal(x,0) :- not true(correct).')
for i in range(1, r+1):
    print(f'goal(x,{int(100 * (r-i+1) / (r))}) :- true(correct), true(round({i})).')
print('goal(o,0).')
