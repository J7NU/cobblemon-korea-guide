#!/usr/bin/env python3
# spawns.json -> spawns-inline.js
# Classification: use TARGETED biome tags (non is_overworld) for card placement.
# is_overworld / climate-universal (targeted>=13) -> 전역 collapse. A species can be BOTH.
import json, collections

d = json.load(open('data/spawns.json'))
BIOME_IDS = ['plains','forest','flower','jungle','desert','badlands','mountain',
             'cave','snow','taiga','swamp','river','ocean','beach','nether','end']
RIDX = {'common':0,'uncommon':1,'rare':2,'ultra':3}
CUT = 13   # targeted span >= CUT -> treat as universal (collapse only)

def is_broad(r): return any('is_overworld' in t for t in r.get('tags_raw', []))

by_sp = collections.defaultdict(list)
kr_of = {}
for r in d:
    by_sp[r['en']].append(r)
    kr_of[r['en']] = r['kr']

species = sorted(by_sp.keys())
SP, sp_idx = [], {}
for en in species:
    sp_idx[en] = len(SP)
    SP.append([kr_of[en], en])

BSPEC = {b: [] for b in BIOME_IDS}   # biomeId -> [ [spIdx, rIdx, cond], ... ]
UNIV = []                             # [ [spIdx, rIdx, cond], ... ]
SDET = {}                             # spIdx -> [ [biomeId|'*', rIdx, cond, level], ... ]
tb_size = {}                          # spIdx -> targeted biome count (for sort)

for en in species:
    rows = by_sp[en]
    i = sp_idx[en]
    targeted = [r for r in rows if not is_broad(r)]
    broadrows = [r for r in rows if is_broad(r)]
    tb = set()
    for r in targeted: tb.update(r['biomes'])
    hb = len(broadrows) > 0
    is_universal = hb or len(tb) >= CUT
    place_specific = tb if len(tb) < CUT else set()
    tb_size[i] = len(tb) if tb else 99

    det = []
    # biome-specific placement (targeted)
    for b in BIOME_IDS:
        if b not in place_specific: continue
        cand = [r for r in targeted if b in r['biomes']]
        pick = sorted(cand, key=lambda r:(RIDX[r['rarity']], len(r['cond'])))[0]
        ri = RIDX[pick['rarity']]
        BSPEC[b].append([i, ri, pick['cond']])
        det.append([b, ri, pick['cond'], pick['level']])
    # universal collapse entry
    if is_universal:
        pool = broadrows if broadrows else targeted
        u = sorted(pool, key=lambda r:(RIDX[r['rarity']], -len(r['biomes'])))[0]
        UNIV.append([i, RIDX[u['rarity']], u['cond']])
        det.append(['*', RIDX[u['rarity']], u['cond'], u['level']])
    SDET[i] = det

# sort biome-specific: rarity asc, then specificity (fewer targeted biomes first), then kr
for b in BIOME_IDS:
    BSPEC[b].sort(key=lambda e:(e[1], tb_size[e[0]], SP[e[0]][0]))
UNIV.sort(key=lambda e:(e[1], SP[e[0]][0]))

def trim(e): return e[:2] if len(e) >= 3 and e[2] == '' else e
BSPEC = {b:[trim(e) for e in v] for b,v in BSPEC.items()}
UNIV = [trim(e) for e in UNIV]

out = ['/* AUTO-GENERATED from Cobblemon spawn_pool_world (GitLab main). Do not hand-edit. */']
for name, obj in [('_SP',SP),('_BSPEC',BSPEC),('_UNIV',UNIV),('_SDET',SDET)]:
    out.append('window.%s=%s;' % (name, json.dumps(obj, ensure_ascii=False, separators=(',',':'))))
js = '\n'.join(out) + '\n'
open('data/spawns-inline.js','w').write(js)

print('species:', len(SP), '| universal:', len(UNIV))
print('biome-specific:', {b:len(BSPEC[b]) for b in BIOME_IDS})
print('bytes:', len(js.encode()))
