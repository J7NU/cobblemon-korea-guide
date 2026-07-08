# -*- coding: utf-8 -*-
# Splice normalized spawn data + new biome-browser JS into the guide HTML.
import json, io

HTML='cobblemon-korea-guide.html'
lines=open(HTML,encoding='utf-8').read().split('\n')

# sanity: confirm boundaries (1-indexed 2017 = const RB, 2176 = })(); )
assert lines[2016].strip().startswith('const RB='), repr(lines[2016])
assert lines[2175].strip()=='})();', repr(lines[2175])
assert lines[2176].strip()=='</script>', repr(lines[2176])

BIOME_META=[
 {"id":"plains","emoji":"🌾","name":"평원·초원","desc":"가장 흔한 지형. 초보 초반 포획에 최적.","mcid":"plains, sunflower_plains, meadow"},
 {"id":"forest","emoji":"🌲","name":"숲·자작나무 숲","desc":"풀·벌레·페어리 타입과 초반 팀원이 풍부.","mcid":"forest, birch_forest, dark_forest"},
 {"id":"flower","emoji":"🌸","name":"꽃 숲·목초지","desc":"페어리·풀 타입이 몰리는 곳.","mcid":"flower_forest"},
 {"id":"jungle","emoji":"🌴","name":"정글","desc":"풀·벌레 타입 밀집. 습한 지역 전용 스폰.","mcid":"jungle, sparse_jungle, bamboo_jungle"},
 {"id":"desert","emoji":"🏜️","name":"사막","desc":"불꽃·땅·바위 타입과 화석 루트.","mcid":"desert"},
 {"id":"badlands","emoji":"🟧","name":"황무지(메사)","desc":"바위·불꽃 타입, 딥상어동 지하 루트.","mcid":"badlands, eroded_badlands, wooded_badlands"},
 {"id":"mountain","emoji":"⛰️","name":"산·봉우리","desc":"드래곤·바위·격투 타입 등 강력한 희귀종.","mcid":"stony_peaks, jagged_peaks, windswept_hills, meadow"},
 {"id":"cave","emoji":"🕳️","name":"동굴·지하","desc":"고스트·독·강철·바위 타입. y40 이하가 밀집 구간.","mcid":"dripstone_caves, lush_caves, deep_dark (지하 공통)"},
 {"id":"snow","emoji":"❄️","name":"눈·얼음 지대","desc":"얼음 타입. 눈 오는 날 스폰률 상승.","mcid":"snowy_plains, snowy_slopes, ice_spikes, frozen_peaks"},
 {"id":"taiga","emoji":"🌲","name":"타이가·가문비 숲","desc":"추운 침엽수림. 얼음·강철·일부 풀 타입.","mcid":"taiga, snowy_taiga, old_growth_pine/spruce_taiga"},
 {"id":"swamp","emoji":"🐸","name":"늪지","desc":"독·물·고스트 타입.","mcid":"swamp, mangrove_swamp"},
 {"id":"river","emoji":"🏞️","name":"강·시냇물","desc":"물 타입 스폰의 핵심. 스타터 물 계열도 여기.","mcid":"river, frozen_river"},
 {"id":"ocean","emoji":"🌊","name":"바다","desc":"가장 큰 물 타입 풀. 차가운 바다엔 라프라스.","mcid":"ocean, cold_ocean, deep_ocean, frozen_ocean 등"},
 {"id":"beach","emoji":"🏖️","name":"해변","desc":"물가와 육지가 만나는 곳. 게 계열·물새.","mcid":"beach, snowy_beach, stony_shore"},
 {"id":"nether","emoji":"🔥","name":"네더","desc":"불꽃·독·드래곤 타입. 지옥 차원 전용.","mcid":"nether_wastes, crimson_forest, warped_forest, basalt_deltas"},
 {"id":"end","emoji":"🌌","name":"엔드","desc":"에스퍼·드래곤 타입. 최종 차원. 스폰이 매우 적음.","mcid":"the_end, end_highlands, end_midlands"},
]

data_js=open('data/spawns-inline.js',encoding='utf-8').read().rstrip('\n')

meta_js='const BIOME_META='+json.dumps(BIOME_META,ensure_ascii=False,separators=(',',':'))+';'

block=r'''  /* ===== 스폰 데이터 (Cobblemon 공식 spawn_pool_world, GitLab main 기준 자동 생성) ===== */
%DATA%
  const RB={common:['흔함','gray'],uncommon:['보통','green'],rare:['희귀','blue'],ultra:['초희귀','gold']};
  const R2=['common','uncommon','rare','ultra'];
  const SP=window._SP||[],BSPEC=window._BSPEC||{},UNIV=window._UNIV||[],SDET=window._SDET||{};
  %META%
  const _METABY={};BIOME_META.forEach(m=>_METABY[m.id]=m);
  function e2mon(e){const s=SP[e[0]]||['?','?'];return [s[0],s[1],R2[e[1]],e[2]||''];}
  const BIOMES=BIOME_META.map(m=>({id:m.id,emoji:m.emoji,name:m.name,desc:m.desc,mcid:m.mcid,mons:(BSPEC[m.id]||[]).map(e2mon)}));
  const LAND=new Set(BIOME_META.filter(m=>m.id!=='nether'&&m.id!=='end').map(m=>m.id));
  const RARITY_ORDER=['common','uncommon','rare','ultra'];
  let selBiome=null,rarityFilter='all';

  /* 지연 렌더: 바이옴 스폰 탭 첫 활성 시 버튼 생성 */
  _lazyTab.spawn=function(){
    BIOMES.forEach(b=>{
      const btn=document.createElement('button');
      btn.className='biomebtn';btn.type='button';btn.dataset.id=b.id;
      btn.innerHTML='<span class="emoji">'+b.emoji+'</span>'+b.name;
      grid.appendChild(btn);
    });
  };

  const emptyCard=document.getElementById('spawnEmptyCard'),resultCard=document.getElementById('spawnResultCard');
  const emojiEl=document.getElementById('spawnBiomeEmoji'),nameEl=document.getElementById('spawnBiomeName'),descEl=document.getElementById('spawnBiomeDesc'),bodyEl=document.getElementById('spawnResultBody');

  function monRows(list){
    let html='';
    RARITY_ORDER.forEach(r=>{
      if(rarityFilter!=='all'&&rarityFilter!==r)return;
      const sub=list.filter(m=>m[2]===r);
      if(!sub.length)return;
      const [rlabel,rcolor]=RB[r];
      html+='<div class="raritygroup"><h3><span class="tag '+rcolor+'">'+rlabel+'</span> <span style="font-size:12px;color:var(--muted);font-weight:400">'+sub.length+'종</span></h3>';
      html+=sub.map(m=>{
        const cond=m[3]?'<div class="cond">↳ '+m[3]+'</div>':'';
        const en=m[1]?'<span class="en">'+esc(m[1])+'</span>':'';
        const nm='<span class="kr pmon" data-kr="'+esc(m[0])+'" data-en="'+esc(m[1])+'">'+esc(m[0])+'</span>';
        return '<div class="mon">'+nm+en+cond+'</div>';
      }).join('');
      html+='</div>';
    });
    return html;
  }

  function render(){
    if(!selBiome){resultCard.style.display='none';emptyCard.style.display='block';return}
    const b=BIOMES.find(x=>x.id===selBiome);
    emptyCard.style.display='none';resultCard.style.display='block';
    emojiEl.textContent=b.emoji;nameEl.textContent=b.name;
    descEl.innerHTML=b.desc+(b.mcid?' <br><span style="color:var(--blue);font-size:12px">마크 바이옴: '+b.mcid+'</span>':'');
    let html=monRows(b.mons);
    if(!html)html='<p class="emptytype">이 필터에 해당하는 포켓몬이 없어</p>';
    if(LAND.has(b.id)&&UNIV.length){
      const specIdx=new Set((BSPEC[b.id]||[]).map(e=>e[0]));
      const uList=UNIV.filter(e=>!specIdx.has(e[0])).map(e2mon);
      const uh=monRows(uList);
      if(uh)html+='<details class="univbox"><summary>🌍 이 외 <b>전역 스폰</b> 더보기 <span class="kv">(아무 바이옴이나 나오는 '+uList.length+'종)</span></summary><div class="univbody">'+uh+'</div></details>';
    }
    bodyEl.innerHTML=html;
  }

  grid.addEventListener('click',e=>{
    const b=e.target.closest('.biomebtn');if(!b)return;
    document.querySelectorAll('.biomebtn').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');selBiome=b.dataset.id;render();
  });
  document.getElementById('rarityFilter').addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b)return;
    document.querySelectorAll('#rarityFilter button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');rarityFilter=b.dataset.r;render();
  });

  /* 스폰맵 빌드 — 도감에서 스폰 정보 표시용 (EN·KR 양쪽 키) */
  window._BIOMES=BIOMES;
  window._SPAWN_MAP={};
  Object.keys(SDET).forEach(i=>{
    const s=SP[i];if(!s)return;
    const arr=SDET[i].map(d=>{
      const isU=d[0]==='*';const m=_METABY[d[0]];
      return {biome:isU?'전역 (아무 바이옴이나)':(m?m.name:d[0]),emoji:isU?'🌍':(m?m.emoji:''),rarity:R2[d[1]],cond:d[2]||null,level:d[3]||null};
    });
    const kk=s[0].replace(/\(.*?\)/g,'').trim();
    window._SPAWN_MAP[s[1]]=arr;
    if(!window._SPAWN_MAP[kk])window._SPAWN_MAP[kk]=arr;
  });
})();
/* ===== 통합 검색 인덱스 빌드 (페이지 로드 시 1회) ===== */
window._SPAWN_IDX=(function(){
  const R2=['common','uncommon','rare','ultra'];
  const idx=[];
  (window._BIOMES||[]).forEach(b=>b.mons.forEach(m=>{
    idx.push({kr:m[0],en:m[1],biomeId:b.id,biomeName:b.name,biomeEmoji:b.emoji,rarity:m[2],cond:m[3]||null});
  }));
  const SP=window._SP||[];
  (window._UNIV||[]).forEach(e=>{
    const s=SP[e[0]];if(!s)return;
    idx.push({kr:s[0],en:s[1],biomeId:'*',biomeName:'🌍 전역',biomeEmoji:'🌍',rarity:R2[e[1]],cond:e[2]||null});
  });
  return idx;
})();'''

block=block.replace('%DATA%',data_js).replace('%META%',meta_js)

new_lines=lines[:2016]+block.split('\n')+lines[2176:]
open(HTML,'w',encoding='utf-8').write('\n'.join(new_lines))
print('spliced. new line count:', len('\n'.join(new_lines).split('\n')))
