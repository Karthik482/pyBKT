//  UPDATED FILE
//
//  synthetic_data_helper.cpp
//  synthetic_data_helper
//
//  Created by CristiÃƒÂ¡n Garay on 10/15/16.
//  Copyright Ã‚Â© 2016 Cristian Garay. All rights reserved.
//

#define NPY_NO_DEPRECATED_API NPY_1_11_API_VERSION

#include <iostream>
#include <stdint.h>
#include <alloca.h>
#include <Eigen/Core>
#include <boost/python.hpp>
#include <numpy/ndarrayobject.h>
#include <boost/python/numpy.hpp>
#include <boost/python/ptr.hpp>
#include <Python.h>


using namespace Eigen;
using namespace std;
using namespace boost::python;
namespace np = boost::python::numpy;

#if PY_VERSION_HEX >= 0x03000000
void *
#else
void
#endif
init_numpy(){
    //Py_Initialize;
    import_array();
}


struct double_to_python_float
{
    static PyObject* convert(double const& d)
      {
        return boost::python::incref(
          boost::python::object(d).ptr());
      }
};

//numpy scalar converters.
template <typename T, NPY_TYPES NumPyScalarType>
struct enable_numpy_scalar_converter
{
  enable_numpy_scalar_converter()
  {
    // Required NumPy call in order to use the NumPy C API within another
    // extension module.
    // import_array();
    init_numpy();

    boost::python::converter::registry::push_back(
      &convertible,
      &construct,
      boost::python::type_id<T>());
  }

  static void* convertible(PyObject* object)
  {
    // The object is convertible if all of the following are true:
    // - is a valid object.
    // - is a numpy array scalar.
    // - its descriptor type matches the type for this converter.
    return (
      object &&                                                    // Valid
      PyArray_CheckScalar(object) &&                               // Scalar
      PyArray_DescrFromScalar(object)->type_num == NumPyScalarType // Match
    )
      ? object // The Python object can be converted.
      : NULL;
  }

  static void construct(
    PyObject* object,
    boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    // Obtain a handle to the memory block that the converter has allocated
    // for the C++ type.
    namespace python = boost::python;
    typedef python::converter::rvalue_from_python_storage<T> storage_type;
    void* storage = reinterpret_cast<storage_type*>(data)->storage.bytes;

    // Extract the array scalar type directly into the storage.
    PyArray_ScalarAsCtype(object, storage);

    // Set convertible to indicate success.
    data->convertible = storage;
  }
};

dict create_synthetic_data(dict& model, numpy::ndarray& starts, numpy::ndarray& lengths, numpy::ndarray& resources){
    //TODO: check if parameters are null.
    //TODO: check that dicts have the required members.
    //TODO: check that all parameters have the right sizes.
    //TODO: i'm not sending any error messages.
    
    numpy::ndarray learns = extract<numpy::ndarray>(model["learns"]);
    int num_resources = len(learns);

    numpy::ndarray forgets = extract<numpy::ndarray>(model["forgets"]);
    numpy::ndarray guesses = extract<numpy::ndarray>(model["guesses"]);
    
    numpy::ndarray slips = extract<numpy::ndarray>(model["slips"]);
    int num_subparts = len(slips);
    
    Vector2d initial_distn;
    double prior = extract<double>(model["prior"]);
    initial_distn << 1-prior, prior;
    
    MatrixXd As(2, 2*num_resources);
    for (int n=0; n<num_resources; n++) {
        double learn = extract<double>(learns[n]);
        double forget = extract<double>(forgets[n]);
        As.col(2*n) << 1-learn, learn;
        As.col(2*n+1) << forget, 1-forget;
    }
    
    int num_sequences = len(starts);
    
    long int bigT = 0;
    for (int k=0; k<num_sequences; k++) {
        bigT += extract<long int>(lengths[k]); //extract this as int??
    }
    
    //// outputs
    int all_stateseqs[1][bigT]; //used to be int8_t
    int all_data[num_subparts][bigT]; //used to be int8_t
    all_data[0][0] = 0;
    dict result;
    
    /* COMPUTATION */
    
    for (int sequence_index=0; sequence_index < num_sequences; sequence_index++) {
        long int sequence_start = extract<long int>(starts[sequence_index]) - 1; //should i extract these as ints?
        long int T = extract<long int>(lengths[sequence_index]);
        
        Vector2d nextstate_distr = initial_distn;

        for (int t=0; t<T; t++) {
            all_stateseqs[0][sequence_start + t] = nextstate_distr(0) < ((double) rand()) / ((double) RAND_MAX); //always all_stateseqs[0]?
            for (int n=0; n<num_subparts; n++) {
                all_data[n][sequence_start+t] = ((all_stateseqs[0][sequence_start + t]) ? extract<double>(slips[n]) : (1-extract<double>(guesses[n]))) < (((double) rand()) / ((double) RAND_MAX));
            }
            
            nextstate_distr = As.col(2*(extract<long int>(resources[sequence_start + t])-1)+all_stateseqs[0][sequence_start + t]); //extract int is right??
        }
    }
    
    //wrapping results in numpy objects.
    //npy_intp all_stateseqs_dims[2] = {1, bigT}; //just put directly this array into the PyArray_SimpleNewFromData function?
    //PyObject * all_stateseqs_pyObj = PyArray_SimpleNewFromData(2, all_stateseqs_dims, NPY_INT, all_stateseqs); //this should be NPY_INT8.
    //boost::python::handle<> all_stateseqs_handle( all_stateseqs_pyObj );
    //np::ndarray all_stateseqs_handle_arr = np::array(all_stateseqs);
    
    //npy_intp all_data_dims[2] = {num_subparts, bigT}; //just put directly this array into the PyArray_SimpleNewFromData function?
    //PyObject * all_data_pyObj = PyArray_SimpleNewFromData(2, all_data_dims, NPY_INT, all_data); //this should be NPY_INT8.
    //boost::python::handle<> all_data_handle( all_data_pyObj );
    /*
    Py_intptr_t shape1[1] = { bigT * num_subparts };
    np::ndarray all_data_arr = np::zeros(1, shape1, np::dtype::get_builtin<double>());
    int oned_all_data[bigT * num_subparts];
    for(int i=0;i<num_subparts;i++){
        for(int j=0;j<bigT;j++){
            oned_all_data[i*bigT + j] = all_data[i][j];
        }
    }
    std::copy(&oned_all_data[0], &oned_all_data[num_subparts * bigT - 1], reinterpret_cast<double*>(all_data_arr.get_data()));
    
    */
    
    /*boost::python::list l_stateseqs;
    for(int i=0;i<bigT;i++){
        l_stateseqs.append(all_stateseqs[0][i]);
    }
    np::ndarray all_stateseqs_arr = np::array(l_stateseqs);
    
    boost::python::list l_data;
    for(int i=0;i<num_subparts;i++){
        for(int j=0;j<bigT;j++){
            l_data.append(all_data[i][j]);
        }
    }
    np::ndarray all_data_arr = np::array(l_data);
    */
    boost::python::tuple orig_shape_seq = boost::python::make_tuple(1, bigT);
    np::ndarray final_stateseqs_arr = np::zeros(orig_shape_seq, np::dtype::get_builtin<int>());
    for(int i=0;i<bigT;i++){
        final_stateseqs_arr[0][i] = all_stateseqs[0][i];
    }
    
    boost::python::tuple orig_shape_data = boost::python::make_tuple(num_subparts, bigT);
    np::ndarray final_data_arr = np::zeros(orig_shape_data, np::dtype::get_builtin<int>());
    for(int i=0;i<num_subparts;i++){
        for(int j=0;j<bigT;j++){
            final_data_arr[i][j] = all_data[i][j];
        }
    }
    result["stateseqs"] = final_stateseqs_arr;
    result["data"] = final_data_arr;
    return(result);
    
}

BOOST_PYTHON_MODULE(synthetic_data_helper){
    //import_array();
    init_numpy();
    /*if(PyArray_API == NULL)
	{
	    import_array();
	}*/
    //np::ndarray::set_module_and_type("numpy", "ndarray");
    //np::initialize();
    Py_Initialize();
    np::initialize();
    to_python_converter<double, double_to_python_float>();
    //enable_numpy_scalar_converter<boost::int8_t, NPY_INT8>();
   // enable_numpy_scalar_converter<boost::int16_t, NPY_INT16>();
    //enable_numpy_scalar_converter<boost::int32_t, NPY_INT32>();
   // enable_numpy_scalar_converter<boost::int64_t, NPY_INT64>();
    
    def("create_synthetic_data", create_synthetic_data);
    
}