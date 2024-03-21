role(x).
role(o).


init(cell(1,1,b)).
init(cell(1,2,b)).
init(cell(2,1,b)).
init(cell(2,2,b)).
init(control(x)).

legal(o, noop) :- true(control(x)).
legal(x, noop) :- true(control(o)).

legal(x, mark(1, 1)) :- \+ true(tried(x, 1, 1)), true(control(x)).
legal(x, mark(1, 2)) :- \+ true(tried(x, 1, 2)), true(control(x)).
legal(x, mark(2, 1)) :- \+ true(tried(x, 2, 1)), true(control(x)).
legal(x, mark(2, 2)) :- \+ true(tried(x, 2, 2)), true(control(x)).


legal(o, mark(1, 1)) :- \+ true(tried(o, 1, 1)), true(control(o)).
legal(o, mark(1, 2)) :- \+ true(tried(o, 1, 2)), true(control(o)).
legal(o, mark(2, 1)) :- \+ true(tried(o, 2, 1)), true(control(o)).
legal(o, mark(2, 2)) :- \+ true(tried(o, 2, 2)), true(control(o)).

next(tried(x, 1, 1)) :- does(x, mark(1, 1)).
next(tried(x, 1, 2)) :- does(x, mark(1, 2)).
next(tried(x, 2, 1)) :- does(x, mark(2, 1)).
next(tried(x, 2, 2)) :- does(x, mark(2, 2)).


next(tried(o, 1, 1)) :- does(o, mark(1, 1)).
next(tried(o, 1, 2)) :- does(o, mark(1, 2)).
next(tried(o, 2, 1)) :- does(o, mark(2, 1)).
next(tried(o, 2, 2)) :- does(o, mark(2, 2)).

next(tried(x, 1, 1)) :- true(tried(x, 1, 1)).
next(tried(x, 1, 2)) :- true(tried(x, 1, 2)).
next(tried(x, 2, 1)) :- true(tried(x, 2, 1)).
next(tried(x, 2, 2)) :- true(tried(x, 2, 2)).

next(tried(o, 1, 1)) :- true(tried(o, 1, 1)).
next(tried(o, 1, 2)) :- true(tried(o, 1, 2)).
next(tried(o, 2, 1)) :- true(tried(o, 2, 1)).
next(tried(o, 2, 2)) :- true(tried(o, 2, 2)).

sees(x,success) :- does(x, mark(1,1)), true(cell(1, 1, b)).
next(cell(1,1,x)) :- does(x, mark(1,1)), true(cell(1, 1, b)).
next(control(o)) :- does(x, mark(1,1)), true(cell(1, 1, b)).
sees(x,fail) :- does(x, mark(1,1)), true(cell(1, 1, o)).
next(control(x)) :- does(x, mark(1,1)), true(cell(1, 1, o)).

sees(x,success) :- does(x, mark(1,2)), true(cell(1, 2, b)).
next(cell(1,2,x)) :- does(x, mark(1,2)), true(cell(1, 2, b)).
next(control(o)) :- does(x, mark(1,2)), true(cell(1, 2, b)).
sees(x,fail) :- does(x, mark(1,2)), true(cell(1, 2, o)).
next(control(x)) :- does(x, mark(1,2)), true(cell(1, 2, o)).

sees(x,success) :- does(x, mark(2,1)), true(cell(2, 1, b)).
next(cell(2,1,x)) :- does(x, mark(2,1)), true(cell(2, 1, b)).
next(control(o)) :- does(x, mark(2,1)), true(cell(2, 1, b)).
sees(x,fail) :- does(x, mark(2,1)), true(cell(2, 1, o)).
next(control(x)) :- does(x, mark(2,1)), true(cell(2, 1, o)).

sees(x,success) :- does(x, mark(2,2)), true(cell(2, 2, b)).
next(cell(2,2,x)) :- does(x, mark(2,2)), true(cell(2, 2, b)).
next(control(o)) :- does(x, mark(2,2)), true(cell(2, 2, b)).
sees(x,fail) :- does(x, mark(2,2)), true(cell(2, 2, o)).
next(control(x)) :- does(x, mark(2,2)), true(cell(2, 2, o)).


sees(o,success) :- does(o, mark(1,1)), true(cell(1, 1, b)).
next(cell(1,1,o)) :- does(o, mark(1,1)), true(cell(1, 1, b)).
next(control(x)) :- does(o, mark(1,1)), true(cell(1, 1, b)).
sees(o,fail) :- does(o, mark(1,1)), true(cell(1, 1, x)).
next(control(o)) :- does(o, mark(1,1)), true(cell(1, 1, x)).

sees(o,success) :- does(o, mark(1,2)), true(cell(1, 2, b)).
next(cell(1,2,o)) :- does(o, mark(1,2)), true(cell(1, 2, b)).
next(control(x)) :- does(o, mark(1,2)), true(cell(1, 2, b)).
sees(o,fail) :- does(o, mark(1,2)), true(cell(1, 2, x)).
next(control(o)) :- does(o, mark(1,2)), true(cell(1, 2, x)).


sees(o,success) :- does(o, mark(2,1)), true(cell(2, 1, b)).
next(cell(2,1,o)) :- does(o, mark(2,1)), true(cell(2, 1, b)).
next(control(x)) :- does(o, mark(2,1)), true(cell(2, 1, b)).
sees(o,fail) :- does(o, mark(2,1)), true(cell(2, 1, x)).
next(control(o)) :- does(o, mark(2,1)), true(cell(2, 1, x)).

sees(o,success) :- does(o, mark(2,2)), true(cell(2, 2, b)).
next(cell(2,2,o)) :- does(o, mark(2,2)), true(cell(2, 2, b)).
next(control(x)) :- does(o, mark(2,2)), true(cell(2, 2, b)).
sees(o,fail) :- does(o, mark(2,2)), true(cell(2, 2, x)).
next(control(o)) :- does(o, mark(2,2)), true(cell(2, 2, x)).

next(cell(1, 1, x)):- true(cell(1, 1, x)).
next(cell(1, 1, o)):- true(cell(1, 1, o)).
next(cell(1, 2, x)):- true(cell(1, 2, x)).
next(cell(1, 2, o)):- true(cell(1, 2, o)).
next(cell(2, 1, x)):- true(cell(2, 1, x)).
next(cell(2, 1, o)):- true(cell(2, 1, o)).
next(cell(2, 2, x)):- true(cell(2, 2, x)).
next(cell(2, 2, o)):- true(cell(2, 2, o)).



next(cell(1, 1, b)):- \+ affect(cell(1, 1)), true(cell(1, 1, b)).
next(cell(1, 2, b)):- \+ affect(cell(1, 2)), true(cell(1, 2, b)).
next(cell(2, 1, b)):- \+ affect(cell(2, 1)), true(cell(2, 1, b)).
next(cell(2, 2, b)):- \+ affect(cell(2, 2)), true(cell(2, 2, b)).
affect(cell(1, 1)) :- does(x, mark(1,1)), true(cell(1, 1, b)).
affect(cell(1, 2)) :- does(x, mark(1,2)), true(cell(1, 2, b)).
affect(cell(2, 1)) :- does(x, mark(2,1)), true(cell(2, 1, b)).
affect(cell(2, 2)) :- does(x, mark(2,2)), true(cell(2, 2, b)).


affect(cell(1, 1)) :- does(o, mark(1,1)), true(cell(1, 1, b)).
affect(cell(1, 2)) :- does(o, mark(1,2)), true(cell(1, 2, b)).
affect(cell(2, 1)) :- does(o, mark(2,1)), true(cell(2, 1, b)).
affect(cell(2, 2)) :- does(o, mark(2,2)), true(cell(2, 2, b)).

line(x) :- true(cell(1, 1, x)), true(cell(1, 2, x)).
line(x) :- true(cell(2, 1, x)), true(cell(2, 2, x)).

line(x) :- true(cell(1, 1, x)), true(cell(2, 1, x)).
line(x) :- true(cell(1, 2, x)), true(cell(2, 2, x)).


line(o) :- true(cell(1, 1, o)), true(cell(1, 2, o)).
line(o) :- true(cell(2, 1, o)), true(cell(2, 2, o)).


line(o) :- true(cell(1, 1, o)), true(cell(2, 1, o)).
line(o) :- true(cell(1, 2, o)), true(cell(2, 2, o)).


terminal :- \+ true(cell(1,1,b)), \+ true(cell(1,2,b)), \+ true(cell(2,1,b)), \+ true(cell(2,2,b)).
terminal :- line(x).
terminal :- line(o).
goal(x, 50) :- \+ line(x), \+ line(o).
goal(o, 50) :- \+ line(x), \+ line(o).
goal(x, 100) :- line(x).
goal(o, 0) :- line(x).
goal(o, 100) :- line(o).
goal(x, 0) :- line(o).
