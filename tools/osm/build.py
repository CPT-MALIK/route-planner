"""Builds compact Saudi map layers (roads, wadis, built-up areas, place names) from an OSM GeoJSON-seq export.
Runs on GitHub Actions (see .github/workflows/osm-extract.yml). Output: delta-encoded integer coordinates (1e-5 deg), gzipped JSON."""
import json, sys, gzip, math, collections
src, outdir = sys.argv[1], sys.argv[2]
TOL = 0.00015  # ~16 m Douglas-Peucker tolerance (deg); final per-zoom thinning is done when embedding

def dp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False]*len(pts); keep[0] = keep[-1] = True; st = [(0, len(pts)-1)]
    while st:
        a, b = st.pop(); ax, ay = pts[a]; bx, by = pts[b]; dx, dy = bx-ax, by-ay; L = dx*dx+dy*dy; best, bi = 0, -1
        for i in range(a+1, b):
            px, py = pts[i]
            if L == 0: d = math.hypot(px-ax, py-ay)
            else:
                t = max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L)); d = math.hypot(px-(ax+t*dx), py-(ay+t*dy))
            if d > best: best, bi = d, i
        if best > tol: keep[bi] = True; st += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

def enc(pts):
    o = []; px = py = 0
    for x, y in pts:
        X, Y = round(x*1e5), round(y*1e5); o += [X-px, Y-py]; px, py = X, Y
    return o

def ring_area_km2(r):
    a = 0; lat = sum(p[1] for p in r)/len(r); k = 111.32*111.32*math.cos(math.radians(lat))
    for (x1, y1), (x2, y2) in zip(r, r[1:]+r[:1]): a += x1*y2-x2*y1
    return abs(a)/2*k

RCLS = {'motorway':'m','motorway_link':None,'trunk':'m','primary':'p','secondary':'s','tertiary':'t'}
roads = collections.defaultdict(list); wadis = []; urban = []; places = []; stats = collections.Counter()
with open(src, encoding='utf-8') as f:
    for line in f:
        line = line.strip().lstrip('\x1e')
        if not line: continue
        ft = json.loads(line); g = ft.get('geometry') or {}; p = ft.get('properties') or {}; t = g.get('type')
        if t == 'Point' and p.get('place') in ('city','town','village'):
            x, y = g['coordinates']
            places.append([round(x,5), round(y,5), {'city':0,'town':1,'village':2}[p['place']], p.get('name:ar') or p.get('name') or '', p.get('name:en') or '', int(''.join(c for c in (p.get('population') or '0') if c.isdigit()) or 0)])
            stats['place_'+p['place']] += 1; continue
        hw = p.get('highway'); ww = p.get('waterway'); lu = p.get('landuse')
        if t == 'LineString':
            pts = dp(g['coordinates'], TOL)
            if hw in RCLS and RCLS[hw]: roads[RCLS[hw]].append(enc(pts)); stats['road_'+hw] += 1; stats['v_road'] += len(pts)
            elif ww in ('wadi','river') or (ww == 'stream' and p.get('intermittent') == 'yes'): wadis.append(enc(pts)); stats['wadi_'+ww] += 1; stats['v_wadi'] += len(pts)
        elif t in ('Polygon','MultiPolygon') and lu == 'residential':
            polys = [g['coordinates']] if t == 'Polygon' else g['coordinates']
            for poly in polys:
                r = poly[0]; A = ring_area_km2(r)
                if A < 0.05: stats['urban_small'] += 1; continue
                pts = dp(r, TOL)
                if len(pts) >= 4: urban.append([round(A, 2), enc(pts)]); stats['urban'] += 1; stats['v_urban'] += len(pts)
out = {'roads': roads, 'wadis': wadis, 'urban': urban, 'places': places}
for k, v in out.items():
    with gzip.open(f'{outdir}/{k}.json.gz', 'wt', encoding='utf-8') as g: json.dump(v, g, separators=(',', ':'), ensure_ascii=False)
json.dump(stats, open(f'{outdir}/stats.json', 'w'), indent=1)
print(json.dumps(stats, indent=1))
