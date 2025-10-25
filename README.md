# chronopt

Chronopt is a time-series statistical inference package, it's goals are:
- Be fast, without sacrificing safety
- Be modular and informative

## Installation 
```bash
pip install chronopt
```

## Development Installation
Clone this repository, python installation via:
```bash
uv sync
```

Building the rust package w/ python bindings:
```bash
uv run maturin develop
```

## Tests
To run the python tests, use pytest:
```bash
uv run pytest
```

for the rust tests, use cargo:
```bash
cargo test
```