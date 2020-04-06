import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit
from pyBKT.test import crossvalidate
from pyBKT.util import data_helper, check_data
from copy import deepcopy

#parameters classes
num_gs = 1 #number of guess/slip classes

num_fit_initializations = 20
skill_name = "Box and Whisker"

#data!
data = data_helper.assistments_data(skill_name)
check_data.check_data(data)
num_learns = len(data["resource_names"])

crossvalidate.crossvalidate(data, num_gs, num_learns, verbose=True)