"""Independent FontTools and HarfBuzz checks of browser-produced files."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
import json,sys
try: import uharfbuzz as hb
except ImportError: sys.path.insert(0,'/tmp/formaco-python');import uharfbuzz as hb
ROOT=Path(__file__).resolve().parents[1]
ACC='ÁÀÂÃÉÊÍÓÔÕÚÜÇáàâãéêíóôõúüç'
REQUIRED=set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'+ACC+' \u00a0.,:;!?\'"‘’“”«»()[]{}-–—…/\\@#&%+−=*_$€£ºª\u0301\u0300\u0302\u0303\u0308\u0327')
results=[]
def record(name,ok,detail=''):
 results.append({'check':name,'passed':bool(ok),'detail':detail});print(('PASS ' if ok else 'FAIL ')+name+' '+detail,flush=True)
for path in sorted((ROOT/'examples').glob('*.otf')):
 font=TTFont(path,checkChecksums=2);cmap=font.getBestCmap();names=font['name'];gs=font.getGlyphSet();stem=path.stem
 record(stem+' Unicode coverage',REQUIRED <= set(map(chr,cmap)))
 record(stem+' valid tables',all(t in font for t in ['CFF ','cmap','hmtx','name','OS/2','GPOS','GSUB','GDEF']))
 expected=300 if 'light' in stem else 600 if 'semibold' in stem else 700 if 'bold' in stem else 500 if 'medium' in stem else 400
 record(stem+' weight class',font['OS/2'].usWeightClass==expected,str(font['OS/2'].usWeightClass))
 record(stem+' italic classification',bool(font['head'].macStyle&2)==('-italic' in stem) and bool(font['OS/2'].fsSelection&1)==('-italic' in stem))
 record(stem+' licence metadata', 'MIT' in (names.getDebugName(13) or ''))
 record(stem+' family grouping',names.getDebugName(16)=='Formaço Study' and names.getDebugName(17) is not None)
 record(stem+' PostScript-safe name',all(ord(c)<127 and c not in ' [](){}<>/%' for c in names.getDebugName(6)))
 for ch in ['O','o','B','Á','ç']:
  pen=RecordingPen();gs[cmap[ord(ch)]].draw(pen)
  if ch=='ç':
   bounds=BoundsPen(gs);gs[cmap[ord(ch)]].draw(bounds);record(stem+' cedilla outline below baseline',bounds.bounds is not None and bounds.bounds[1]< -100)
  else:record(stem+' '+ch+' real contours',sum(op=='moveTo' for op,_ in pen.value)>1)
 pen=RecordingPen();gs[cmap[ord('O')]].draw(pen)
 record(stem+' designed bearings',font['hmtx'].metrics[cmap[ord('H')]][1]==(52 if '-italic' in stem else 55))
 # Flatten via fontTools for independent winding/counter validation.
 from fontTools.pens.basePen import BasePen
 class SamplePen(BasePen):
  def __init__(self,gs):super().__init__(gs);self.paths=[];self.points=[]
  def _moveTo(self,p):self.points=[p]
  def _lineTo(self,p):self.points.append(p)
  def _curveToOne(self,b,c,d):
   a=self._getCurrentPoint()
   for i in range(1,25):
    t=i/24;u=1-t;self.points.append(tuple(u**3*a[k]+3*u*u*t*b[k]+3*u*t*t*c[k]+t**3*d[k] for k in [0,1]))
  def _closePath(self):self.paths.append(self.points+[self.points[0]])
 sample=SamplePen(gs);gs[cmap[ord('O')]].draw(sample)
 areas=[sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]))/2 for p in sample.paths]
 record(stem+' O preserved counter winding',len(areas)==2 and areas[0]*areas[1]<0)
 mark=next(l for l in font['GPOS'].table.LookupList.Lookup if l.LookupType==4).SubTable[0]
 record(stem+' all marks covered',all(cmap[ord(c)] in mark.MarkCoverage.glyphs for c in '\u0301\u0300\u0302\u0303\u0308\u0327'))
 record(stem+' base anchors covered',all(cmap[ord(c)] in mark.BaseCoverage.glyphs for c in 'ACEIOUaceiou'))
 raw=path.read_bytes();import struct
 padded=raw+b'\0'*((-len(raw))%4);record(stem+' whole SFNT checksum',sum(struct.unpack('>'+str(len(padded)//4)+'I',padded))&0xffffffff==0xb1b0afba)
 face=hb.Face(raw);hfont=hb.Font(face);hfont.scale=(1000,1000)
 def shape(text,features=None):
  b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(hfont,b,features or {});return [(i.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
 pairs=shape('AV');normal=shape('AV',{'kern':False})
 record(stem+' shaping pair kerning',sum(g[1] for g in pairs)==sum(g[1] for g in normal)-60)
 import unicodedata
 record(stem+' NFC / NFD Portuguese shaping',all(shape(ch)==shape(unicodedata.normalize('NFD',ch)) for ch in ACC))
 # H + acute is not precomposable: this explicitly exercises GPOS instead of NFC.
 hmark=shape('H\u0301',{'ccmp':False});hmarkOff=shape('H\u0301',{'ccmp':False,'mark':False})
 record(stem+' actual GPOS mark placement',len(hmark)==2 and hmark[-1][1]==0 and hmark[-1][4]>600 and hmark[-1]!=hmarkOff[-1],str(hmark))
 # Decompile, checksum and round trip the WOFF independently.
 woffpath=path.with_suffix('.woff');wf=TTFont(woffpath,checkChecksums=2)
 wraw=woffpath.read_bytes();n=struct.unpack_from('>H',wraw,12)[0];wchecks={wraw[44+i*20:48+i*20].decode():struct.unpack_from('>I',wraw,60+i*20)[0] for i in range(n)};n=struct.unpack_from('>H',raw,4)[0];ochecks={raw[12+i*16:16+i*16].decode():struct.unpack_from('>I',raw,16+i*16)[0] for i in range(n)}
 record(stem+' WOFF original table checksums',wchecks==ochecks)
 record(stem+' WOFF equivalent maps/metrics',wf.flavor=='woff' and wf.getBestCmap()==cmap and wf['hmtx'].metrics==font['hmtx'].metrics)
 font.close();wf.close()
(ROOT/'tests'/'font-results.json').write_text(json.dumps(results,indent=2))
if any(not r['passed'] for r in results):raise SystemExit(1)
