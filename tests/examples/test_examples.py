import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"


def _run_example(relative_path: pathlib.Path | str, timeout: float = 120.0) -> None:
    script = EXAMPLES / relative_path
    result = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Example {relative_path} failed with code {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def _discover_example_scripts() -> list[pathlib.Path]:
    scripts: list[pathlib.Path] = []
    for path in EXAMPLES.rglob("*.py"):
        # Skip any helper or private modules if they are ever added
        if path.name.startswith("_"):
            continue
        scripts.append(path)
    scripts.sort()
    return [script.relative_to(EXAMPLES) for script in scripts]


EXAMPLE_SCRIPTS = _discover_example_scripts()


@pytest.mark.parametrize("relative_path", EXAMPLE_SCRIPTS, ids=lambda p: str(p))
def test_example_script(relative_path: pathlib.Path) -> None:
    # predator_prey examples require the optional diffrax dependency
    rel_str = str(relative_path)
    if "predator_prey" in rel_str:
        pytest.importorskip(
            "diffrax", reason="diffrax not installed for predator_prey examples"
        )

    timeout = 240.0 if "predator_prey" in rel_str else 120.0
    _run_example(relative_path, timeout=timeout)
