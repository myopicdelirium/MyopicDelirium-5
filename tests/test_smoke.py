import os, glob, subprocess, sys
def test_smoke():
    env=dict(os.environ); env.update({"PYTHONPATH":"src"})
    subprocess.check_call([sys.executable,"-m","tholos.cli.run_sim","--config","configs/base.yaml"],env=env)
    run=sorted(glob.glob("out/*"))[-1]
    assert os.path.isfile(os.path.join(run,"artifacts","composite.gif"))
