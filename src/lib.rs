use pyo3::prelude::*;

pub mod optimisers;
pub mod problem;

// Python module definition
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<problem::Builder>()?;
    m.add_class::<problem::SimpleProblem>()?;
    m.add_class::<problem::BuilderFactory>()?;
    m.add_class::<problem::Problem>()?;
    m.add_class::<optimisers::NelderMead>()?;
    m.add_class::<optimisers::OptimisationResults>()?;
    Ok(())
}
