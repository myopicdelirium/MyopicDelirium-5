import os, time, math, random
from .viz import render_frame, write_outputs
def _clamp(v,a,b):
    return a if v<a else b if v>b else v
def _mk_env(cfg):
    W=cfg.env["grid"]; H=cfg.env["grid"]
    rng=random.Random(cfg.seed_env)
    veg=[[max(0,min(255,int(128+40*math.sin(x*0.08)+40*math.cos(y*0.07)+rng.uniform(-20,20)))) for x in range(W)] for y in range(H)]
    water=[[max(0,min(255,int(80+60*math.sin(x*0.05)+60*math.cos(y*0.05))))) for x in range(W)] for y in range(H)]
    danger=[[0]*W for _ in range(H)]
    for _ in range(W*H//45):
        cx=rng.randrange(W); cy=rng.randrange(H); r=rng.randint(6,14)
        for y in range(max(0,cy-r),min(H,cy+r+1)):
            for x in range(max(0,cx-r),min(W,cx+r+1)):
                if (x-cx)**2+(y-cy)**2<=r*r:
                    danger[y][x]=min(255,danger[y][x]+rng.randint(120,200))
    G={"W":W,"H":H}
    return G,water,veg,danger
def _mk_agents(cfg,G):
    rng=random.Random(cfg.seed_agents)
    return [{"x":rng.randrange(G["W"]),"y":rng.randrange(G["H"]),"e":200,"id":i} for i in range(cfg.agents)]
def _mk_preds(cfg,G):
    rng=random.Random(cfg.seed_preds)
    return [{"x":rng.randrange(G["W"]),"y":rng.randrange(G["H"]),"id":i} for i in range(cfg.predators)]
def _step(cfg,G,water,veg,danger,agents,preds):
    W=G["W"]; H=G["H"]
    new_agents=[]; grid=[[0]*W for _ in range(H)]
    for a in agents:
        grid[a["y"]][a["x"]]+=1
    for a in agents:
        bx=a["x"]; by=a["y"]; bs=-10**9
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                nx=_clamp(a["x"]+dx,0,W-1)
                ny=_clamp(a["y"]+dy,0,H-1)
                s=veg[ny][nx]-1.2*danger[ny][nx]-2*grid[ny][nx]
                if s>bs:
                    bs=s; bx=nx; by=ny
        a["x"]=bx; a["y"]=by
        a["e"]-=1
        gain=min(4,veg[a["y"]][a["x"]]//32)
        a["e"]+=gain
        veg[a["y"]][a["x"]]=max(0,veg[a["y"]][a["x"]]-2)
        if a["e"]>0:
            new_agents.append(a)
    agents=new_agents
    for p in preds:
        tgt=None; bd=10**9
        for a in agents:
            dx=a["x"]-p["x"]; dy=a["y"]-p["y"]; d=dx*dx+dy*dy
            if d<bd:
                bd=d; tgt=a
        if tgt:
            dx=tgt["x"]-p["x"]; dy=tgt["y"]-p["y"]
            if dx!=0: dx=1 if dx>0 else -1
            if dy!=0: dy=1 if dy>0 else -1
            p["x"]=_clamp(p["x"]+dx,0,W-1)
            p["y"]=_clamp(p["y"]+dy,0,H-1)
    alive=[]; pc={(p["x"],p["y"]) for p in preds}
    for a in agents:
        if (a["x"],a["y"]) not in pc:
            alive.append(a)
    for _ in range(300):
        ry=random.randrange(H); rx=random.randrange(W)
        veg[ry][rx]=min(255,veg[ry][rx]+1)
    return alive,preds
def run_sim(cfg):
    ts=time.strftime("%Y%m%d_%H%M%S")
    out_dir=os.path.join("out",f"{cfg.tag}_{ts}","artifacts")
    os.makedirs(out_dir,exist_ok=True)
    G,water,veg,danger=_mk_env(cfg)
    agents=_mk_agents(cfg,G)
    preds=_mk_preds(cfg,G)
    frames=[]
    for t in range(cfg.steps):
        agents,preds=_step(cfg,G,water,veg,danger,agents,preds)
        if t%cfg.render_every==0:
            frames.append(render_frame(G,water,veg,danger,agents,preds,[],None,None,cfg.env.get("img_scale",2),None))
    final=render_frame(G,water,veg,danger,agents,preds,[],None,None,cfg.env.get("img_scale",2),None)
    out_png=os.path.join(out_dir,"composite.png")
    out_gif=os.path.join(out_dir,"composite.gif")
    viewer=os.path.join(out_dir,"viewer.html")
    write_outputs(frames,final,out_png,out_gif,viewer,False)
    return out_dir
