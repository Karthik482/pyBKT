#########################################
# setup.py                              #
# Setup for PyBKT                       #
#                                       #
# @author Anirudhan Badrinath           #
# Last edited: 07 March 2020            #
#########################################

import numpy as np, os
from shutil import copyfile

FILES = {'Makefile': './', 'synthetic_data_helper.cpp': './generate/',
         'predict_onestep_states.cpp': './fit/', 'E_step.cpp': './fit/'}

def boost_version():
    os.system("cat $(whereis boost | awk '{print $2}')/version.hpp | grep \"#define BOOST_LIB_VERSION\" | awk '{print $3}' | sed 's\\\"\\\\g' | cut -d\"_\" -f2 > np-include.info")
    return int(open("np-include.info", "r").read().strip())

def copy_files(l, s):
    for i in l:
        copyfile(s + "/" + i, l[i] + "/" + i)

if boost_version() < 65:
    copy_files(FILES, '.DEPRECATED')
else:
    copy_files(FILES, '.NEW')

f = open("np-include.info", "w")
f.write(np.get_include() + "\n")
f.close()

os.system('make setup')
