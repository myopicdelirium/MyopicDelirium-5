import argparse, os, yaml
from types import SimpleNamespace
from tholos.sim.engine import run_sim
def _ns(d):
    if isinstance(d, dict):
        return SimpleNamespace(**{k:_ns(v) for k,v in d.items()})
    if isinstance(d, list):
        return [_ns(v) for v in d]
    return d
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    args=ap.parse_args()
    with open(args.config,"r") as f:
        raw=yaml.safe_load(f)
    cfg=_ns(raw)
    cfg.seed_env=int(cfg.seed)+1
    cfg.seed_agents=int(cfg.seed)+2
    cfg.seed_preds=int(cfg.seed)+3
    out_dir=run_sim(cfg)
    eff=os.path.join(os.path.dirname(out_dir),"config_effective.yaml")
    with open(eff,"w") as f:
        yaml.safe_dump(raw,f,sort_keys=False)
    print(out_dir)
if __name__=="__main__":
    main()
