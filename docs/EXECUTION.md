# Execution

## Local
PYTHONPATH=src python -m tholos.cli.run_sim --config configs/base.yaml
open out/$(ls -t out | head -n1)/artifacts/composite.gif

## Verify
bash scripts/verify.sh

## Tests
pytest -q
