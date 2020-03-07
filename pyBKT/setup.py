import numpy as np, os

f = open("np-include.info", "w")
f.write(np.get_include() + "\n")
f.close()

os.system('make')
