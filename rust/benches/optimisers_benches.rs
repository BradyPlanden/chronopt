use chronopt::prelude::*;
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use std::time::Duration;

fn quadratic_problem() -> Problem {
    ScalarProblemBuilder::new()
        .with_objective(|x: &[f64]| {
            let x0 = x[0] - 1.5;
            let x1 = x[1] + 0.5;
            x0 * x0 + x1 * x1
        })
        .build()
        .expect("failed to build quadratic problem")
}

fn quadratic_problem_with_gradient() -> Problem {
    ScalarProblemBuilder::new()
        .with_objective_and_gradient(
            |x: &[f64]| {
                let x0 = x[0] - 1.5;
                let x1 = x[1] + 0.5;
                x0 * x0 + x1 * x1
            },
            |x: &[f64]| vec![2.0 * (x[0] - 1.5), 2.0 * (x[1] + 0.5)],
        )
        .build()
        .expect("failed to build quadratic problem with gradient")
}

fn bench_nelder_mead_quadratic(c: &mut Criterion) {
    let problem = quadratic_problem();
    let optimiser = NelderMead::new()
        .with_max_iter(200)
        .with_threshold(1e-8)
        .with_sigma0(0.6)
        .with_position_tolerance(1e-6);
    let initial = vec![5.0_f64, -4.0_f64];

    c.bench_function("nelder_mead_quadratic", move |b| {
        let problem = &problem;
        let optimiser = optimiser.clone();
        let initial = initial.clone();
        b.iter(|| {
            let result = optimiser.run(problem, black_box(initial.clone()));
            black_box(result.fun);
        });
    });
}

fn bench_cmaes_quadratic(c: &mut Criterion) {
    let problem = quadratic_problem();
    let optimiser = CMAES::new()
        .with_max_iter(200)
        .with_threshold(1e-8)
        .with_sigma0(0.6)
        .with_seed(42);
    let initial = vec![5.0_f64, -4.0_f64];

    c.bench_function("cmaes_quadratic", move |b| {
        let problem = &problem;
        let optimiser = optimiser.clone();
        let initial = initial.clone();
        b.iter(|| {
            let result = optimiser.run(problem, black_box(initial.clone()));
            black_box(result.fun);
        });
    });
}

fn bench_adam_quadratic(c: &mut Criterion) {
    let problem = quadratic_problem_with_gradient();
    let optimiser = Adam::new()
        .with_step_size(0.1)
        .with_max_iter(200)
        .with_threshold(1e-8);
    let initial = vec![5.0_f64, -4.0_f64];

    c.bench_function("adam_quadratic", move |b| {
        let problem = &problem;
        let optimiser = optimiser.clone();
        let initial = initial.clone();
        b.iter(|| {
            let result = optimiser.run(problem, black_box(initial.clone()));
            black_box(result.fun);
        });
    });
}

fn optimiser_benches(c: &mut Criterion) {
    bench_nelder_mead_quadratic(c);
    bench_cmaes_quadratic(c);
    bench_adam_quadratic(c);
}

criterion_group!(name = optimisers; config = Criterion::default().measurement_time(Duration::from_secs(10)); targets = optimiser_benches);
criterion_main!(optimisers);
