import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit
from pyBKT.util import data_helper, check_data
from copy import deepcopy

#parameters classes
num_gs = 2 #number of guess/slip classes

num_fit_initializations = 20
skill_name = "Probability of Two Distinct Events"

data = data_helper.assistments_data(skill_name)
check_data.check_data(data)
num_learns = len(data["resource_names"])

data_temp = [[],[]]
for i in range(len(data["resources"])):
    for j in range(num_gs):
        if data["resources"][i] == j+1:
            data_temp[j].append(data["data"][0][i])
        else:
            data_temp[j].append(0)
data["data"] = np.asarray(data_temp, dtype='int32')
print(data_temp[0])
print(data_temp[1])
#data["resources"] = np.asarray(resource_temp)
#fit models, starting with random initializations

num_fit_initializations = 5
best_likelihood = float("-inf")

for i in range(num_fit_initializations):
	fitmodel = random_model_uni.random_model_uni(num_learns, num_gs) # include this line to randomly set initial param values
	(fitmodel, log_likelihoods) = EM_fit.EM_fit(fitmodel, data)
	if(log_likelihoods[-1] > best_likelihood):
		best_likelihood = log_likelihoods[-1]
		best_model = fitmodel

# compare the fit model to the true model

#print(best_model['As'])
#print(best_model['guesses'])
print('')
print('Trained model for %s skill given %d learning rates, %d guess/slip rate' % (skill_name, num_learns, num_gs))
print('\t\tlearned')
print('prior\t\t%.4f' % (best_model["pi_0"][1][0]))
for key, value in data["resource_names"].items():
    print('Learn: %s\t\t%.4f' % (key, best_model['As'][value-1, 1, 0].squeeze()))
for key, value in data["resource_names"].items():
    print('Forget: %s\t\t%.4f' % (key, best_model['As'][value-1, 0, 1].squeeze()))

for s in range(num_gs):
    print('guess%d\t\t%.4f' % (s+1, best_model['guesses'][s]))
for s in range(num_gs):
    print('slip%d\t\t%.4f' % (s+1, best_model['slips'][s]))
