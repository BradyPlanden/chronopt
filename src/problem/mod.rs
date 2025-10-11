use pyo3::prelude::*;
use std::collections::HashMap;

// Builder pattern for the optimisation problem
#[pyclass]
pub struct Builder {
    callables: Vec<PyObject>,
    config: HashMap<String, f64>,
}

#[pymethods]
impl Builder {
    fn add_callable(slf: Py<Self>, py: Python, obj: PyObject) -> PyResult<Py<Self>> {
        let mut builder = slf.borrow_mut(py);
        // callable verification
        if !obj.bind(py).is_callable() {
            return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "Object must be a callable",
            ));
        }
        builder.callables.push(obj);
        drop(builder);
        Ok(slf)
    }

    fn build(&self, py: Python) -> PyResult<Problem> {
        if self.callables.is_empty() {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                "At least one callable must be provided",
            ));
        }

        Ok(Problem {
            objective: self.callables[0].clone_ref(py), // clone zero index?
            config: self.config.clone(),
        })
    }
}

// Problem factory for creating builders
#[pyclass]
pub struct SimpleProblem;

#[pymethods]
impl SimpleProblem {
    fn __call__(&self) -> Builder {
        Builder {
            callables: Vec::new(),
            config: HashMap::new(),
        }
    }
}

// Main API Entry
#[pyclass]
pub struct BuilderFactory;

#[pymethods]
impl BuilderFactory {
    #[new]
    fn new() -> Self {
        Self
    }

    #[getter]
    fn SimpleProblem(&self) -> SimpleProblem {
        SimpleProblem
    }
}

// Problem class
#[pyclass]
pub struct Problem {
    objective: PyObject,
    config: HashMap<String, f64>,
}

#[pymethods]
impl Problem {
    pub fn evaluate(&self, py: Python, x: Vec<f64>) -> PyResult<f64> {
        let result = self.objective.call1(py, (x,))?;
        result.extract(py)
    }
}
