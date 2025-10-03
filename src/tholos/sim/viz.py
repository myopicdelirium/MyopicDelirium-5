from PIL import Image, ImageDraw
def render_frame(G, water, veg, danger, agents, preds, houses, game_k=None, game=None, scale=2, side_panel=None):
    W=G["W"]; H=G["H"]
    img=Image.new("RGB",(W,H))
    px=img.load()
    for y in range(H):
        for x in range(W):
            px[x,y]=(danger[y][x],veg[y][x],water[y][x])
    d=ImageDraw.Draw(img)
    for p in preds:
        x=p["x"]; y=p["y"]
        d.rectangle((x-1,y-1,x+1,y+1),outline=(0,0,0),fill=(220,30,30))
    for a in agents:
        d.point((a["x"],a["y"]),fill=(255,255,255))
    if scale!=1:
        img=img.resize((W*scale,H*scale),Image.NEAREST)
    return img
def write_outputs(frames, final_frame, out_png, out_gif, viewer_html, open_view=False):
    final_frame.save(out_png)
    if frames:
        frames[0].save(out_gif,save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=2)
    else:
        final_frame.save(out_gif)
    html='<!DOCTYPE html><html><head><meta charset="utf-8"><title>viewer</title><style>body{background:#0b0b12;color:#e8e8f0;font-family:system-ui;padding:24px}main{max-width:920px;margin:0 auto}img{image-rendering:pixelated}a{color:#9cc3ff}</style></head><body><main><h1>viewer</h1><p><a href="composite.gif">GIF</a> • <a href="composite.png">PNG</a></p><img src="composite.gif"></main></body></html>'
    with open(viewer_html,"w",encoding="utf-8") as f:
        f.write(html)
