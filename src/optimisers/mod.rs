use pyo3::prelude::*;

use crate::problem::Problem;

// Initial optimiser
#[pyclass]
pub struct NelderMead {
    problem: Py<Problem>,
    max_iter: usize,
    threshold: f64,
}

#[pymethods]
impl NelderMead {
    #[new]
    fn new(problem: Py<Problem>) -> Self {
        Self {
            problem,
            max_iter: 1000,
            threshold: 1e-6,
        }
    }

    fn run(&self, py: Python) -> PyResult<OptimisationResults> {
        let problem = self.problem.borrow(py);

        // Simplified Nelder-Mead for testing
        let mut x = vec![0.0, 0.0];
        let mut best_val = problem.evaluate(py, x.clone())?;
        let mut iterations = 0;

        for i in 0..self.max_iter {
            iterations += 1;

            // Simplified step
            let perturbation = 0.1 / (i as f64 + 1.0);
            let mut improved = false;

            for j in 0..x.len() {
                let mut x_new = x.clone();
                x_new[j] += perturbation;

                let val = problem.evaluate(py, x_new.clone())?;
                if val < best_val {
                    x = x_new;
                    best_val = val;
                    improved = true;
                }
            }

            if !improved && perturbation < self.threshold {
                break;
            }
        }
        Ok(OptimisationResults {
            x,
            fun: best_val,
            nit: iterations,
            success: true,
        })
    }
}

// Results object
#[pyclass]
pub struct OptimisationResults {
    #[pyo3(get)]
    x: Vec<f64>,
    #[pyo3(get)]
    fun: f64,
    #[pyo3(get)]
    nit: usize,
    #[pyo3(get)]
    success: bool,
}

#[pymethods]
impl OptimisationResults {
    fn __repr__(&self) -> String {
        format!(
            "OptimizationResults(x={:?}, fun={:.6}, nit={}, success={}))",
            self.x, self.fun, self.nit, self.success
        )
    }
}
