#for python3

#c++ compiler
CXX = g++

#-------------------

PYTHON_INCLUDE_PATH = $(shell python3-config --includes)

O2_LIB = -O2

EIGEN_INCLUDE_PATH = -I./Eigen

# BOOST_PYTHON_INCLUDE_PATH = -I$(shell whereis boost | awk '{print $2}')

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
BOOST_PYTHON_LIB_PATH = -L$(shell whereis libboost_python | cut -d' ' -f 2 | sed 's/libboost.*//')

BOOST_NUMPY_PATH = -L$(shell whereis libboost_numpy | cut -d' ' -f 2 | sed 's/libboost.*//')

#boost-python libs
BOOST_PYTHON_LIBS = -lboost_python3 -lboost_numpy3 

#openmp libs
OPENMP_LIBS = -fopenmp

ALL_LIBS = -L$(PYTHON_LIB_PATH) $(PYTHON_LIBS) $(BOOST_PYTHON_LIB_PATH) \
$(BOOST_PYTHON_LIBS) $(BOOST_NUMPY_PATH) $(OPENMP_LIBS)

#-------------------

default: generate/synthetic_data_helper.so fit/E_step.so fit/predict_onestep_states.so
	@python test/hand_specified_model3.py

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
