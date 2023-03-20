from z3 import *
x = Int('x')
y = Int('y')
# solve(x<31,x>=0,y>=0,y<31, x + (30-y)*31 == 924)
solve(x<60,x>=0,y>=0,y<60, x + y*60 == 916 )
