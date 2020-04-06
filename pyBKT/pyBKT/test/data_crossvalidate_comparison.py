import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit
from pyBKT.test import crossvalidate
from pyBKT.util import data_helper, check_data
import copy

#parameters classes
num_gs = 1 #number of guess/slip classes

num_fit_initializations = 20
skill_name = "Probability of Two Distinct Events"

#data!
data = data_helper.assistments_data(skill_name)

data_onelearnrate = copy.deepcopy(data)
temp = [1] * len(data_onelearnrate["resources"]) #manually set every resource to be the same (1)
data_onelearnrate["resources"]=np.asarray(temp)
print(data_onelearnrate["resources"].shape, data["resources"].shape)
check_data.check_data(data_onelearnrate)

print("Model using only 1 resource:")
crossvalidate.crossvalidate(data_onelearnrate, num_gs, 1)

check_data.check_data(data)
num_learns = len(data["resource_names"])
print("Model using %d resources:" % num_learns)
crossvalidate.crossvalidate(data, num_gs, num_learns)