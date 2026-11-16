"""Packs the osm-data branch layers (see build.py) into the compact JS block embedded in index.html.
Usage: python3 pack.py <osm-data dir> <out.js>
Lines: simplified (Douglas-Peucker), joined end-to-end per class, sorted on a 0.5 deg grid, then one stream of
zigzag-varint deltas (1e-5 deg) that continues from line to line; gzipped, base64. Decoded in the page with DecompressionStream."""
import json, gzip, math, sys, base64, collections
D, OUT = sys.argv[1].rstrip('/')+'/', sys.argv[2]
src = open(__file__.replace('pack.py','build.py')).read(); ns = {'math': math}; exec(src[src.index('def dp'):src.index('RCLS =')], ns); dp = ns['dp']

def dec(a):
    x = y = 0; o = []
    for i in range(0, len(a), 2): x += a[i]; y += a[i+1]; o.append((x, y))
    return o
def km(p):
    return sum(math.hypot((b[0]-a[0])*math.cos(math.radians(a[1]/1e5)), b[1]-a[1])*1.1132e-3 for a, b in zip(p, p[1:]))
def simp(p, tol):  # p in 1e-5 ints
    return [(round(x*1e5), round(y*1e5)) for x, y in dp([(x/1e5, y/1e5) for x, y in p], tol)] if len(p) > 2 else p
def join(lines):
    ends = collections.defaultdict(list); alive = [True]*len(lines); L = [list(l) for l in lines]
    for i, l in enumerate(L): ends[l[0]].append(i); ends[l[-1]].append(i)
    out = []
    for i in range(len(L)):
        if not alive[i]: continue
        alive[i] = False; cur = L[i]
        for side in (1, 0):
            while True:
                e = cur[-1] if side else cur[0]; nxt = next((j for j in ends[e] if alive[j]), None)
                if nxt is None: break
                alive[nxt] = False; n = L[nxt]
                if side: cur = cur + (n[1:] if n[0] == e else n[::-1][1:])
                else: cur = (n[:-1] if n[-1] == e else n[::-1][:-1]) + cur
        out.append(cur)
    return out
def varint(n, b):
    while True:
        c = n & 0x7f; n >>= 7
        if n: b.append(c | 0x80)
        else: b.append(c); return
def pack(lines):
    lines.sort(key=lambda l: (int(l[0][1]/5e4), int(l[0][0]/5e4) if int(l[0][1]/5e4) % 2 == 0 else -int(l[0][0]/5e4)))
    b = bytearray(); varint(len(lines), b); px = py = 0
    for l in lines:
        varint(len(l), b)
        for x, y in l:
            dx, dy = x-px, y-py; px, py = x, y; varint((dx << 1) ^ (dx >> 63), b); varint((dy << 1) ^ (dy >> 63), b)
    return base64.b64encode(gzip.compress(bytes(b), 9, mtime=0)).decode()

roads = json.load(gzip.open(D+'roads.json.gz')); wad = json.load(gzip.open(D+'wadis.json.gz'))
urb = json.load(gzip.open(D+'urban.json.gz')); pl = json.load(gzip.open(D+'places.json.gz'))
res = {}; info = {}
for c in 'mpst':
    ls = join([dec(a) for a in roads[c]]); ls = [simp(l, 0.0005) for l in ls]; ls = [l for l in ls if len(l) > 1]
    res[c] = pack(ls); info[c] = (len(ls), sum(map(len, ls)), len(res[c]))
ws = [l for l in join([dec(a) for a in wad]) if km(l) >= 10]; ws = [simp(l, 0.00075) for l in ws]
res['w'] = pack(ws); info['w'] = (len(ws), sum(map(len, ws)), len(res['w']))
us = [simp(dec(e[1]), 0.0005) for e in urb if e[0] >= 0.5]; us = [u for u in us if len(u) >= 4]
res['u'] = pack(us); info['u'] = (len(us), sum(map(len, us)), len(res['u']))
towns = [[p[2], p[4] or p[3], round(p[1], 4), round(p[0], 4)] for p in pl if p[2] <= 1]
js = ('// Offline map layers from OpenStreetMap (c) OpenStreetMap contributors, ODbL 1.0, Geofabrik GCC extract; built by tools/osm.\n'
      '// m motorway+trunk, p primary, s secondary, t tertiary, w wadis >=10 km, u residential areas >=0.5 km2. Format: see tools/osm/pack.py\n'
      'const OSMB=' + json.dumps(res, separators=(',', ':')) + ';\n'
      'const OSM_TOWNS=' + json.dumps(towns, separators=(',', ':'), ensure_ascii=False) + '; // [0 city|1 town, name, lat, lon]\n')
open(OUT, 'w', encoding='utf-8').write(js)
print(json.dumps(info), 'towns', len(towns), 'js bytes', len(js.encode()))
