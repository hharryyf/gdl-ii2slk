#from clyngor import ASP, solve
import sys
import clingo 
'''
    Input is a GDL-II file written in lp format, no "or" is allowed in the GDL-II file.
    The GDL-II must be grounded, and acyclic
    for speed up, you cannot put goal in the body of any rule.
'''
init = set()
initf = set()
legal = {}
role = set()
base = set()
next = set()
see = {}
goal = {}
other = set()
dependency = {}    
graph = {}
vertices = set()
visited = {}
dp = {}


def build(head, body):
    def slk_var(atominfo: dict):
        if atominfo['type'] == 'legal':
            return 'legal_' + atominfo['player'] + '_' + atominfo['slk']
        #elif atominfo['type'] == 'goal':
        #    return 'goal_' + atominfo['player'] + '_' + atominfo['slk']
        elif atominfo['type'] == 'init':
            return 'true_' + atominfo['slk']
        elif atominfo['type'] == 'true':
            return 'true_' + atominfo['slk']
        elif atominfo['type'] == 'next':
            return 'next_' + atominfo['slk']
        elif atominfo['type'] == 'sees':
            return 'sees_' + atominfo['player'] + '_' + atominfo['slk']
        elif atominfo['type'] == 'does':
            return 'does_' + atominfo['player'] + '_' + atominfo['slk']
        elif atominfo['type'] == 'terminal':
            return 'terminal'
        elif atominfo['type'] == 'role':
            return 'role_' + atominfo['slk']
        else:
            return atominfo['slk']
    
    def create_var(atominfo: dict):
        if atominfo['type'] == 'legal':
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
            if atominfo['player'] not in legal:
                legal[atominfo['player']] = set()
            legal[atominfo['player']].add(atominfo['slk'])
        elif atominfo['type'] == 'init':
            base.add(atominfo['slk'])
            init.add(atominfo['slk'])
        elif atominfo['type'] == 'true':
            base.add(atominfo['slk'])
        elif atominfo['type'] == 'next':
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
            base.add(atominfo['slk'])
            next.add(atominfo['slk'])
        elif atominfo['type'] == 'sees':
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
            if atominfo['player'] not in see:
                see[atominfo['player']] = set()
            see[atominfo['player']].add(atominfo['slk'])
        elif atominfo['type'] == 'does':
            # return 'does_' + atominfo['player'] + '_' + atominfo['slk']
            pass
        elif atominfo['type'] == 'terminal':
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
        elif atominfo['type'] == 'role':
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
            role.add(atominfo['slk'])
        else:
            if slk_var(atominfo) not in dependency:
                dependency[slk_var(atominfo)] = []
            other.add(slk_var(atominfo))

    create_var(head)
    vertices.add(slk_var(head))
    dp[slk_var(head)] = -1
    if slk_var(head) not in graph:
        graph[slk_var(head)] = []
    for bd in body:
        create_var(bd)
        vertices.add(slk_var(bd))
        dp[slk_var(bd)] = -1
        if slk_var(bd) not in graph:
            graph[slk_var(bd)] = []
        graph[slk_var(head)].append(slk_var(bd))

    if len(body) == 0 and head['type'] != 'init':
        if slk_var(head)[:5] == 'goal_':
            dependency[slk_var(head)].append('(Environment.ok = 0)')
        else:
            dependency[slk_var(head)].append('(ok = 0)')
    elif len(body) != 0:
        conjunct = []
        for bd in body:
            if slk_var(bd)[:5] == 'goal':
                print('goal cannot appear in the body!')
                exit(1)
            if bd['positive'] == True:
                if slk_var(head)[:5] == 'goal_':
                    conjunct.append(f'(Environment.{slk_var(bd)} = true)')
                else:
                    conjunct.append(f'({slk_var(bd)} = true)')
            else:
                if slk_var(head)[:5] == 'goal_':
                    conjunct.append(f'(Environment.{slk_var(bd)} = false)')
                else:
                    conjunct.append(f'({slk_var(bd)} = false)')
        conj = conjunct[0]
        for i in range(1, len(conjunct)):
            conj = conj + ' and ' + conjunct[i]
        dependency[slk_var(head)].append(f'({conj})')



def debug():
    print('--- dependency ---')    
    for rule in dependency.keys():
        print(f'{rule} <=> {dependency[rule]}')
    print('--- init ---')
    print(init)
    print('--- legal ---')
    print(legal)
    print('--- role ---')
    print(role)
    print('--- base ---')
    print(base)
    print('--- see ---')
    print(see)
    #print('--- goal ---')
    #print(goal)
    print('--- done ---')
    print(legal)
    print('---other ---')
    print(other)

def clean(fluent: str):
        return fluent.replace(',', '_').replace(' ','').replace('(', '_').replace(')', '')


        
def parse_content(atom: str, num: int):
    
    if num == 1:
        if atom[:5] == 'init(':
            initf.add('true(' + atom[5:] + '.')
        pos = 0
        for ch in atom:
            pos += 1
            if ch == '(':
                break
        return clean(atom[pos:-1])
    elif num == 2:
        pos = 0
        for ch in atom:
            pos += 1
            if ch == '(':
                break
        atom = atom[pos:len(atom)]
        pos, tol = 0, 0
        for ch in atom:
            pos += 1
            if ch == '(':
                tol += 1
            elif ch == ')':
                tol -= 1
            if ch == ',' and tol == 0:
                break
        return clean(atom[:pos-1]), clean(atom[pos:-1])

    return clean(atom)            

'''
    returns a tuple (type of the atom, player, name of the atom in SLK, positive negative)
'''
def parse_atom(atom: str):
    atom = atom.strip()
    atom_type = 'other'
    player = ''
    slk = ''
    positive = True
    if len(atom) > 4 and atom[:4] == 'not ':
        atom = atom[4:].strip()
        positive = False

    if '(' not in atom:
        if atom == 'terminal':
            atom_type = 'terminal'
            slk = 'terminal'
        else:
            slk = parse_content(atom, 0)
    else:
        curr = ''
        for ch in atom:
            if ch == '(':
                break 
            curr += ch
        if curr == 'goal':
            nx = atom[4:].replace('(', '').replace(')','').split(',')
            if nx[0] not in goal:
                goal[nx[0].strip()] = set()
            goal[nx[0].strip()].add(int(nx[1].strip()))
        if curr == 'does' or curr == 'legal' or curr == 'sees': # curr == 'goal' or 
            atom_type = curr
            content = parse_content(atom, 2)
            player = content[0]
            slk = content[1]
        elif curr == 'next' or curr == 'init' or curr == 'role' or curr == 'true':
            atom_type = curr
            content = parse_content(atom, 1)
            slk = content
        else:
            slk = parse_content(atom, 0)

    return {'type': atom_type, 'player': player, 'slk': slk, 'positive': positive}

def parse_rule(rule: str):
    rule = rule.replace('.', '')

    head = ''
    body = []
    if ':-' in rule:
        rule = rule.split(':-')
        rule[0] = rule[0].strip()
        rule[1] = rule[1].strip()
        head = parse_atom(rule[0])
        curr = ''
        tol = 0
        for ch in rule[1]:
            if ch == ',' and tol == 0:
                body.append(parse_atom(curr))
                curr = ''
            else:
                curr += ch
                if ch == '(':
                    tol += 1
                elif ch == ')':
                    tol -= 1

        if curr != '':
            body.append(parse_atom(curr))

    else:
        head = parse_atom(rule)            

    return head, body

# all the variables for the environment
def print_environment_vars(maxd:int =3, recall:int = 1):
    print('    Vars:')
    print(f'        ok: 0.. 0;')
    # print the roles
    #for r in role:
    #    print(f'        role_{r}: boolean;')
    print(f'        counter: 0 .. {maxd};')
    # print(f'        init: 0 .. {maxd};')
    print(f'        act_step: boolean;')
    
    for r in sorted(legal.keys()):
        for act in sorted(legal[r]):
            print(f'        does_{r}_{act}: boolean;')

    for atom in sorted(base):
        print(f'        true_{atom}: boolean;')

    # print the sees and observations
    for r in sorted(see.keys()):
        for observations in sorted(see[r]):
            for i in range(recall+1):
                if i == 0:
                    print(f'        sees_{r}_{observations}: boolean;')    
                print(f'        seen_{r}_{observations}_{i+1}: boolean;')

    for r in sorted(legal.keys()):
        for atom in sorted(legal[r]):
            print(f'        legal_{r}_{atom}: boolean;')
    
    # print the base propositions
    for atom in sorted(base):
        print(f'        next_{atom}: boolean;')
    

    # print the sees and observations
    #for r in sorted(see.keys()):
    #    for observations in sorted(see[r]):
    #        for i in range(recall+1):
                # print(f'        sees_{r}_{observations}_{i+1}_obs: boolean;')
    #            print(f'        next_sees_{r}_{observations}_{i+1}: boolean;')
    
    print(f'        terminal: boolean;')
    for r in sorted(legal.keys()):
        for act in sorted(legal[r]):
            for i in range(recall):
                print(f'        done_{r}_{act}_{i+1}: boolean;')
                
    for atom in sorted(other):
        if atom[:5] != 'goal_':
            print(f'        {atom}: boolean;')
    print('    end Vars')

def print_evolutions(maxd:int = 3, recall:int = 1):
    print('    Evolution:')
    print(f'        -- print the counters')
    print('        ok = 0 if (ok = 0);')
    print(f'        (counter = counter + 1) if !((terminal = true and counter = 0) or counter = {maxd} or (counter = {maxd-2} and act_step = false));')
    print(f'        (counter = 0) if ((terminal = true and counter = 0) or counter = {maxd} or (counter = {maxd-2} and act_step = false));')
    print(f'        act_step = false if ((counter < {maxd-2} and act_step = false) or (counter = {maxd} and act_step = true));')
    print(f'        act_step = true if !((counter < {maxd-2} and act_step = false) or (counter = {maxd} and act_step = true));')    
    print()
    print(f'        -- print the dependencies')
    for d in sorted(dependency.keys()):
        if d[:5] == 'goal_' or d[:5] == 'role_':
            continue
        rule = dependency[d]
        if len(rule) == 0:
            print(f'        {d}=false if (ok = 0);')
        else:
            cond = '(' + rule[0]
            for i in range (1, len(rule)):
                cond = cond + ' or ' + rule[i]
            cond = cond + ')'
            print(f'        {d}=true if {cond};')
            print(f'        {d}=false if !{cond};')
    print()

    print(f'        -- print the next for actions')
    
    print(f'        -- local observation evolution')
    for r in sorted(legal.keys()):
        lgr = sorted(legal[r])
        illegal = ''
        for i in range(len(lgr)):
            act = lgr[i]
            if i == 0:
                illegal += f'(player_{r}.Action={act} and legal_{r}_{act}=false)'
            else:
                illegal += f' or (player_{r}.Action={act} and legal_{r}_{act}=false)'
        
        for i in range(len(lgr)):
            act = lgr[i]
            prevbad = ''
            for j in range(i):
                if j == 0:
                    prevbad += f'legal_{r}_{lgr[j]}=false'
                else:
                    prevbad += f' and legal_{r}_{lgr[j]}=false'

            false_str = f'(counter = {maxd} and act_step = true)'
            if i != 0:
                true_str = f'(counter = 0 and act_step = true and terminal = false and legal_{r}_{act} = true and (player_{r}.Action={act} or (({illegal}) and ({prevbad}))))'
            else:
                true_str = f'(counter = 0 and act_step = true and terminal = false and legal_{r}_{act} = true and (player_{r}.Action={act} or ({illegal})))'
                
            print(f'        does_{r}_{act} = true if {true_str};')
            print(f'        does_{r}_{act} = false if {false_str};')
            print(f'        does_{r}_{act} = does_{r}_{act}  if !({false_str} or {true_str});')
    
    # print the evolutions for true
    for b in sorted(base):
            print(f'        true_{b} = next_{b} if ((act_step = true and counter = {maxd}));')
            print(f'        true_{b} = true_{b} if !((act_step = true and counter = {maxd}));')


    # print the evolutions for recall
    for r in sorted(legal.keys()):
        for act in sorted(legal[r]):
            for i in range(recall):
                if i == 0:
                    print(f'        done_{r}_{act}_{i+1} = does_{r}_{act} if ((act_step = true and counter = {maxd}));')
                else:
                    print(f'        done_{r}_{act}_{i+1} = done_{r}_{act}_{i} if ((act_step = true and counter = {maxd}));')
                    
                print(f'        done_{r}_{act}_{i+1} = done_{r}_{act}_{i+1} if !((act_step = true and counter = {maxd}));')
    
    
    for r in sorted(see.keys()):
        for observations in sorted(see[r]):
            for i in range(recall+1):
                if i == 0:
                    print(f'        seen_{r}_{observations}_{i+1} = sees_{r}_{observations} if ((act_step = true and counter = {maxd}));')
                    print(f'        seen_{r}_{observations}_{i+1} = seen_{r}_{observations}_{i+1} if !((act_step = true and counter = {maxd}));')
                else:
                    print(f'        seen_{r}_{observations}_{i+1} = seen_{r}_{observations}_{i} if ((act_step = true and counter = {maxd}));')
                    print(f'        seen_{r}_{observations}_{i+1} = seen_{r}_{observations}_{i+1} if !((act_step = true and counter = {maxd}));')
    

    print('    end Evolution')


def print_init(maxd:int = 3, recall:int = 1):
    init_fluent = ''
    for s in initf:
        init_fluent += s + ' '

    with open(sys.argv[1], "r") as g:
        ASP_program = g.read()
    ASP_program += init_fluent
    
    ctl = clingo.Control(arguments=['-W', 'none'])  # Here you can write the arguments you would pass to clingo by command line.
    ctl.add("base", [], ASP_program)  # Adds the program to the control object.
    ctl.ground([("base", [])])  # Grounding...
    init_true = set()
    # Solving...
    with ctl.solve(yield_=True) as solution_iterator:
        for model in solution_iterator:
            # Model is an instance of clingo.solving.Model class 
            # Reference: https://potassco.org/clingo/python-api/current/clingo/solving.html#clingo.solving.Model
            for s in str(model).split():
                init_true.add(clean(s))

    print('InitStates')
    print(f'    Environment.counter = 0 and Environment.ok = 0 and Environment.act_step = true')
    for atom in sorted(base):
        if atom in init:
            print(f'    and Environment.true_{atom} = true')
        else:
            print(f'    and Environment.true_{atom} = false')
        if f'next_{atom}' in init_true:
            print(f'    and Environment.next_{atom} = true')
        else:
            print(f'    and Environment.next_{atom} = false')
            
    # print the sees and observations
    for r in sorted(see.keys()):
        for observations in sorted(see[r]):
            for i in range(recall+1):
                if i == 0:
                    if f'sees_{r}_{observations}' in init_true:
                        print(f'    and Environment.sees_{r}_{observations} = true')
                    else:
                        print(f'    and Environment.sees_{r}_{observations} = false')
                print(f'    and Environment.seen_{r}_{observations}_{i+1} = false')
                
    for r in sorted(legal.keys()):
        for atom in sorted(legal[r]):
            if f'legal_{r}_{atom}' in init_true:
                print(f'    and Environment.legal_{r}_{atom} = true')
            else:
                print(f'    and Environment.legal_{r}_{atom} = false')
    
    if 'terminal' in init_true:
        print(f'    and Environment.terminal = true')
    else:
        print(f'    and Environment.terminal = false')    

    for r in sorted(legal.keys()):
        for act in sorted(legal[r]):
            print(f'    and Environment.does_{r}_{act} = false')
            for i in range(recall):
                print(f'    and Environment.done_{r}_{act}_{i+1} = false')
    
    for atom in sorted(other):
        if atom[:5] != 'goal_':
            if atom in init_true:
                print(f'    and Environment.{atom} = true', end = '')
            else:
                print(f'    and Environment.{atom} = false', end = '')
    print(';')
    print('end InitStates')
    
def print_agent(agent, recall=1):
    print(f'Agent player_{agent}')
    print('    Lobsvars={counter,act_step', end='')
    if agent in sorted(see):
        for observations in sorted(see[agent]):
            for i in range(recall+1):
                print(f', seen_{agent}_{observations}_{i+1}', end='')
    
    #for atom in sorted(legal[agent]):
    #    print(f', legal_{agent}_{atom}', end='')
    for act in sorted(legal[agent]):
        for i in range(recall):
            print(f', done_{agent}_{act}_{i+1}', end='')
    print('};')
    print('    Vars:')
    print()
    print('    end Vars')
    print('    Actions = {', end = '')
    for act in sorted(legal[agent]):
        print(f'{act}, ', end='')
    print('none};')
    print('    Protocol:')
    for act in sorted(legal[agent]):
        print(f'        (Environment.counter = 0 and Environment.act_step = true): ' + '{' + f'{act}' + '};')
    print('        Other : {none};')
    print('    end Protocol')
    print('    Evolution:\n\n    end Evolution')
    print('end Agent')

def longest_chain():
    def dfs(v):
        if dp[v] != -1:
            return dp[v]
        dp[v] = 1
        for nv in graph[v]:
            dp[v] = max(dp[v], dfs(nv) + 1)
        return dp[v]
    for v in vertices:
        if dp[v] == -1:
            dfs(v)
    ans = 1
    for v in vertices:
        ans = max(ans, dp[v])
    print('-- maximum chain length', ans)
    return ans

def writeslk(recall:int = 1):
    # write the SLK file
    # The Environment Agent
    print('Semantics=SingleAssignment;')
    print()
    print('Agent Environment')
    maxd = longest_chain()
    print_environment_vars(maxd, recall)
    print('    Actions = { none };')
    print('    Protocol:')
    print('        Other: {none};')
    print('    end Protocol')
    print_evolutions(maxd, recall)
    print('end Agent')

    # Other Agents
    for r in sorted(role):
        print()
        print_agent(r, recall)
        print()
    # Evaluation
    
    print('Evaluation')
    for d in sorted(dependency.keys()):
        if d[:5] != 'goal_':
            continue
        rule = dependency[d]
        cond = '(' + rule[0]
        for i in range (1, len(rule)):
            cond = cond + ' or ' + rule[i]
        cond = cond + ')'
        print(f'    {d} if {cond};')
    print('t if (Environment.terminal = true and Environment.act_step = true and Environment.counter = 0);')
    print('end Evaluation')
    # initial states
    print()
    print_init(maxd, recall)
    print()
    # other information
    print('Groups\nend Groups')
    print()
    print('Fairness\nend Fairness')
    print()
    print('Formulae')
    print('    AF t;')
    # exist NE
    # print('<<env>> ', end='')
    # for r in role:
    #     print(f'<<{r}>> ', end='')
    # print('(Environment, env)', end = ' ')
    # for r in role:
    #     print(f'(player_{r}, {r}) ', end='')
    # i = 1
    # print('(', end='')
    # for r in role:
    #     print('(', end='')
    #     scores = sorted(goal[r])
    #     for j in range(len(scores)):
    #         print(f'(F (goal_{r}_{scores[j]} and t) and ([[{r}{j}]] (player_{r}, {r}{j}) F (t and (goal_{r}_{scores[0]} ', end='')
    #         for k in range(1, j+1):
    #             print(f'or goal_{r}_{scores[k]}', end=' ')
    #         if j != len(scores) - 1:
    #             print(')))) or ', end='')
    #         else:
    #             print(')))) ', end='')

    #     print(') ', end='')
    #     if i != len(role):
    #         print(' and ', end='')
    #     i += 1
    # print(');')
    print('end Formulae')

def construct_dependencies(file):    
    f = open(file=file, mode='r')
    curr = ''
    for line in f:
        line = line.strip()
        if len(line) == 0 or line[0] == '-' or line == None:
            continue
        curr += line
        if curr[-1] == '.':
            head, body = parse_rule(curr)
            build(head, body)
        curr = ''
    f.close()
    for b in base:
        if b not in next:
            dependency[f'next_{b}'] = []

def gdl2slk(file, recall:int = 1):
    construct_dependencies(file)
    writeslk(recall)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage python translate.py [name of the GDL-II file] [recall depth]')
        sys.exit(1)
    gdl2slk(sys.argv[1], int(sys.argv[2]))
    