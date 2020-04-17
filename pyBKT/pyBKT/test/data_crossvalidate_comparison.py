import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit
from pyBKT.test import crossvalidate
from pyBKT.util import assistments_data_helper, check_data
import copy

#parameters classes
num_gs = 1 #number of guess/slip classes

num_fit_initializations = 20
skill_name = "Probability of Two Distinct Events"

#data!
data = assistments_data_helper.assistments_data("https://drive.google.com/uc?export=download&id=0B3f_gAH-MpBmUmNJQ3RycGpJM0k", skill_name, resource_name = "answer_type")
num_learns = len(data["resource_names"])
num_gs = len(data["gs_names"])

data_onelearnrate = assistments_data_helper.assistments_data("https://drive.google.com/uc?export=download&id=0B3f_gAH-MpBmUmNJQ3RycGpJM0k", skill_name, resource_name = None)

check_data.check_data(data_onelearnrate)

print("Model using only 1 resource:")
crossvalidate.crossvalidate(data_onelearnrate, num_gs, 1)
print(" ")
check_data.check_data(data)
num_learns = len(data["resource_names"])
print("Model using %d resources:" % num_learns)
crossvalidate.crossvalidate(data, num_gs, num_learns)