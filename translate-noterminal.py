import sys

'''
    Input is a GDL-II file written in lp format, no "or" is allowed in the GDL-II file.
    The GDL-II must be grounded, and acyclic
'''

init = set()
legal = {}
role = set()
base = set()
next = set()
see = {}
#goal = {}
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
            return 'next_sees_' + atominfo['player'] + '_' + atominfo['slk'] + '_1'
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
        #elif atominfo['type'] == 'goal':
        #    if slk_var(atominfo) not in dependency:
        #        dependency[slk_var(atominfo)] = []
        #    if atominfo['player'] not in goal:
        #        goal[atominfo['player']] = set()
        #    goal[atominfo['player']].add(atominfo['slk'])
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
        dependency[slk_var(head)].append('(ok = true)')
    elif len(body) != 0:
        conjunct = []
        for bd in body:
            if bd['positive'] == True:
                conjunct.append(f'({slk_var(bd)} = true)')
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


        
def parse_content(atom: str, num: int):
    def clean(fluent: str):
        return fluent.replace(',', '_').replace(' ','').replace('(', '_').replace(')', '')

    if num == 1:
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

    #print(atom, 'this case')
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
            print('parse atom', atom)
            slk = parse_content(atom, 0)
    else:
        curr = ''
        for ch in atom:
            if ch == '(':
                break 
            curr += ch
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
        #print('parse rule', rule)
        head = parse_atom(rule)            

    return head, body

# print all the variables for the environment
def print_environment_vars(maxd:int =3):
    print('    Vars:')
    print(f'        counter: 0 .. {maxd};')
    print(f'        init: 0 .. {maxd};')
    print(f'        act_step: boolean;')
    print(f'        ok: boolean;')
    # print the roles
    for r in role:
        print(f'        role_{r}: boolean;')
    # print the base propositions
    for atom in base:
        print(f'        true_{atom}: boolean;')
        print(f'        next_{atom}: boolean;')
    # print the sees and observations
    for r in see.keys():
        for observations in see[r]:
            print(f'        sees_{r}_{observations}_1: boolean;')
            print(f'        sees_{r}_{observations}_1_obs: boolean;')
            print(f'        next_sees_{r}_{observations}_1: boolean;')
    # print the goals
    #for r in goal.keys():
    #    for score in goal[r]:
    #        print(f'        goal_{r}_{score}: boolean;')
    #        print(f'        goal_{r}_{score}_obs: boolean;')
    # print the legals
    for r in legal.keys():
        for atom in legal[r]:
            print(f'        legal_{r}_{atom}: boolean;')
            print(f'        legal_{r}_{atom}_obs: boolean;')
    # print the terminal
    print(f'        terminal: boolean;')
    #print(f'        terminal_obs: boolean;')
    # print the does
    for r in legal.keys():
        for act in legal[r]:
            print(f'        does_{r}_{act}: boolean;')
            print(f'        done_{r}_{act}_1: boolean;')
            print(f'        done_{r}_{act}_1_obs: boolean;')
            print(f'        next_done_{r}_{act}_1: boolean;')
    
    # print other derived predicates
    for atom in other:
        print(f'        {atom}: boolean;')
    print('    end Vars')

def print_evolutions(maxd:int = 3):
    print('    Evolution:')
    print(f'        -- print the counters')
    print('        ok = true if (ok = true);')
    print('        (init = init - 1) if (init > 0);')
    print('        (init = 0) if (init = 0);')
    print(f'       (counter = counter + 1) if !(init <> 0 or (terminal = true and counter = 0) or counter = {maxd});')
    print(f'        (counter = 0) if (init <> 0 or (terminal = true and counter = 0) or counter = {maxd});')
    print(f'        act_step = false if ((init > 1) or (counter < {maxd} and init = 0 and act_step = false) or (counter = {maxd} and init = 0 and act_step = true));')
    print(f'        act_step = true if !((init > 1) or (counter < {maxd} and init = 0 and act_step = false) or (counter = {maxd} and init = 0 and act_step = true));')    
    print()
    print(f'        -- print the dependencies')
    for d in dependency.keys():
        rule = dependency[d]
        if len(rule) == 0:
            print(f'        {d}=false if (ok = true);')
        else:
            cond = '(' + rule[0]
            for i in range (1, len(rule)):
                cond = cond + ' or ' + rule[i]
            cond = cond + ')'
            print(f'        {d}=true if {cond};')
            print(f'        {d}=false if !{cond};')
    print()

    print(f'        -- print the next for actions')
    for r in legal.keys():
        for act in legal[r]:
            print(f'        next_done_{r}_{act}_1 = true if (does_{r}_{act} = true);')
            print(f'        next_done_{r}_{act}_1 = false if !(does_{r}_{act} = true);')
    
    print(f'        -- local observation evolution')
    # evolution of the observation of goals
    #for r in goal.keys():
    #    for score in goal[r]:
    #        print(f'        goal_{r}_{score}_obs = goal_{r}_{score}_obs if !(init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    #        print(f'        goal_{r}_{score}_obs = goal_{r}_{score} if (init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    # print the legals observations
    for r in legal.keys():
        for atom in legal[r]:
            print(f'        legal_{r}_{atom}_obs = legal_{r}_{atom}_obs if !(init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
            print(f'        legal_{r}_{atom}_obs = legal_{r}_{atom} if (init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    # print the sees and observations
    for r in see.keys():
        for observations in see[r]:
            print(f'        sees_{r}_{observations}_1_obs = sees_{r}_{observations}_1_obs if !(init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
            print(f'        sees_{r}_{observations}_1_obs = sees_{r}_{observations}_1 if (init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    
    # print the terminal observations
    #print(f'        terminal_obs = terminal_obs if !(init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    #print(f'        terminal_obs = terminal if (init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    
    # print the does observations
    for r in legal.keys():
        for act in legal[r]:
            print(f'        done_{r}_{act}_1_obs = done_{r}_{act}_1_obs if !(init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
            print(f'        done_{r}_{act}_1_obs = done_{r}_{act}_1 if (init = 1 or (init = 0 and act_step = false and counter = {maxd}));')
    

    # print the evolutions of actions
    for r in legal.keys():
        for act in legal[r]:
            print(f'        does_{r}_{act} = true if (player_{r}.Action = {act} and init = 0 and counter = 0 and act_step = true and terminal = false);')
            print(f'        does_{r}_{act} = false if (counter = {maxd} and act_step = true);')
            print(f'        does_{r}_{act} = does_{r}_{act}  if !((counter = {maxd} and act_step = true) or (player_{r}.Action = {act} and init = 0 and counter = 0 and act_step = true and terminal = false));')
    
    # print the evolutions for true
    for b in base:
        if b in init:
            print(f'        true_{b} = next_{b} if ((init = 0 and act_step = true and counter = {maxd}));')
            print(f'        true_{b} = true if (init = {maxd});')
            print(f'        true_{b} = true_{b} if !((init = 0 and act_step = true and counter = {maxd}) or (init = {maxd}));')
        else:
            print(f'        true_{b} = next_{b} if ((init = 0 and act_step = true and counter = {maxd}));')
            print(f'        true_{b} = true_{b} if !((init = 0 and act_step = true and counter = {maxd}));')


    # print the evolutions for recall
    for r in legal.keys():
        for act in legal[r]:
            print(f'        done_{r}_{act}_1 = next_done_{r}_{act}_1 if ((init = 0 and act_step = true and counter = {maxd}));')
            print(f'        done_{r}_{act}_1 = done_{r}_{act}_1 if !((init = 0 and act_step = true and counter = {maxd}));')
    
    
    for r in see.keys():
        for observations in see[r]:
            print(f'        sees_{r}_{observations}_1 = next_sees_{r}_{observations}_1 if ((init = 0 and act_step = true and counter = {maxd}));')
            print(f'        sees_{r}_{observations}_1 = sees_{r}_{observations}_1 if !((init = 0 and act_step = true and counter = {maxd}));')
    

    print('    end Evolution')


def print_init(maxd:int = 3):
    print('InitStates')
    print(f'    Environment.counter = 0 and Environment.ok = true and Environment.init = {maxd} and Environment.act_step = false')
    for r in role:
        print(f'    and Environment.role_{r} = false')
    for atom in base:
        print(f'    and Environment.true_{atom} = false')
        print(f'    and Environment.next_{atom} = false')
    
    # print the sees and observations
    for r in see.keys():
        for observations in see[r]:
            print(f'    and Environment.sees_{r}_{observations}_1 = false')
            print(f'    and Environment.sees_{r}_{observations}_1_obs = false')
            print(f'    and Environment.next_sees_{r}_{observations}_1 = false')
    # print the goals
    #for r in goal.keys():
    #    for score in goal[r]:
    #        print(f'    and Environment.goal_{r}_{score} = false')
    #        print(f'    and Environment.goal_{r}_{score}_obs = false')
    # print the legals
    for r in legal.keys():
        for atom in legal[r]:
            print(f'    and Environment.legal_{r}_{atom} = false')
            print(f'    and Environment.legal_{r}_{atom}_obs = false')
    # print the terminal
    print(f'    and Environment.terminal = false')
    #print(f'    and Environment.terminal_obs = false')
    # print the does
    for r in legal.keys():
        for act in legal[r]:
            print(f'    and Environment.does_{r}_{act} = false')
            print(f'    and Environment.done_{r}_{act}_1 = false')
            print(f'    and Environment.done_{r}_{act}_1_obs = false')
            print(f'    and Environment.next_done_{r}_{act}_1 = false')
    
    # print other derived predicates
    for atom in other:
        print(f'    and Environment.{atom} = false', end = '')
    print(';')
    print('end InitStates')
    
def print_agent(agent):
    print(f'Agent player_{agent}')
    print('    Lobsvars={init,counter,act_step', end='')
    for observations in see[agent]:
        print(f', sees_{agent}_{observations}_1_obs', end='')
    # print the goals
    #for score in goal[agent]:
    #    print(f', goal_{agent}_{score}_obs', end='')
    # print the legals
    for atom in legal[agent]:
        print(f', legal_{agent}_{atom}_obs', end='')
    # print the terminal
    #print(f', terminal_obs', end='')
    # print the does
    for act in legal[agent]:
        print(f', done_{agent}_{act}_1_obs', end='')
    print('};')
    print('    Vars:')
    print()
    print('    end Vars')
    print('    Actions = {', end = '')
    for act in legal[agent]:
        print(f'{act}, ', end='')
    print('none};')
    print('    Protocol:')
    for act in legal[agent]:
        print(f'        (Environment.init = 0 and Environment.counter = 0 and Environment.act_step = true and Environment.legal_{agent}_{act}_obs = true): ' + '{' + f'{act}' + '};')
    print('        (Environment.counter > 0 or Environment.init > 0 or Environment.act_step = false) : {none};')
    print('        (Environment.counter = 0 and Environment.act_step = true ', end='')
    for act in legal[agent]:
        print(f'and Environment.legal_{agent}_{act}_obs = false ', end='')
    print(') : {none};')
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
    return ans + 1

def writeslk():
    # write the SLK file
    # The Environment Agent
    print('Semantics=SingleAssignment;')
    print()
    print('Agent Environment')
    maxd = longest_chain()
    print_environment_vars(maxd)
    print('    Actions = { none };')
    print('    Protocol:')
    print('        Other: {none};')
    print('    end Protocol')
    print_evolutions(maxd)
    print('end Agent')

    # Other Agents
    for r in role:
        print()
        print_agent(r)
        print()
    # Evaluation
    print('Evaluation\n\nend Evaluation')
    # initial states
    print()
    print_init(maxd)
    print()
    # other information
    print('Groups\nend Groups')
    print()
    print('Fairness\nend Fairness')
    print()
    print('Formulae\n\nend Formulae')

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

def gdl2slk(file):
    construct_dependencies(file)
    writeslk()
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage python translate.py [name of the GDL-II file]')
        sys.exit(1)
    
    gdl2slk(sys.argv[1])
    