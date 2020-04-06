import sys
sys.path.append('../')
import numpy as np
from pyBKT.generate import synthetic_data, random_model_uni
from pyBKT.fit import EM_fit, predict_onestep
from pyBKT.test import accuracy
from pyBKT.util import data_helper, check_data
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from copy import deepcopy

#data only for the indices given
def fix_data(data, indices):
    training_data = {}
    resources = []
    d = []
    start_temp = [data["starts"][i] for i in indices]
    length_temp = [data["lengths"][i] for i in indices]
    training_data["resource_names"] = data["resource_names"]
    starts = []
    for i in range(len(start_temp)):
        starts.append(len(resources)+1)
        resources.extend(data["resources"][start_temp[i]:start_temp[i]+length_temp[i]])
        d.extend(data["data"][0][start_temp[i]:start_temp[i]+length_temp[i]])
    training_data["starts"] = np.asarray(starts)
    training_data["lengths"] = np.asarray(length_temp)
    training_data["data"] = np.asarray([d],dtype='int32')
    resource=np.asarray(resources)
    stateseqs=np.copy(resource)
    training_data["stateseqs"]=np.asarray([stateseqs],dtype='int32')
    training_data["resources"]=resource
    training_data=(training_data)
    return training_data

def crossvalidate(data, num_gs, num_learns, verbose=False):
    folds = 5
    total = 0
    num_fit_initializations = 20
    kf = KFold(folds)
    iteration = 0
    
    for train, test in kf.split(data["starts"]): #crossvalidation on students, split into 5 groups by default
        iteration += 1
        training_data = fix_data(data, train)

        num_fit_initializations = 5
        best_likelihood = float("-inf")
        
        for i in range(num_fit_initializations):
        	fitmodel = random_model_uni.random_model_uni(num_learns, num_gs) # include this line to randomly set initial param values
        	(fitmodel, log_likelihoods) = EM_fit.EM_fit(fitmodel, training_data)
        	if(log_likelihoods[-1] > best_likelihood):
        		best_likelihood = log_likelihoods[-1]
        		best_model = fitmodel
        		
        if verbose:
            print(" ")
            print('Iteration %d' % (iteration))
            print('Trained model given 1 learning rate, 1 guess/slip rate')
            print('\tlearned')
            print('prior\t%.4f' % (best_model["pi_0"][1][0]))
            for r in range(num_learns):
                print('learn%d\t%.4f' % (r+1, best_model['As'][r, 1, 0].squeeze()))
            for r in range(num_learns):
                print('forget%d\t%.4f' % (r+1, best_model['As'][r, 0, 1].squeeze()))
            
            for s in range(num_gs):
                print('guess%d\t%.4f' % (s+1, best_model['guesses'][s]))
            for s in range(num_gs):
                print('slip%d\t%.4f' % (s+1, best_model['slips'][s]))
            
        test_data = fix_data(data, test)
        (correct_predictions, state_predictions) = predict_onestep.run(best_model, test_data)
        
        total += accuracy.compute_accuracy(test_data["data"], correct_predictions)
    print("Average RMSE: ", total/folds)
    
