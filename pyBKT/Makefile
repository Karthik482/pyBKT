#for python3

#c++ compiler
CXX = g++

#-------------------

PYTHON_INCLUDE_PATH = $(shell python3-config --includes)

O2_LIB = -O2

#where eigen was installed.
EIGEN_INCLUDE_PATH = -I./Eigen

#numpy include path
#this should change for anaconda?
#need to get this more programmaticaly.
#NUMPY_INCLUDE_PATH = -I/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy/core/include
#NUMPY_INCLUDE_PATH = -I/Users/cgaray/anaconda/lib/python3.5/site-packages/numpy/core/include/
NUMPY_INCLUDE_PATH = -I$(shell cat np-include.info)

ALL_OPTS = $(PYTHON_INCLUDE_PATH) $(O2_LIB) $(EIGEN_INCLUDE_PATH) \
$(NUMPY_INCLUDE_PATH)

#-------------------

#change python-config for python3-config on python3 (works with Anaconda).
#or complete the paths and libraries manually.

#where the dylib files are located.
PYTHON_LIB_PATH = $(shell python3-config --exec-prefix)/lib

#basic python libs
PYTHON_LIBS = $(shell python3-config --libs)

#boost-python lib path.
#need to get this more programmaticaly.
BOOST_PYTHON_LIB_PATH = $(shell ldconfig -p | grep libboost_python | sort -r | head -n1 | cut -d">" -f2 | xargs | sed 's/libboost.*//')

#boost-python libs
BOOST_PYTHON_LIBS = -l$(shell ldconfig -p | grep libboost_python | sort -r | head -n1 | cut -d">" -f1 | xargs | sed 's/\.so.*//' | sed 's/.*lib//')

#openmp libs
OPENMP_LIBS = -fopenmp

ALL_LIBS = -L$(PYTHON_LIB_PATH) $(PYTHON_LIBS) -L$(BOOST_PYTHON_LIB_PATH) \
$(BOOST_PYTHON_LIBS) $(OPENMP_LIBS)

#-------------------

default:
	@python3 setup.py

setup: generate/synthetic_data_helper.so fit/E_step.so fit/predict_onestep_states.so
	@python3 test/hand_specified_model3.py
	@rm -f np-include.info

generate/synthetic_data_helper.so: generate/synthetic_data_helper.o
	@$(CXX) $< $(ALL_LIBS) -Wl,-rpath,$(PYTHON_LIB_PATH) -shared -o $@ -w

generate/synthetic_data_helper.o: generate/synthetic_data_helper.cpp Makefile
	@$(CXX) $< $(ALL_OPTS) -c -fPIC -o $@ -w

fit/E_step.so: fit/E_step.o
	@$(CXX) $< $(ALL_LIBS) -Wl,-rpath,$(PYTHON_LIB_PATH) -shared -o $@ -w

fit/E_step.o: fit/E_step.cpp Makefile
	@$(CXX) $< $(ALL_OPTS) -c -fPIC -o $@ -w

fit/predict_onestep_states.so: fit/predict_onestep_states.o
	@$(CXX) $< $(ALL_LIBS) -Wl,-rpath,$(PYTHON_LIB_PATH) -shared -o $@ -w

fit/predict_onestep_states.o: fit/predict_onestep_states.cpp Makefile
	@$(CXX) $< $(ALL_OPTS) -c -fPIC -o $@ -w

clean:
	rm -rf generate/*.so generate/*.o fit/*.so fit/*.o

.PHONY: default clean
