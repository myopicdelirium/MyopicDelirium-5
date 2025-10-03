#!/usr/bin/env bash
set -euo pipefail
python -m pip install -U pip >/dev/null
pip install -r requirements.txt >/dev/null
PYTHONPATH=src python -m tholos.cli.run_sim --config configs/base.yaml
RUN=$(ls -t out | head -n1)
test -s "out/$RUN/artifacts/composite.png"
test -s "out/$RUN/artifacts/composite.gif"
test -s "out/$RUN/artifacts/viewer.html"
echo "OK: out/$RUN/artifacts"
