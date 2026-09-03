#!/usr/bin/env python3
import base64, io, os, re, sys, zlib


def seed(text):
    """Stable seed: builtin hash() is salted per process, so it would make the
    generated placeholder covers change on every run."""
    return zlib.crc32(text.encode()) % 9999
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets/img/nawaf-portrait.png")
# (template_path, output_path)
TARGETS = [(os.path.join(HERE, "artifact-ar.html"), os.path.join(HERE, "build/artifact-ar.build.html")),
           (os.path.join(HERE, "artifact-en.html"), os.path.join(HERE, "build/artifact-en.build.html"))]

def datauri_jpg(im, q=85):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def datauri_svg(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()

# ---- real photo ----
src = Image.open(SRC)
W,H = src.size

# about portrait: 4:5 crop, full height, centered horizontally
tw = int(H*0.8)
x0 = max(0,(W-tw)//2)
portrait = src.crop((x0,0,x0+tw,H)).resize((720, 900), Image.LANCZOS)
PORTRAIT = datauri_jpg(portrait, 86)

# avatar: square crop around face (upper-center)
sq = int(W*0.66)
ax = (W-sq)//2
ay = int(H*0.08)
avatar = src.crop((ax,ay,ax+sq,ay+sq)).resize((150,150), Image.LANCZOS)
AVATAR = datauri_jpg(avatar, 88)

# ---- placeholder mockups (abstract dashboards, no text) ----
def work_thumb(seed):
    # dark mini panel, blue accents
    import random; r=random.Random(seed)
    bars="".join(f'<rect x="{18+i*20}" y="{88-h}" width="12" height="{h}" rx="2" fill="#2E5CFF" opacity="{0.5+0.5*(i%2)}"/>'
                 for i,h in enumerate([r.randint(20,58) for _ in range(6)]))
    pts=" ".join(f"{150+i*15},{40+r.randint(-14,14)}" for i in range(8))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="152" viewBox="0 0 240 152">
<rect width="240" height="152" fill="#12161D"/>
<rect x="16" y="14" width="70" height="8" rx="4" fill="#2A313C"/>
<rect x="150" y="14" width="74" height="8" rx="4" fill="#2A313C"/>
{bars}
<polyline points="{pts}" fill="none" stroke="#7B9BFF" stroke-width="2.2"/>
{"".join(f'<circle cx="{150+i*15}" cy="{40+r.randint(-14,14)}" r="2.4" fill="#7B9BFF"/>' for i in range(0))}
<rect x="150" y="96" width="74" height="40" rx="6" fill="#1B212B"/>
</svg>'''
    return datauri_svg(svg)

def prod_shot(seed, accent="#C67E24"):
    import random; r=random.Random(seed)
    kpis="".join(f'<rect x="{20+i*88}" y="46" width="76" height="42" rx="7" fill="#F4F1EA" stroke="#EADCC2"/>'
                 f'<rect x="30+{i*88}" y="56" width="34" height="7" rx="3" fill="{accent}" opacity="0.8"/>'
                 f'<rect x="30" y="0" width="0" height="0"/>' for i in range(3))
    bars="".join(f'<rect x="{28+i*30}" y="{176-h}" width="18" height="{h}" rx="3" fill="{accent}" opacity="{0.55+0.15*(i%3)}"/>'
                 for i,h in enumerate([r.randint(28,74) for _ in range(7)]))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="200" viewBox="0 0 320 200">
<rect width="320" height="200" fill="#FFFFFF"/>
<rect x="0" y="0" width="320" height="30" fill="#F7F0E3"/>
<circle cx="20" cy="15" r="5" fill="{accent}"/>
<rect x="34" y="11" width="90" height="8" rx="4" fill="#E3D6BE"/>
<rect x="20" y="46" width="76" height="42" rx="7" fill="#FAF6EE" stroke="#EADCC2"/>
<rect x="108" y="46" width="76" height="42" rx="7" fill="#FAF6EE" stroke="#EADCC2"/>
<rect x="196" y="46" width="104" height="42" rx="7" fill="#FAF6EE" stroke="#EADCC2"/>
<rect x="30" y="56" width="40" height="8" rx="4" fill="{accent}"/>
<rect x="118" y="56" width="40" height="8" rx="4" fill="#2E5CFF"/>
<rect x="206" y="56" width="60" height="8" rx="4" fill="#14171C"/>
{bars}
<line x1="20" y1="176" x2="300" y2="176" stroke="#EADCC2" stroke-width="1.5"/>
</svg>'''
    return datauri_svg(svg)

_cache={}
def real(rel, maxw=1100, q=76):
    key=(rel,maxw,q)
    if key in _cache: return _cache[key]
    im=Image.open(os.path.join(HERE, "assets/work", rel))
    if im.width>maxw:
        im=im.resize((maxw,int(im.height*maxw/im.width)), Image.LANCZOS)
    u=datauri_jpg(im, q); _cache[key]=u; return u

def cat_thumb(accent, dark=False):
    import random; r=random.Random(seed(accent))
    bg="#12161D" if dark else "#FFFFFF"
    grid="#2A313C" if dark else "#EDEEEA"
    bars="".join(f'<rect x="{16+i*24}" y="{104-h}" width="14" height="{h}" rx="2" fill="{accent}" opacity="{0.55+0.15*(i%3)}"/>'
                 for i,h in enumerate([r.randint(24,64) for _ in range(6)]))
    return datauri_svg(f'''<svg xmlns="http://www.w3.org/2000/svg" width="184" height="120" viewBox="0 0 184 120">
<rect width="184" height="120" fill="{bg}"/><rect x="14" y="14" width="60" height="8" rx="4" fill="{grid}"/>
<rect x="120" y="14" width="50" height="8" rx="4" fill="{grid}"/>{bars}
<line x1="14" y1="104" x2="170" y2="104" stroke="{grid}" stroke-width="1.4"/></svg>''')

# work screenshots live in assets/work/ (already downscaled to the pipeline width)
Dash="dash_sales.png"; Iqama="dash_iqama.png"; Q4="dash_q4.png"
Sys1="sys_panel.png"; Sys2="sys_perf.png"
INCPH=prod_shot(15,"#2E5CFF")

def local(path, maxw=1400, q=78):
    key=(path,maxw,q)
    if key in _cache: return _cache[key]
    im=Image.open(path)
    if im.width>maxw:
        im=im.resize((maxw,int(im.height*maxw/im.width)), Image.LANCZOS)
    u=datauri_jpg(im, q); _cache[key]=u; return u

SY=os.path.join(HERE, "assets/siyanah")+"/"
import os
def sy(name, **kw):
    p=SY+name
    return local(p, **kw) if os.path.exists(p) else prod_shot(60,"#2E6327")

def ph_cover(kind):
    """Illustrative 16:10 cover for works that have no screenshot yet."""
    C={'dash':('#2E5CFF','#EEF2FF'),'sys':('#1F2937','#EDEFF3'),'rep':('#4B5563','#EFF0F2'),
       'study':('#C67E24','#FAF3E8'),'auto':('#4B63D6','#EDF0FF')}
    acc,bg=C.get(kind,C['dash'])
    import random; r=random.Random(seed(kind))
    body=''
    if kind=='dash':
        body=''.join('<rect x="%d" y="120" width="88" height="56" rx="9" fill="#fff" stroke="#E3E6EC"/>'%(70+i*104) for i in range(4))
        body+=''.join('<rect x="%d" y="136" width="44" height="9" rx="4" fill="%s" opacity=".85"/>'%(84+i*104,acc) for i in range(4))
        bars=''.join('<rect x="%d" y="%d" width="24" height="%d" rx="4" fill="%s" opacity="%.2f"/>'%(84+i*40,330-hh,hh,acc,0.45+0.12*(i%4))
                     for i,hh in enumerate([r.randint(50,140) for _ in range(7)]))
        body+='<rect x="60" y="200" width="330" height="160" rx="12" fill="#fff" stroke="#E3E6EC"/>'+bars
        pts=' '.join('%d,%d'%(440+i*46,300-r.randint(20,110)) for i in range(7))
        body+='<rect x="420" y="200" width="320" height="160" rx="12" fill="#fff" stroke="#E3E6EC"/><polyline points="%s" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'%(pts,acc)
    elif kind=='sys':
        body='<rect x="60" y="110" width="180" height="250" rx="12" fill="#fff" stroke="#E3E6EC"/>'
        body+=''.join('<rect x="80" y="%d" width="%d" height="12" rx="6" fill="%s" opacity="%.2f"/>'%(136+i*40,140 if i else 110,acc,.85 if i==1 else .22) for i in range(5))
        body+='<rect x="260" y="110" width="480" height="250" rx="12" fill="#fff" stroke="#E3E6EC"/>'
        body+=''.join('<rect x="284" y="%d" width="432" height="30" rx="7" fill="%s"/><rect x="300" y="%d" width="%d" height="10" rx="5" fill="%s" opacity=".5"/><rect x="640" y="%d" width="60" height="10" rx="5" fill="%s" opacity=".28"/>'%(140+i*46,bg,150+i*46,120+r.randint(0,120),acc,150+i*46,acc) for i in range(4))
    elif kind=='rep':
        body='<rect x="180" y="70" width="440" height="320" rx="10" fill="#fff" stroke="#E3E6EC"/>'
        body+='<rect x="214" y="104" width="200" height="16" rx="8" fill="%s"/>'%acc
        body+='<rect x="214" y="132" width="330" height="9" rx="4" fill="%s" opacity=".28"/>'%acc
        body+=''.join('<rect x="214" y="%d" width="%d" height="9" rx="4" fill="#D7DAE0"/>'%(176+i*26,372-r.randint(0,150)) for i in range(5))
        body+='<rect x="214" y="316" width="140" height="42" rx="8" fill="%s" opacity=".16"/><rect x="236" y="331" width="96" height="12" rx="6" fill="%s"/>'%(acc,acc)
    elif kind=='study':
        body='<rect x="60" y="110" width="330" height="250" rx="12" fill="#fff" stroke="#EADCC2"/>'
        body+=''.join('<rect x="88" y="%d" width="%d" height="11" rx="5" fill="%s" opacity="%.2f"/>'%(146+i*44,270-r.randint(0,110),acc,.7 if i==0 else .25) for i in range(4))
        body+='<rect x="410" y="110" width="330" height="250" rx="12" fill="#fff" stroke="#EADCC2"/>'
        body+=''.join('<rect x="%d" y="%d" width="34" height="%d" rx="5" fill="%s" opacity="%.2f"/>'%(440+i*54,330-hh,hh,acc,0.4+0.15*(i%4))
                      for i,hh in enumerate([r.randint(60,150) for _ in range(5)]))
    else:
        for i in range(3):
            body+='<rect x="%d" y="150" width="170" height="110" rx="14" fill="#fff" stroke="#E3E6EC"/>'%(80+i*230)
            body+='<circle cx="%d" cy="195" r="20" fill="%s" opacity=".16"/><circle cx="%d" cy="195" r="7" fill="%s"/>'%(165+i*230,acc,165+i*230,acc)
            body+='<rect x="%d" y="228" width="110" height="9" rx="4" fill="%s" opacity=".25"/>'%(110+i*230,acc)
            if i<2: body+='<path d="M%d 205 H%d" stroke="%s" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round"/>'%(258+i*230,300+i*230,acc)
    svg=('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">'
         '<rect width="800" height="500" fill="%s"/>'
         '<rect x="40" y="40" width="720" height="420" rx="18" fill="#F7F8F9" stroke="#E3E6EC"/>'
         '<rect x="40" y="40" width="720" height="46" rx="18" fill="#fff"/><rect x="40" y="74" width="720" height="12" fill="#fff"/>'
         '<circle cx="72" cy="63" r="5" fill="%s"/><rect x="90" y="58" width="120" height="10" rx="5" fill="#E3E6EC"/>'
         '%s</svg>')%(bg,acc,body)
    return datauri_svg(svg)


tokens = {
    "__AVATAR__": AVATAR, "__PORTRAIT__": PORTRAIT,
    "__PH_DASH__": ph_cover("dash"), "__PH_SYS__": ph_cover("sys"), "__PH_REP__": ph_cover("rep"),
    "__PH_STUDY__": ph_cover("study"), "__PH_AUTO__": ph_cover("auto"),
    # elevator maintenance system (p7) — curated shots from the handoff folder
    "__WORK_P7__": sy("u1.png"),
    "__G_P7_1__": sy("u1.png"), "__G_P7_2__": sy("u2.png"), "__G_P7_3__": sy("u3.png"),
    "__G_P7_4__": sy("u4.png"), "__G_P7_5__": sy("u5.png"), "__G_P7_6__": sy("u6.png"),
    # work card thumbnails
    "__WORK_P1__": real(Dash), "__WORK_P2__": real(Iqama), "__WORK_P3__": real(Sys1),
    "__WORK_P4__": real("study_1.png"), "__WORK_P5__": ph_cover("rep"), "__WORK_P6__": real("store_3.png"),
    # product card shots
    "__SHOT_FREE__": real("calc_1.png"), "__SHOT_STORE__": real("store_1.png"),
    "__SHOT_RIBHI__": real("ribhi_1.png"), "__SHOT_MOSADED__": real("mosaded_1.png"), "__SHOT_INCOME__": INCPH,
    # work galleries
    "__G_P1_1__": real(Dash), "__G_P1_2__": real(Q4),
    "__G_P2_1__": real(Iqama),
    "__G_P3_1__": real(Sys1), "__G_P3_2__": real(Sys2),
    "__G_P4_1__": real("study_1.png"), "__G_P4_2__": real("study_2.png"), "__G_P4_3__": real("study_3.png"),
    "__G_P5_1__": ph_cover("rep"),
    "__G_P6_1__": real("store_2.png"), "__G_P6_2__": real("store_3.png"),
    # product galleries
    "__PG_FREE_1__": real("calc_1.png"), "__PG_FREE_2__": real("calc_2.png"),
    "__PG_STORE_1__": real("store_1.png"), "__PG_STORE_2__": real("store_2.png"), "__PG_STORE_3__": real("store_3.png"),
    "__PG_RIBHI_1__": real("ribhi_1.png"), "__PG_RIBHI_2__": real("ribhi_2.png"), "__PG_RIBHI_3__": real("ribhi_3.png"),
    "__PG_MOS_1__": real("mosaded_1.png"), "__PG_MOS_2__": real("mosaded_2.png"), "__PG_MOS_3__": real("mosaded_3.png"),
    "__PG_INC_1__": INCPH,
    # archive category thumbnails
    "__CAT_DASH__": cat_thumb("#2E5CFF"), "__CAT_SYS__": cat_thumb("#7B9BFF",dark=True),
    "__CAT_REP__": cat_thumb("#5A6472"), "__CAT_STUDY__": cat_thumb("#C67E24"), "__CAT_AUTO__": cat_thumb("#4B63D6"),
}

for tpl,out in TARGETS:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(tpl,"r",encoding="utf-8") as f: html=f.read()
    for k,v in tokens.items():
        html=html.replace(k,v)
    with open(out,"w",encoding="utf-8") as f: f.write(html)
    left=[k for k in tokens if k in html]
    print(out, "remaining tokens:", left, "size:", len(html))
print("avatar b64 len:", len(AVATAR), "portrait b64 len:", len(PORTRAIT))
