import marsatm
import matplotlib.pyplot as plt
import math

# Constants
CDS = 4.92    #m^2
ve = 4400.0    #m/s
mzfw = 699.0        #kg
g0 = 3.711       #m/s
dt = 0.01           #s
Kv = 0.05
s = "n"
mdot = 0.0  #kg/s
thrust = 0.0

def flight():
    global dt
    global g0
    global mzfw
    global CDS
    global s
    global mdot

    # initialise values
    t = 0.0     #s
    x = 0.0     #m
    y = 20000   #m
    V = 262.0   #m/s
    gamma = math.radians(-20.0) #rad
    Vx = V * math.cos(gamma)    #m/s
    Vy = V * math.sin(gamma)    #m/s
    mf = float(input("Input fuel mass in kilograms"))
    s = input("would you like to do a suicide burn? ('y' for yes / 'n' for no + enter)")
    ht = float(input("Input burn altitude here"))


    # Create tables
    ttab = []
    xtab = []
    ytab = []
    vtab = []
    mdottab = []
    gammatab = []

    marstable = marsatm.marsinit("data/marsatm.txt")

    while y > 0.0:
        temp, rho, c, p = marsatm.marsatm(y, marstable)
        t = t + dt
        m = mzfw + mf

        Fdrag = 0.5 * rho * V ** 2.0 * CDS
        Fgrav = m * g0

        Fthrust, mdot, dVy = thrusters(m, y, ht, Vy)

        Fx = (Fdrag + Fthrust) * (- Vx / V)
        Fy = (Fdrag + Fthrust) * (- Vy / V) - Fgrav

        ax = Fx / m
        ay = Fy / m

        mf = mf - mdot * dt

        Vx = Vx + ax * dt
        Vy = Vy + ay * dt

        V = math.sqrt(Vx ** 2.0 + Vy ** 2.0)
        gamma = math.degrees(math.atan2(Vy, Vx))

        x = x + Vx * dt
        y = y + Vy * dt
        ttab.append(t)
        xtab.append(x)
        ytab.append(y)
        vtab.append(V)
        mdottab.append(mdot)
        gammatab.append(gamma)

    print("Maximum velocity reached: ", max(vtab))

    # Plotting
    plt.figure()
    plt.subplot(231)
    plt.title("Trajectory")
    plt.plot(xtab, ytab)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.subplot(232)
    plt.title("Altitude vs speed")
    plt.plot(vtab, ytab)

    plt.subplot(233)
    plt.title("Mass flow vs time")
    plt.plot(ttab, mdottab)

    plt.subplot(234)
    plt.title("Altitude vs time")
    plt.plot(ttab, ytab)

    plt.subplot(235)
    plt.title("Speed vs time")
    plt.plot(ttab, vtab)

    plt.subplot(236)
    plt.title("Gamma vs time")
    plt.plot(ttab, gammatab)

    plt.show()



def thrusters(m, y, ht, Vy):
    global g0, Kv, ve, s
    Vyref = -2.0

    if m > 699.0 and 0.3 <= y <= ht:

        # suicide burn
        if s == "y":
            mdot = 5.0

        # Mdot calculation
        else:
            dVy = Vyref - Vy
            mdot = (m * g0 / ve) + Kv * dVy
            if mdot >= 5.0:
                mdot = 5.0

        thrust = mdot * ve

    else:
        thrust = 0
        mdot = 0
    return thrust, mdot, Vy

def suicide(cond):
    global mdot
    if cond == "y":
        mdot = 5.0
    return mdot

flight()
