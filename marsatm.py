import os
# Constants
g = 3.711
R = 191.84

def marsinit(filename):
    with open(filename,'r') as f:
        marstable = [line.rstrip().split() for line in f]
        marstable = marstable[2:17]
    return marstable

def marsatm(h, marstable):
    alt = h/1000
    for line in range(len(marstable)):
        if float(marstable[line + 1][0]) > alt >= float(marstable[line][0]):
            k = (alt - float(marstable[line][0]))/(float(marstable[line + 1][0])-float(marstable[line][0]))
            temp = (1-k) * float(marstable[line][1]) + k * float(marstable[line+1][1])
            rho = (1 - k) * float(marstable[line][2]) + k * float(marstable[line + 1][2])
            c = (1-k) * float(marstable[line][3]) + k * float(marstable[line +1][3])
            p = rho * R * temp
            return temp, rho, c, p

marstable = marsinit("data/marsatm.txt")

