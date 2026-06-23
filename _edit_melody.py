# -*- coding: utf-8 -*-
import io, re, sys

path = "index.html"
with io.open(path, "r", encoding="utf-8") as f:
    html = f.read()

# ---------- 1) Remove the keyboard-mapping card (the one above the melody) ----------
mel_head = html.find('<div class="gk-head" style="background:#7FB23E;">')
assert mel_head != -1, "melody card head not found"
mel_card_start = html.rfind('<div class="gk-card">', 0, mel_head)
map_head = html.find('<div class="gk-head" style="background:#EF8A3C;">')
assert map_head != -1, "mapping card head not found"
map_card_start = html.rfind('<div class="gk-card">', 0, map_head)
assert map_card_start != -1 and map_card_start < mel_card_start, "card order unexpected"
html = html[:map_card_start] + html[mel_card_start:]

# ---------- 2) Replace melody note data ----------
NEW_DATA = """const L1=[
      [{k:'b/4',d:'q'},{k:'a/4',d:'q'},{k:'a/4',d:'q'},{k:'g/4',d:'q'}],
      [{k:'g/4',d:'8'},{k:'a/4',d:'8'},{k:'a/4',d:'8'},{k:'b/4',d:'8'},{k:'a/4',d:'8'},{k:'a/4',d:'8'},{k:'g/4',d:'8'},{k:'g/4',d:'8'}]
    ];
    const L2=[
      [{k:'b/4',d:'q'},{k:'a/4',d:'q'},{k:'a/4',d:'q'},{k:'g/4',d:'q'}],
      [{k:'g/4',d:'8'},{k:'a/4',d:'8'},{k:'a/4',d:'8'},{k:'b/4',d:'8'},{k:'a/4',d:'8'},{k:'a/4',d:'8'},{k:'g/4',d:'q'}],
      [{k:'b/4',d:'8'},{k:'c/5',d:'8'},{k:'b/4',d:'8'},{k:'a/4',d:'8'},{k:'g/4',d:'h'}]
    ];
    const systems="""
html, n = re.subn(r"const L1=\[.*?const systems=", NEW_DATA, html, count=1, flags=re.S)
assert n == 1, "L1/L2 data block not replaced"

# ---------- 3) Beam eighths in groups of <=4 ----------
NEW_BEAM = """const beams=[];let grp=[];
        const flushBeam=function(){for(var s=0;s<grp.length;s+=4){var sub=grp.slice(s,s+4);if(sub.length>1)beams.push(new VF.Beam(sub));}grp=[];};
        for(let i=0;i<specs.length;i++){
          const sp=specs[i],eighth=!sp.r&&sp.d.charAt(0)==='8';
          if(eighth){grp.push(notes[i]);}else{flushBeam();}
        }
        flushBeam();"""
html, n = re.subn(r"const beams=\[\];let grp=\[\];.*?if\(grp\.length>1\)beams\.push\(new VF\.Beam\(grp\)\);",
                  NEW_BEAM, html, count=1, flags=re.S)
assert n == 1, "beam block not replaced"

# ---------- 4) 4세 English texts ----------
def rep(a, b):
    global html
    assert a in html, "text not found: " + a
    html = html.replace(a, b, 1)

rep("🎹 G key 익히기 <small>솔(G)부터 시작하는 음계</small>",
    "🎵 Melody Practice <small>주 이름 찬양 · G key</small>")
rep("🎵 멜로디 연습 — 주 이름 찬양", "🎵 Melody — 주 이름 찬양")
rep("색깔 음표를 오른손으로 따라 쳐요 · So La Ti Do", "🤚🏻 Right Hand · So La Ti Do")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(html)
print("DONE")
