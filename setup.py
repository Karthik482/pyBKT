#########################################
# setup.py                              #
# Setup for PyBKT                       #
#                                       #
# @author Anirudhan Badrinath           #
# Last edited: 07 March 2020            #
#########################################

import numpy as np, os
import sys
from shutil import copyfile
import subprocess as s
from distutils.core import setup, Extension

os.chdir('pyBKT')

FILES = {'synthetic_data_helper.cpp': './generate/',
         'predict_onestep_states.cpp': './fit/', 'E_step.cpp': './fit/'}
ALL_COMPILE_ARGS = ['-c', '-fPIC', '-w']
ALL_LINK_ARGS = ['-fopenmp']
ALL_LIBRARIES = ['crypt', 'pthread', 'dl', 'util', 'm']
INCLUDE_DIRS = sys.path + [np.get_include(), 'pyBKT/Eigen/']
LIBRARY_DIRS = [] 

def find_library_dirs():
    lst = []
    os.system("whereis libboost_python | cut -d' ' -f 2 | sed 's/libboost.*//' > np-include.info")
    lst.append(open("np-include.info", "r").read().strip())
    os.system("python3-config --exec-prefix > np-include.info")
    lst.append(open("np-include.info", "r").read().strip() + "/lib")
    return lst

def find_dep_lib_dirs():
    lst = []
    os.system("ldconfig -p | grep libboost_python | sort -r | head -n1 | cut -d\">\" -f2 | xargs | sed 's/libboost.*//' > np-include.info")
    lst.append(open("np-include.info", "r").read().strip())
    os.system("python3-config --exec-prefix > np-include.info")
    lst.append(open("np-include.info", "r").read().strip() + "/lib")
    return lst

def find_dep_lib_name():
    os.system("ldconfig -p | grep libboost_python | sort -r | head -n1 | cut -d'>' -f1 | xargs | sed 's/.so.*//' | sed 's/.*lib//' > np-include.info")
    return open("np-include.info", "r").read().strip()

def find_boost_version():
    os.system("cat $(whereis boost | awk '{print $2}')/version.hpp | grep \"#define BOOST_LIB_VERSION\" | awk '{print $3}' | sed 's\\\"\\\\g' > np-include.info")
    return int(open("np-include.info", "r").read().strip().replace('_', ''))

def copy_files(l, s):
    for i in l:
        copyfile(s + "/" + i, l[i] + "/" + i)

def clean():
    os.remove('np-include.info')

if find_boost_version() < 165:
    copy_files(FILES, '.DEPRECATED')
    LIBRARY_DIRS = find_dep_lib_dirs()
    ALL_LIBRARIES.append(find_dep_lib_name())
else:
    copy_files(FILES, '.NEW')
    LIBRARY_DIRS = find_library_dirs()
    ALL_LIBRARIES += ['boost_python3', 'boost_numpy3']

clean()

os.chdir('..')

module1 = Extension('pyBKT/generate/synthetic_data_helper', sources = ['pyBKT/generate/synthetic_data_helper.cpp'], include_dirs = INCLUDE_DIRS,
                    extra_compile_args = ALL_COMPILE_ARGS,
                    library_dirs = LIBRARY_DIRS, 
                    libraries = ALL_LIBRARIES, 
                    extra_link_args = ALL_LINK_ARGS)

module2 = Extension('pyBKT/fit/E_step', sources = ['pyBKT/fit/E_step.cpp'], include_dirs = INCLUDE_DIRS,
                    extra_compile_args = ALL_COMPILE_ARGS,
                    library_dirs = LIBRARY_DIRS, 
                    libraries = ALL_LIBRARIES, 
                    extra_link_args = ALL_LINK_ARGS)

module3 = Extension('pyBKT/fit/predict_onestep_states', sources = ['pyBKT/fit/predict_onestep_states.cpp'], include_dirs = INCLUDE_DIRS,
                    extra_compile_args = ALL_COMPILE_ARGS,
                    library_dirs = LIBRARY_DIRS, 
                    libraries = ALL_LIBRARIES, 
                    extra_link_args = ALL_LINK_ARGS)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyBKT",
    version="1.3",
    author="Anirudhan Badrinath",
    author_email="abadrinath@berkeley.edu",
    description="PyBKT",
    url="https://github.com/CAHLR/pyBKT",
    packages=['pyBKT', 'pyBKT.generate', 'pyBKT.fit', 'pyBKT.util'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules = [module1, module2, module3]
)
