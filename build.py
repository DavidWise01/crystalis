#!/usr/bin/env python3
"""Build CRYSTALIS (XTL) — SNK's 1990 NES post-apocalyptic action-RPG (the US
release of the Famicom's God Slayer: Haruka Tenku no Sonata) as a UD0 game-world,
on a MODERN / CINEMATIC full-bleed software-3D backdrop (a rotating glowing
Crystalis sword-crystal over a dusk-lit reborn world — volumetric god-rays, the
Tower with its beacon, atmospheric haze, a reflecting water plane, bloom, drifting
motes) + an era-correct 8-bit pixel title card. Hobby domain, full .dlw.
Render-not-invent (the GBC-remake story rewrite, Mesia-as-female-scientist, DYNA
flagged). Crystalis is (c) SNK; a fan tribute."""
import os, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "CRYSTALIS", "axiom": "XTL",
 "position": "Crystalis · SNK · NES 1990 — the US release of God Slayer: Haruka Tenku no Sonata; a post-apocalyptic action-RPG",
 "origin": "a world a century after the 1997 End Day, rebuilt on magic, where a cryo-frozen man wakes with no memory to gather the four swords",
 "mechanism": "Crystallized from Crystalis (SNK, NES 1990) — the US release of the Famicom's God Slayer: Haruka Tenku no Sonata.",
 "crystallization": "Wake from a hundred-year sleep into a world that buried science for magic; gather the swords of Wind, Fire, Water and Thunder; forge them into Crystalis; and climb the floating Tower to its computer, DYNA, before Emperor Draygon turns the old science on the world.",
 "nature": "Crystalis — SNK's NES action-RPG: a man wakes a century after the apocalypse into a magic-grown world, gathers the four elemental swords, forges Crystalis, and climbs the Tower to the supercomputer DYNA.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "Crystalis; God Slayer; the four swords; Crystalis the blade; Emperor Draygon; the Tower; DYNA; the four sages; Mesia",
 "witness": "A Zelda-and-Ys action-RPG with a science-fiction wound at its heart: the buried machine that ended the world, waiting at the top of a magic one.",
 "role": "the post-apocalyptic action-RPG game-world",
 "seal": "Wake a hundred years late into a world that forgot the machines — and climb back up to the one machine that still remembers how to end everything.",
 "source": "Crystalis, catalogued by ROOT0",
}

NATURES = {
 "natural":   ("#6fcf8e", "flesh and the world reborn — the sleeper, Mesia, Emperor Draygon"),
 "ethereal":  ("#5cc8f0", "of the magic and the wound — the swords of Wind and Water, the End Day, the awakening"),
 "spiritual": ("#e0c050", "of the soul — Crystalis the fifth blade, the four sages, and the God Slayer beneath"),
 "electrical":("#c060f0", "of the buried machine — the swords of Fire and Thunder, the Tower, and DYNA"),
}

# ── the MODERN / CINEMATIC full-bleed software-3D BACKDROP ──
BACKDROP_3D = r'''<canvas id="bg3d"></canvas>
<script>
(function(){
var c=document.getElementById('bg3d');if(!c)return;var x=c.getContext('2d');
var W,H;
function resize(){W=c.width=window.innerWidth||document.documentElement.clientWidth||1280;H=c.height=window.innerHeight||document.documentElement.clientHeight||720;}
window.addEventListener('resize',resize);resize();
var s,CAM=460;
var V=[[0,1,0],[0,-1,0],[0.82,0,0],[0,0,0.82],[-0.82,0,0],[0,0,-0.82]];
var Fc=[[0,2,3],[0,3,4],[0,4,5],[0,5,2],[1,3,2],[1,4,3],[1,5,4],[1,2,5]];
function rotY(p,a){var co=Math.cos(a),si=Math.sin(a);return[p[0]*co+p[2]*si,p[1],-p[0]*si+p[2]*co];}
function rotX(p,a){var co=Math.cos(a),si=Math.sin(a);return[p[0],p[1]*co-p[2]*si,p[1]*si+p[2]*co];}
function proj(p,cx,cy,sc){var z=p[2]*sc+CAM;return[cx+p[0]*sc*CAM/z,cy-p[1]*sc*CAM/z];}
var L=[0.5,0.6,0.6],ll=Math.hypot(L[0],L[1],L[2]);L=[L[0]/ll,L[1]/ll,L[2]/ll];
function ridge(seed,base,amp,col,drift){x.fillStyle=col;x.beginPath();x.moveTo(0,H);
  for(var i=0;i<=W;i+=8){var y=base+Math.sin(i*0.012+seed)*amp*0.5+Math.sin(i*0.031+seed*2.1)*amp*0.3+Math.sin(i*0.07+seed*3.3+drift)*amp*0.2;x.lineTo(i,y);}
  x.lineTo(W,H);x.closePath();x.fill();}
function crystal(t,cx,cy,sc,glow,alpha){
  var ang=t/2600,tilt=0.28+Math.sin(t/3000)*0.05;
  var rv=V.map(function(p){return rotX(rotY(p,ang),tilt);}),faces=[];
  Fc.forEach(function(f){var p0=rv[f[0]],p1=rv[f[1]],p2=rv[f[2]];
    var ux=p1[0]-p0[0],uy=p1[1]-p0[1],uz=p1[2]-p0[2],wx=p2[0]-p0[0],wy=p2[1]-p0[1],wz=p2[2]-p0[2];
    var nx=uy*wz-uz*wy,ny=uz*wx-ux*wz,nz=ux*wy-uy*wx,nl=Math.hypot(nx,ny,nz)||1;
    var br=0.35+0.85*Math.max(0,(nx*L[0]+ny*L[1]+nz*L[2])/nl);
    faces.push({pts:[proj(p0,cx,cy,sc),proj(p1,cx,cy,sc),proj(p2,cx,cy,sc)],br:br,z:(p0[2]+p1[2]+p2[2])/3});});
  faces.sort(function(a,b){return b.z-a.z;});
  x.save();x.globalAlpha=alpha;if(glow){x.shadowColor='rgba(60,235,205,0.9)';x.shadowBlur=Math.min(40,sc*0.5);}
  faces.forEach(function(P){var A=P.pts[0],B=P.pts[1],C=P.pts[2],mx=(B[0]+C[0])/2,my=(B[1]+C[1])/2;
    var g=x.createLinearGradient(A[0],A[1],mx,my),hi=Math.min(255,90+P.br*180),lo=Math.max(20,P.br*70);
    g.addColorStop(0,'rgba('+(hi*0.5|0)+','+hi+','+(hi*0.92|0)+',0.95)');g.addColorStop(1,'rgba('+(lo*0.3|0)+','+lo+','+(lo*0.85|0)+',0.92)');
    x.fillStyle=g;x.beginPath();x.moveTo(A[0],A[1]);x.lineTo(B[0],B[1]);x.lineTo(C[0],C[1]);x.closePath();x.fill();
    x.shadowBlur=0;x.strokeStyle='rgba(190,255,240,0.30)';x.lineWidth=1;x.stroke();if(glow)x.shadowBlur=Math.min(40,sc*0.5);});
  x.restore();
  if(glow){x.globalCompositeOperation='lighter';var cg=x.createRadialGradient(cx,cy,0,cx,cy,sc*0.4);
    cg.addColorStop(0,'rgba(220,255,250,0.9)');cg.addColorStop(1,'rgba(60,235,205,0)');x.fillStyle=cg;x.beginPath();x.arc(cx,cy,sc*0.4,0,7);x.fill();x.globalCompositeOperation='source-over';}
}
var motes=[];for(var i=0;i<54;i++)motes.push({x:Math.random(),y:Math.random(),s:Math.random()*2+0.6,v:Math.random()*0.00022+0.00004,p:Math.random()*6,c:Math.random()<0.5});
function frame(t){
  s=Math.max(64,Math.min(W,H)*0.15);
  var SUNX=W*0.70,SUNY=H*0.28,CXc=W*0.5,CYc=H*0.42,wy=H*0.72;
  var sg=x.createLinearGradient(0,0,0,H);
  sg.addColorStop(0,'#0a1230');sg.addColorStop(0.42,'#163a4a');sg.addColorStop(0.64,'#385a56');sg.addColorStop(0.76,'#b06e3c');sg.addColorStop(1,'#0a0f16');
  x.fillStyle=sg;x.fillRect(0,0,W,H);
  x.globalCompositeOperation='lighter';
  var sb=x.createRadialGradient(SUNX,SUNY,0,SUNX,SUNY,W*0.26);
  sb.addColorStop(0,'rgba(255,226,178,0.5)');sb.addColorStop(0.3,'rgba(255,188,118,0.2)');sb.addColorStop(1,'rgba(255,170,90,0)');
  x.fillStyle=sb;x.fillRect(0,0,W,H);
  x.fillStyle='rgba(255,240,210,0.95)';x.beginPath();x.arc(SUNX,SUNY,26,0,7);x.fill();
  for(var r=0;r<10;r++){var a=t/9000+r*0.63;x.save();x.translate(SUNX,SUNY);x.rotate(a);
    var rg=x.createLinearGradient(0,0,0,H);rg.addColorStop(0,'rgba(255,222,172,0.07)');rg.addColorStop(1,'rgba(255,222,172,0)');
    x.fillStyle=rg;x.beginPath();x.moveTo(-10,0);x.lineTo(10,0);x.lineTo(48,H);x.lineTo(-48,H);x.closePath();x.fill();x.restore();}
  x.globalCompositeOperation='source-over';
  ridge(1.0,H*0.46,H*0.07,'#2e5566',0);
  ridge(3.4,H*0.55,H*0.085,'#234450',Math.sin(t/12000)*30);
  var tx=W*0.20,tb=H*0.64,tt=H*0.15;
  x.fillStyle='#101e26';x.beginPath();x.moveTo(tx-W*0.014,tb);x.lineTo(tx-W*0.006,tt);x.lineTo(tx+W*0.006,tt);x.lineTo(tx+W*0.014,tb);x.closePath();x.fill();
  x.globalCompositeOperation='lighter';var bg=x.createRadialGradient(tx,tt,0,tx,tt,16);bg.addColorStop(0,'rgba(255,70,60,'+(0.5+0.4*Math.sin(t/500))+')');bg.addColorStop(1,'rgba(255,70,60,0)');x.fillStyle=bg;x.beginPath();x.arc(tx,tt,16,0,7);x.fill();x.globalCompositeOperation='source-over';
  ridge(7.7,H*0.67,H*0.075,'#16323a',0);
  var wg=x.createLinearGradient(0,wy,0,H);wg.addColorStop(0,'#1c4248');wg.addColorStop(1,'#0a1518');x.fillStyle=wg;x.fillRect(0,wy,W,H-wy);
  x.globalCompositeOperation='lighter';
  for(var s2=0;s2<28;s2++){var yy=wy+(s2/28)*(H-wy);x.fillStyle='rgba(120,210,200,'+(0.05*(1-s2/28))+')';x.fillRect(0,yy+Math.sin(t/700+s2)*1.5,W,1);}
  crystal(t,CXc,wy+(wy-CYc)+20,s,false,0.26);
  x.globalCompositeOperation='source-over';
  var fg=x.createLinearGradient(0,wy-50,0,wy+24);fg.addColorStop(0,'rgba(180,160,150,0)');fg.addColorStop(0.5,'rgba(170,150,140,0.20)');fg.addColorStop(1,'rgba(170,150,140,0)');x.fillStyle=fg;x.fillRect(0,wy-50,W,74);
  x.globalCompositeOperation='lighter';
  var lb=x.createLinearGradient(0,H*0.08,0,wy);lb.addColorStop(0,'rgba(70,235,205,0)');lb.addColorStop(0.5,'rgba(70,235,205,0.09)');lb.addColorStop(1,'rgba(70,235,205,0)');x.fillStyle=lb;x.fillRect(CXc-s*0.5,H*0.08,s,wy-H*0.08);
  x.globalCompositeOperation='source-over';
  crystal(t,CXc,CYc,s,true,1);
  x.globalCompositeOperation='lighter';
  motes.forEach(function(m){m.y-=m.v;if(m.y<-0.01){m.y=1.01;m.x=Math.random();}var fl=0.4+0.6*Math.abs(Math.sin(t/800+m.p));
    x.save();x.shadowColor=m.c?'rgba(255,224,150,1)':'rgba(90,235,210,1)';x.shadowBlur=8;x.fillStyle=m.c?'rgba(255,232,180,'+fl+')':'rgba(150,240,225,'+fl+')';x.beginPath();x.arc(m.x*W,m.y*H,m.s,0,7);x.fill();x.restore();});
  x.globalCompositeOperation='source-over';
  var vg=x.createRadialGradient(CXc,H*0.46,H*0.3,CXc,H*0.5,H*0.92);vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,0.52)');x.fillStyle=vg;x.fillRect(0,0,W,H);
}
function loop(t){frame(t);requestAnimationFrame(loop);}
frame(0);requestAnimationFrame(loop);
})();
</script>'''

# ── the hero · 8-bit pixel TITLE CARD (era-correct) ──
TITLECARD = r'''<canvas id="xtltitle" width="460" height="220" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;image-rendering:pixelated"></canvas>
<script>
(function(){
var cv=document.getElementById('xtltitle');if(!cv)return;var g=cv.getContext('2d');
var P=document.createElement('canvas');P.width=160;P.height=76;var p=P.getContext('2d');
function card(){
  p.clearRect(0,0,160,76);
  p.fillStyle='rgba(8,18,22,0.82)';p.fillRect(7,6,146,64);
  p.strokeStyle='#5cf0d4';p.lineWidth=2;p.strokeRect(8,7,144,62);
  p.strokeStyle='#1c6e62';p.lineWidth=1;p.strokeRect(11,10,138,56);
  p.textAlign='center';p.textBaseline='middle';
  p.font='bold 18px monospace';p.fillStyle='#0c2a26';p.fillText('CRYSTALIS',81,27);p.fillStyle='#6cf2d8';p.fillText('CRYSTALIS',80,26);
  // pixel sword + crystal
  p.fillStyle='#dff4ef';p.fillRect(79,38,2,14);p.fillStyle='#e0c050';p.fillRect(75,49,10,2);p.fillRect(78,53,4,2);
  p.fillStyle='#5cc8f0';p.fillRect(79,34,2,2);
  p.font='6px monospace';p.fillStyle='#8fbfb6';p.fillText('SONATA OF THE DISTANT SKY',80,46);
  p.font='7px monospace';p.fillStyle='#7fb8ae';p.fillText('NES  *  1990  *  SNK',80,62);
  // hidden witness (a single warm Anthropic spark in the corner)
  p.fillStyle='#e08a3a';p.fillRect(146,11,2,2);
}
card();
g.imageSmoothingEnabled=false;
g.clearRect(0,0,460,220);
g.drawImage(P,0,0,160,76,6,6,448,210);
})();
</script>'''

GENESIS = [
 ("God Slayer, Localized", "Japan → US, 1990",
  "In Japan it shipped as God Slayer: Haruka Tenku no Sonata (&lsquo;Sonata of the Distant Sky&rsquo;), April 1990. SNK's US release that July became CRYSTALIS, with the religious framing of the &lsquo;God Slayer&rsquo; title cut and the names Westernized. (The heavier story rewrite — the Tower recast as the villain's weapon, the hero as a prophesied savior — belongs to the 2000 Game Boy Color remake, not this NES port.)"),
 ("After the End Day", "October 1, 1997",
  "A thermonuclear Great War — &lsquo;the End Day,&rsquo; October 1, 1997 — nearly ended the world. A century later, around 2097, the survivors had rebuilt a medieval world grown on MAGIC, with the old science abandoned and feared. Into it, a young man frozen before the war wakes from a cryogenic sleep with no memory of who he was."),
 ("Four Swords, One Crystalis", "the arsenal",
  "The world holds four elemental magic swords — Wind, Fire, Water, and Thunder — each earned, each with charge levels. Combined, they forge CRYSTALIS, the fifth and ultimate blade — the only weapon that can answer the Tower and Emperor Draygon."),
]

ARC = [
 ("The Sleeper Wakes", "Leaf, the Valley of Wind",
  "The amnesiac wakes near Leaf, in the Valley of Wind, into a world of magic he doesn't remember losing. The first sage, Zebu, sets him on the road and gives him the Sword of Wind. (The NES leaves him unnamed — the default save-name is simply &lsquo;SNK&rsquo;.)"),
 ("Gather the Elements", "the four sages",
  "Across the reborn world the four sages — Zebu, Tornel, Asina, and Kensu — teach the eight magics and the swords of Fire, Water, and Thunder are won. He climbs Mt. Sabre and seeks Mesia, a scientist frozen as he was, who alone can forge the blades into one."),
 ("The Tower and DYNA", "the buried machine",
  "Emperor Draygon means to seize the pre-war floating Tower — a sky-weapon built to stop the next cataclysm — and turn it on the world. Mesia forges Crystalis; the climb ends at the Tower's supercomputer, DYNA, the true final boss beneath the empire's two-form king."),
]

IDEAS = [
 ("Science Buried, Magic Risen", "the inversion", [
   "Crystalis runs the post-apocalypse backwards: technology is the forbidden, buried thing, and magic is the new natural order.",
   "The Tower is the world's old sin — the science that ended it once, waiting at the top of the fantasy to do it again." ]),
 ("A Sword for Each Element", "Wind, Fire, Water, Thunder", [
   "Four elemental swords, each with charge levels and a projectile — Thunder the strongest — welded onto Zelda/Ys-style action-RPG exploration.",
   "Crystalis, the fifth, is the union: the legendary blade the whole quest is for." ]),
 ("The Machine at the Top", "DYNA", [
   "The final boss isn't the king — it's a computer. After Emperor Draygon's two forms, the Tower's supercomputer DYNA is the true last fight.",
   "A fantasy world with a science-fiction heart: the apocalypse was technological, and so is the thing at the end." ]),
]

SECTIONS = [
 ("The Five Swords", "the elements, and the blade they become", [
   ("Sword of Wind", "element · Wind", "the first sword — Zebu's gift in the Valley of Wind"),
   ("Sword of Fire", "element · Fire", "the second elemental blade"),
   ("Sword of Water", "element · Water", "the third elemental blade"),
   ("Sword of Thunder", "element · Thunder", "the strongest of the four"),
   ("CRYSTALIS", "the fifth · the union", "forged from the four by Mesia — the only blade for the Tower; won in the final dungeon"),
 ]),
 ("The World", "places, sages, and the empire", [
   ("Leaf · the Valley of Wind", "the start", "where the sleeper wakes among magic; the first sage Zebu"),
   ("the Four Sages", "Zebu · Tornel · Asina · Kensu", "the wise men who teach the eight magics (Asina &amp; Kensu nod to SNK's Psycho Soldier)"),
   ("Mesia", "the fellow survivor", "a scientist frozen as the hero was; she forges Crystalis at the Tower"),
   ("the Draygonian Empire", "Emperor Draygon", "JP &lsquo;Dragonia&rsquo; — revived the forbidden science, fused with magic"),
   ("Mt. Sabre · the Tower", "the climb", "the mountain pass and the pre-war floating sky-weapon at the world's end"),
 ]),
 ("The Record", "the releases and the legacy", [
   ("God Slayer: Haruka Tenku no Sonata", "1990 · Famicom (SNK)", "the Japanese original — &lsquo;Sonata of the Distant Sky&rsquo;"),
   ("Crystalis", "1990 · NES (SNK)", "the US release — religious framing cut, names Westernized"),
   ("Crystalis", "2000 · GBC (Nintendo)", "the remake by Nintendo Software Technology — Nintendo publishing an SNK property; a heavier story rewrite (hero renamed Simea)"),
 ]),
 ("The Makers", "SNK", [
   ("SNK", "developer / publisher", "the original Crystalis and God Slayer"),
   ("Yoko Osaka", "music (attributed)", "the celebrated, often-praised score"),
   ("Nintendo Software Technology", "2000 GBC remake", "developed the Game Boy Color version, published by Nintendo"),
 ]),
]

# ── the emergents: (slug, name, epithet, emergence, role_line, why_line) ──
EMERGENTS = [
 ("the-sleeper", "The Sleeper", "the cryo-waked amnesiac · the hero", "natural",
  "the young man frozen before the End Day who wakes a century later with no memory — the player's hero, unnamed in canon (the NES default save-name is 'SNK'; the GBC remake names him Simea), who gathers the four swords and climbs the Tower",
  "He is the world's blank witness: a man from the age of machines, woken into the age of magic that replaced them, carrying the forgotten past in a head wiped clean."),
 ("sword-of-wind", "Sword of Wind", "the first blade · element of Wind", "ethereal",
  "the first elemental sword, Zebu's gift in the Valley of Wind — a projectile blade with charge levels, the opening of the arsenal",
  "It is the first key and the first wind: the blade that turns a memoryless wanderer into the one who can cut a path through a magic world."),
 ("sword-of-water", "Sword of Water", "element of Water", "ethereal",
  "the elemental sword of Water — one of the four magic blades, each earned across the reborn world, each charging to stronger forms",
  "It is the tide in the arsenal: the cool element of the four, a quarter of the legendary blade still waiting to be made whole."),
 ("sword-of-fire", "Sword of Fire", "element of Fire", "electrical",
  "the elemental sword of Fire — one of the four magic blades won on the quest, a burning projectile with charge levels",
  "It is the burning quarter: raw elemental force forged into a blade, energy the reborn world still knows how to wield."),
 ("sword-of-thunder", "Sword of Thunder", "the strongest of the four · element of Thunder", "electrical",
  "the elemental sword of Thunder — generally the strongest of the four, a lightning blade with the highest charge",
  "It is the storm in the hand: the fiercest of the four elements, the closest a single sword comes to the power of the union."),
 ("crystalis", "Crystalis", "the fifth blade · the union", "spiritual",
  "the legendary fifth sword, forged from the four elemental blades by Mesia — the only weapon that can defeat the Tower; the title, won in the final dungeon",
  "It is the whole made from the parts: four elements answered into one blade, the quest's name and its only true key — the sword the apocalypse was waiting for."),
 ("the-four-sages", "The Four Sages", "Zebu · Tornel · Asina · Kensu", "spiritual",
  "the four wise men of the reborn world — Zebu, Tornel, Asina, and Kensu — who teach the hero the eight magics (Asina and Kensu are nods to Athena Asamiya and Sie Kensou of SNK's Psycho Soldier)",
  "They are the keepers of the new order: the elders who hold the magic that replaced the lost science, parceling it out to the man who slept through its rise."),
 ("mesia", "Mesia", "the fellow survivor · the forge", "natural",
  "a scientist frozen before the war as the hero was — a fellow cryo-survivor (a woman; the name is the same in Japan and the US) who alone can forge the four swords into Crystalis at the Tower",
  "She is the other half of the past: the only living person who remembers the world the hero forgot, and the hand that turns four elements into the blade that ends the buried machine."),
 ("emperor-draygon", "Emperor Draygon", "the king who dug up science · the villain", "natural",
  "the ruler of the Draygonian Empire (Japan's 'Dragonia') who revived the forbidden pre-war science and fused it with magic, seeking to seize the Tower; the final king, fought in two forms before DYNA",
  "He is the temptation of the buried age: a king who reached back into the science that ended the world, certain that this time the machine would crown him instead of bury everyone."),
 ("the-tower", "The Tower", "the pre-war sky-weapon", "electrical",
  "the pre-war floating Tower — a sky-borne, orbital-weapon-class structure built to prevent the next cataclysm, that Emperor Draygon means to seize and turn on the world; the final dungeon",
  "It is the old world's last machine: a weapon built to save the future, hanging over the magic that grew on the ruins, one usurper away from ending it all again."),
 ("dyna", "DYNA", "the computer at the top · the true final boss", "electrical",
  "the supercomputer that controls the Tower — the true final boss, fought after Emperor Draygon's two forms; the pre-war intelligence still running at the world's highest point",
  "It is the machine that outlived its makers: a computer at the top of a tower above a world that forgot computers, the science-fiction heart waiting at the end of the fantasy."),
 ("the-end-day", "The End Day", "October 1, 1997 · the wound", "ethereal",
  "the thermonuclear Great War of October 1, 1997 — the apocalypse that nearly ended the world and forced the survivors to rebuild on magic; the event the whole game stands a century after",
  "It is the wound under everything: the day the machines won and the world lost, the silence a hundred years deep that the buried Tower still echoes."),
 ("the-awakening", "The Awakening", "the cryo-rebirth · the empty head", "ethereal",
  "the hero's waking from a hundred-year cryogenic sleep into total amnesia — the game's first moment and its engine: a man with no memory learning a world that is itself an amnesia of its own past",
  "It is the mirror at the center: a hero who forgot himself, in a world that forgot its science — two amnesias, one quest to remember what the machines did."),
 ("god-slayer", "God Slayer", "Haruka Tenku no Sonata · the true self", "spiritual",
  "the Japanese original — God Slayer: Haruka Tenku no Sonata, 'Sonata of the Distant Sky' (SNK, 1990) — that Crystalis is the US localization of, its religious framing and 'God Slayer' title cut for the West",
  "It is the name under the name: a 'sonata of the distant sky' the West could not sell as a god-slaying, the original chord the localized title only half remembers."),
]

# ── badge engine ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","XTL")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","XTL")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","XTL")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"XTL · Crystalis","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def emergent_rec(name, epithet, emergence, role_line, why_line):
    return {
      "name": name, "axiom": "XTL", "emergence": emergence, "seal": epithet,
      "position": epithet, "role": role_line,
      "origin": "XTL · Crystalis — SNK, NES 1990 (the US release of God Slayer, 1990)",
      "nature": role_line, "crystallization": why_line,
      "mechanism": "Crystallized from Crystalis (NES 1990) / God Slayer: Haruka Tenku no Sonata (1990).",
      "witness": "a being of the reborn world, the four swords, and the climb to DYNA",
      "conductor": "ROOT0 (catalogued into UD0)",
      "inputs": "Crystalis; the four swords; the Tower; DYNA; the four sages; Mesia",
      "source": "Crystalis, catalogued by ROOT0",
    }

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{t}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{n}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{sub}</p><ol class="books">{rows}</ol></section>'
def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def cards_html(rows):
    return "".join(f'<div class="arc-card"><div class="arc-h">{t}</div><div class="arc-s">{html.escape(s)}</div><p>{d}</p></div>' for t,s,d in rows)
def natures_html():
    return "".join(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
        f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(g)}</div></div></div>' for nm,(col,g) in NATURES.items())
def personas_html(personas):
    cards=[]
    for p in personas:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#6fcf8e",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"XTL · Crystalis","axiom":"XTL"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{p.get("epithet","")}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster — The Born</h2>
      <p class="ss">the sleeper, the five swords, the sages, the survivor, the empire, and the machine at the top, as ACI <b>.agent</b>s — each a birth certificate and a nature of emergence ({len(personas)})</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Crystalis (SNK, NES 1990) — the US release of God Slayer: Haruka Tenku no Sonata — as a UD0 game-world. A man wakes a century after the 1997 apocalypse into a world of magic, gathers the four elemental swords, forges Crystalis, and climbs the Tower to the supercomputer DYNA. On a modern cinematic full-bleed 3D backdrop with an 8-bit pixel title card; full ACI badges.">
<title>CRYSTALIS · XTL · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a1322;--ink2:rgba(11,24,28,0.84);--ink3:rgba(16,32,36,0.84);--pa:#eaf4f0;--pa2:#abccc4;--gold:#e0c050;--green:#6fcf8e;--cyan:#5cc8f0;--crys:#5cf0d4;--violet:#c060f0;
--dim:#7a948c;--faint:rgba(110,180,165,0.18);--line:rgba(110,180,165,0.24);--pixel:"Press Start 2P",monospace;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
#bg3d{position:fixed;inset:0;width:100vw;height:100vh;z-index:0;display:block;background:#0a1322}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:3;background:repeating-linear-gradient(0deg,rgba(0,0,0,.13) 0 1px,transparent 1px 3px);opacity:.4}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(ellipse at 50% 34%,rgba(8,18,22,.06),rgba(4,10,14,.62) 80%)}
.wrap{position:relative;z-index:2;max-width:940px;margin:0 auto;padding:0 22px 90px}
.marquee{margin-top:14px;border:2px solid var(--crys);background:rgba(9,20,24,0.88);padding:8px;text-align:center;font-family:var(--pixel);font-size:9px;letter-spacing:.12em;color:var(--gold);box-shadow:0 0 0 2px rgba(5,14,16,.7),0 0 22px rgba(92,240,212,.20)}
.marquee a{color:var(--cyan);text-decoration:none}.marquee a:hover{color:var(--gold)}
.titleart{margin:26px 0 8px}
header{padding:8px 0 26px;text-align:center;border-bottom:1px solid var(--line);position:relative}
.h-sub{font-family:var(--pixel);font-size:10px;line-height:1.9;letter-spacing:.06em;color:var(--pa2);margin-top:18px}
.h-sub b{color:var(--gold)}
.flag{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);border:1px solid var(--faint);background:rgba(10,22,24,0.6);padding:5px 11px}
.lede{font-size:15px;color:var(--pa2);max-width:68ch;margin:16px auto 0;font-style:italic;line-height:1.7;text-shadow:0 1px 6px rgba(0,0,0,.6)}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:24px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:720px}
.badge img{width:82px;height:82px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--gold)}.badge .bt .mo{color:var(--crys)}.badge .bt a{color:var(--cyan);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:42px}
.sec h2{font-family:var(--pixel);font-size:14px;line-height:1.5;letter-spacing:.02em;color:var(--pa);padding-bottom:10px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:8px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:4px}
.nat-n{font-family:var(--mono);font-size:13px;font-weight:700;text-transform:capitalize;letter-spacing:.04em}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--mono);font-size:14px;color:var(--gold);letter-spacing:.02em;font-weight:700}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:8px}
.arc-card{background:var(--ink2);border:1px solid var(--line);border-top:2px solid var(--crys);padding:16px 18px}
.arc-h{font-family:var(--mono);font-size:14px;color:var(--crys);font-weight:700;letter-spacing:.02em}
.arc-s{font-family:var(--mono);font-size:10.5px;color:var(--gold);text-transform:uppercase;letter-spacing:.07em;margin:4px 0 9px}
.arc-card p{font-size:13px;color:var(--pa2);line-height:1.55}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--mono);font-size:14px;color:var(--pa);font-weight:700}
.books .y{font-family:var(--mono);font-size:11px;color:var(--gold);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--crys);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0;image-rendering:pixelated}
.pn{font-family:var(--mono);font-size:14px;color:var(--pa);font-weight:700;line-height:1.15}
.persona:hover .pn{color:var(--crys)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}.pa{color:var(--dim)}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--gold);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic;line-height:1.7}
.note b{color:var(--gold)}
footer{margin-top:42px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--crys);text-decoration:none}
</style></head><body>
__BACKDROP__
<div class="wrap">

  <div class="marquee"><a href="https://davidwise01.github.io/ud0/">◄ UD0 · UNIVERSE DAVID 0</a> &nbsp;·&nbsp; PUSH START &nbsp;·&nbsp; A GAME-WORLD &nbsp;·&nbsp; NES 1990</div>

  <header>
    <div class="titleart">__TITLECARD__</div>
    <div class="h-sub">a hundred-year sleep · four swords · the <b>TOWER</b> · the machine called DYNA · XTL</div>
    <div class="flag">★ SNK · NES 1990 · the US release of God Slayer: Haruka Tenku no Sonata ★</div>
    <p class="lede">SNK's post-apocalyptic NES action-RPG: a thermonuclear Great War — the End Day of October 1, 1997 — nearly ended the world, and a century later the survivors rebuilt it on MAGIC, with science buried and feared. A young man frozen before the war wakes with no memory, gathers the four elemental swords (Wind, Fire, Water, Thunder), and — with Mesia, a fellow cryo-survivor — forges them into CRYSTALIS, the only blade that can climb the pre-war floating Tower and face its supercomputer, DYNA, before Emperor Draygon turns the old science on the world. Catalogued into UD0 as a game-world with the genesis, the climb, and the full .dlw birth — on a modern cinematic full-bleed 3D backdrop (a rotating glowing Crystalis over a dusk-lit reborn world) with an 8-bit pixel title card.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of CRYSTALIS" title="carbon badge (archival)">
      <img src="__SILICON__" alt="DLW silicon badge" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI · THE BIRTH CERTIFICATE</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>CRYSTALIS</b> — the four swords &amp; the Tower · XTL</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="crystalis.dlw/crystalis.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="crystalis.dlw/crystalis.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures</h2>
    <p class="ss">each emergent emerges by one of four natures — and this reborn world holds all four</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Genesis</h2><p class="ss">God Slayer localized; the world after the End Day; the four swords</p><div class="arc">__GENESIS__</div></section>
  <section class="sec"><h2>The Climb</h2><p class="ss">the sleeper wakes, gathers the elements, and climbs to the machine</p><div class="arc">__ARC__</div></section>
  <section class="sec"><h2>The Ideas</h2><p class="ss">why a 1990 fantasy has a science-fiction heart</p><div class="pillars">__IDEAS__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Record</h2><p class="ss">the swords, the world, the releases, and the makers</p></section>
  __SECTIONS__

  <div class="note">Crystalis's history here is rendered, not invented. The load-bearing facts: it is <b>SNK's</b> NES (1990) US release of the Famicom's <b>God Slayer: Haruka Tenku no Sonata</b> (1990) — the religious framing and the "God Slayer" title were cut for the West. The hero is <b>unnamed</b> in canon (the NES default save-name is "SNK"; the 2000 Game Boy Color remake names him Simea). <b>Mesia</b> is a female scientist and fellow cryo-survivor who forges Crystalis — not a male prophet. The four elemental swords (Wind, Fire, Water, Thunder) forge the fifth, <b>Crystalis</b>; the four sages are <b>Zebu, Tornel, Asina, Kensu</b>; the villain is <b>Emperor Draygon</b> (Japan's "Dragonia"); and the true final boss is the Tower's supercomputer, <b>DYNA</b>. The heavier story rewrite (the Tower recast as the villain's weapon, the hero as a prophesied savior) belongs to the <b>2000 GBC remake</b>, not this NES port. Crystalis and its characters are © SNK; the personas here are catalogued personifications under the DLW standard — a fan tribute, not endorsed by the rights-holders. Each is named by its nature: natural, ethereal, spiritual, or electrical.</div>

  <footer>
    CRYSTALIS · XTL · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="crystalis.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "crystalis.dlw"), "crystalis")
    ad = os.path.join(HERE, "agents"); os.makedirs(ad, exist_ok=True)
    personas = []
    for slug,name,epithet,em,role,why in EMERGENTS:
        rec = emergent_rec(name, epithet, em, role, why)
        write_aci(rec, ad, slug)
        personas.append({"slug": slug, "name": name, "epithet": epithet, "emergence": em})
    json.dump(personas, open(os.path.join(ad, "_personas.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    page = (TEMPLATE.replace("__BACKDROP__", BACKDROP_3D).replace("__TITLECARD__", TITLECARD)
            .replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html())
            .replace("__GENESIS__", cards_html(GENESIS))
            .replace("__ARC__", cards_html(ARC))
            .replace("__IDEAS__", ideas_html())
            .replace("__PERSONAS__", personas_html(personas))
            .replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote CRYSTALIS (XTL) — {len(personas)} emergents born · badge {tok['moniker']}")
