use crate::optimisers::{NelderMead, OptimisationResults, Optimiser};
use std::collections::HashMap;

pub type ObjectiveFn = Box<dyn Fn(&[f64]) -> f64 + Send + Sync>;

// Builder pattern for the optimisation problem
pub struct Builder {
    objective: Option<ObjectiveFn>,
    config: HashMap<String, f64>,
    parameter_names: Vec<String>,
    default_optimiser: Option<NelderMead>,
}
impl Builder {
    pub fn new() -> Self {
        Self {
            objective: None,
            config: HashMap::new(),
            parameter_names: Vec::new(),
            default_optimiser: None,
        }
    }

    pub fn with_objective<F>(mut self, f: F) -> Self
    where
        F: Fn(&[f64]) -> f64 + Send + Sync + 'static,
    {
        self.objective = Some(Box::new(f));
        self
    }

    pub fn with_config(mut self, key: String, value: f64) -> Self {
        self.config.insert(key, value);
        self
    }

    pub fn add_parameter(mut self, name: String) -> Self {
        self.parameter_names.push(name);
        self
    }

    pub fn set_optimiser(mut self, optimiser: NelderMead) -> Self {
        self.default_optimiser = Some(optimiser);
        self
    }

    pub fn build(self) -> Result<Problem, String> {
        match self.objective {
            Some(obj) => Ok(Problem {
                objective: obj,
                config: self.config,
                parameter_names: self.parameter_names,
                default_optimiser: self.default_optimiser,
            }),
            None => Err("At least one objective must be provide".to_string()),
        }
    }
}

impl Default for Builder {
    fn default() -> Self {
        Self::new()
    }
}

// Problem class
pub struct Problem {
    objective: ObjectiveFn,
    config: HashMap<String, f64>,
    parameter_names: Vec<String>,
    default_optimiser: Option<NelderMead>,
}

impl Problem {
    pub fn evaluate(&self, x: &[f64]) -> f64 {
        (self.objective)(x)
    }

    pub fn get_config(&self, key: &str) -> Option<&f64> {
        self.config.get(key)
    }

    pub fn config(&self) -> &HashMap<String, f64> {
        &self.config
    }

    pub fn dimension(&self) -> usize {
        if !self.parameter_names.is_empty() {
            return self.parameter_names.len();
        }
        0
    }

    pub fn optimize(
        &self,
        initial: Option<Vec<f64>>,
        optimiser: Option<&dyn Optimiser>,
    ) -> OptimisationResults {
        let x0 = match initial {
            Some(v) => v,
            None => vec![0.0; self.dimension()],
        };

        if let Some(opt) = optimiser {
            return opt.run(self, x0);
        }

        if let Some(default_nm) = &self.default_optimiser {
            return default_nm.run(self, x0);
        }

        // Default to NelderMead when nothing provided
        let nm = NelderMead::new();
        nm.run(self, x0)
    }
}
