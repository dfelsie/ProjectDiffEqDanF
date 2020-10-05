import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dy/dt
def model(y,t):
    dydt =  0.3*t
    return dydt

def fun(y,t):
    return y**2-5*y-6


# initial condition
y0 = 5

# time points
t = np.linspace(0,1)

# solve ODE
y = odeint(fun,y0,t)
y1=odeint(fun,6.001,t)
y2=odeint(fun,-1.1,t)


# plot results
plt.plot(t,y)
plt.plot(t,y1)
plt.plot(t,y2)
plt.xlabel('time')
plt.ylabel('y')
plt.title('Q8')
plt.show()


