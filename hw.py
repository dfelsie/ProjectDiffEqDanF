import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(-1,1,10) #collection of 50 evenly space points between 0 and 20 that act as test ponts

square=np.tanh(20*np.sin(12*x))+(2/100)*np.exp(3*x)*np.sin(300*x)
ot=(1/(1+1000*(x+.5)**2))+1/(np.sqrt(1+1000*(x-.5)**2))
plt.xlim(left=-1)
plt.xlim(right=1)
plt.xlabel("time t")
plt.title("Q7")

plt.plot(x,square,'r--', label="graph of tanh func",color="black")
plt.plot(x,ot,'r--', label= "graph of sqrt func",color="black",ls=":")

plt.legend()
plt.show()