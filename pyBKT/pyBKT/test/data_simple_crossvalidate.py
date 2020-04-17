import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit
from pyBKT.test import crossvalidate
from pyBKT.util import assistments_data_helper, check_data
from copy import deepcopy


num_fit_initializations = 20
skill_name = "Box and Whisker"

#data!
data = assistments_data_helper.assistments_data("https://drive.google.com/uc?export=download&id=0B3f_gAH-MpBmUmNJQ3RycGpJM0k", skill_name)
check_data.check_data(data)
num_learns = len(data["resource_names"])
num_gs = len(data["gs_names"])

crossvalidate.crossvalidate(data, num_gs, num_learns, verbose=True)