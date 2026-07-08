# Cobblemon 스폰 데이터 QA 리포트

- 처리한 species 파일 수: **823**
- 파싱된 스폰 엔트리 수 (`type:"pokemon"`): **2853**
- 고유 종(species) 수: **873**

## 주요 설계 판단 (methodology notes)

- **폼(aspect) 처리**: `pokemon` 필드는 종종 `"raichu alolan"`, `"unown character=a"`처럼 공백으로 구분된 aspect를 포함한다. 알로라/가라르/히스이/팔데아/발렌시아 지역 폼(bare word, 타입·능력이 실제로 다름)은 별도 행으로 유지하고 (ko_kr.json에 이름이 없어 영어 fallback), 그 외 순수 코스메틱 aspect(unown character=, floette/flabebe/florges flower=, magikarp magikarp_jump=, arbok/ekans snake_pattern=, vivillon vivillon_wings=, spinda spots, basculin striped=, gastrodon/shellos sea=, miltank mooshtank=, maushold family=, tea 계열 authenticity=, region_bias=, pyroar female/male 등, 동일 개체·동일 스탯의 겉모습 변형)은 기본 종으로 합쳐서 중복 행을 없앴다.
- **anticondition 처리**: 스폰 JSON의 `anticondition.biomes`는 특정 구체 바이옴을 배제하는 용도지만, 우리 16개 버킷 단위에서는 anticondition 태그가 condition 태그와 같은 버킷을 부분적으로 공유하는 경우가 많아(예: abra는 `is_hills`+`is_temperate`로 산/숲/평원에 매칭되는데 anticondition `is_magical`도 우연히 숲/산 계열 리프를 포함함) 버킷 단위로 전체 차감하면 실제로 나오는 몬스터가 사라지는 오류가 생겼다. 따라서 anticondition은 `tags_raw`에 기록만 하고 버킷 포함 여부에는 반영하지 않았다(과소포함보다 과다포함이 스폰 가이드 목적에 더 안전하다고 판단).
- **`#cobblemon:is_overworld` 처리**: 이 태그 자체 정의는 바닐라 `#minecraft:is_overworld`/`#c:is_overworld`를 그대로 가리킬 뿐 실제 바이옴 목록을 담고 있지 않다(사실상 "오버월드 어디서나"). 과제 지침대로 네더·엔드를 제외한 나머지 14개 육상/수상 버킷 전체에 매핑했다.

## 바이옴별 종 수 (16개)

| 바이옴 | 종 수 |
|---|---|
| plains | 549 |
| forest | 517 |
| flower | 366 |
| jungle | 521 |
| desert | 414 |
| badlands | 390 |
| mountain | 568 |
| cave | 412 |
| snow | 416 |
| taiga | 410 |
| swamp | 427 |
| river | 415 |
| ocean | 389 |
| beach | 423 |
| nether | 124 |
| end | 15 |

## TAG_MAP (직접 매핑, DIRECT_MAP)

| 태그 | 버킷 |
|---|---|
| `#cobblemon:has_block/mud` | swamp |
| `#cobblemon:is_badlands` | badlands |
| `#cobblemon:is_beach` | beach |
| `#cobblemon:is_cave` | cave |
| `#cobblemon:is_cherry_blossom` | flower |
| `#cobblemon:is_coast` | beach |
| `#cobblemon:is_cold_ocean` | ocean |
| `#cobblemon:is_deep_dark` | cave |
| `#cobblemon:is_deep_ocean` | ocean |
| `#cobblemon:is_desert` | desert |
| `#cobblemon:is_dripstone` | cave |
| `#cobblemon:is_end` | end |
| `#cobblemon:is_floral` | flower |
| `#cobblemon:is_forest` | forest |
| `#cobblemon:is_freezing` | snow |
| `#cobblemon:is_frozen_ocean` | ocean |
| `#cobblemon:is_glacial` | snow |
| `#cobblemon:is_grassland` | plains |
| `#cobblemon:is_highlands` | mountain |
| `#cobblemon:is_hills` | mountain |
| `#cobblemon:is_jungle` | jungle |
| `#cobblemon:is_lukewarm_ocean` | ocean |
| `#cobblemon:is_mountain` | mountain |
| `#cobblemon:is_mushroom` | cave |
| `#cobblemon:is_ocean` | ocean |
| `#cobblemon:is_overworld` | plains, forest, flower, jungle, desert, badlands, mountain, cave, snow, taiga, swamp, river, ocean, beach |
| `#cobblemon:is_peak` | mountain |
| `#cobblemon:is_plains` | plains |
| `#cobblemon:is_plateau` | mountain |
| `#cobblemon:is_river` | river |
| `#cobblemon:is_sandy` | desert |
| `#cobblemon:is_savanna` | plains |
| `#cobblemon:is_shrubland` | plains |
| `#cobblemon:is_snowy` | snow |
| `#cobblemon:is_snowy_forest` | forest, snow |
| `#cobblemon:is_snowy_taiga` | taiga, snow |
| `#cobblemon:is_swamp` | swamp |
| `#cobblemon:is_taiga` | taiga |
| `#cobblemon:is_temperate_ocean` | ocean |
| `#cobblemon:is_tundra` | snow |
| `#cobblemon:is_warm_ocean` | ocean |
| `#cobblemon:nether/is_basalt` | nether |
| `#cobblemon:nether/is_crimson` | nether |
| `#cobblemon:nether/is_desert` | nether |
| `#cobblemon:nether/is_forest` | nether |
| `#cobblemon:nether/is_frozen` | nether |
| `#cobblemon:nether/is_fungus` | nether |
| `#cobblemon:nether/is_mountain` | nether |
| `#cobblemon:nether/is_overgrowth` | nether |
| `#cobblemon:nether/is_quartz` | nether |
| `#cobblemon:nether/is_soul_fire` | nether |
| `#cobblemon:nether/is_soul_sand` | nether |
| `#cobblemon:nether/is_toxic` | nether |
| `#cobblemon:nether/is_warped` | nether |
| `#cobblemon:nether/is_wasteland` | nether |
| `#minecraft:is_nether` | nether |

## 모호(ambiguous) 태그 — 파일 fetch 후 재귀 키워드 분류로 해석

| 태그 | 해석된 버킷 |
|---|---|
| `#cobblemon:is_arid` | badlands, desert, plains |
| `#cobblemon:is_bamboo` | cave, desert, forest, jungle, mountain, ocean, swamp |
| `#cobblemon:is_cold` | cave, desert, forest, mountain, ocean, plains, river, snow, swamp, taiga |
| `#cobblemon:is_freshwater` | desert, forest, jungle, river, swamp |
| `#cobblemon:is_island` | badlands, beach, cave, desert, jungle, mountain, nether, plains, river, snow |
| `#cobblemon:is_lush` | cave, jungle, swamp |
| `#cobblemon:is_magical` | beach, cave, forest, jungle, mountain, plains, river, snow, taiga |
| `#cobblemon:is_overworld` | badlands, beach, cave, desert, flower, forest, jungle, mountain, ocean, plains, river, snow, swamp, taiga |
| `#cobblemon:is_saltwater` | ocean |
| `#cobblemon:is_sky` | mountain, river |
| `#cobblemon:is_spooky` | forest, plains, swamp, taiga |
| `#cobblemon:is_temperate` | forest, plains |
| `#cobblemon:is_thermal` | cave, desert, mountain, river, snow, taiga |
| `#cobblemon:is_tropical_island` | beach, jungle, mountain |
| `#cobblemon:is_volcanic` | cave, jungle, mountain, plains, snow |
| `#cobblemon:is_warm` | (빈 집합) |
| `#cobblemon:is_water` | ocean |

## 실제 사용된 전체 조건 문자열 → 해석 버킷 (used-in-data audit)

| 원본 조건 문자열 | 해석 버킷 |
|---|---|
| `#aether:is_aether` | (매핑 실패) |
| `#cobblemon:has_block/mud` | swamp |
| `#cobblemon:is_arid` | badlands, desert, plains |
| `#cobblemon:is_badlands` | badlands |
| `#cobblemon:is_bamboo` | cave, desert, forest, jungle, mountain, ocean, swamp |
| `#cobblemon:is_beach` | beach |
| `#cobblemon:is_cherry_blossom` | flower |
| `#cobblemon:is_coast` | beach |
| `#cobblemon:is_cold` | cave, desert, forest, mountain, ocean, plains, river, snow, swamp, taiga |
| `#cobblemon:is_cold_ocean` | ocean |
| `#cobblemon:is_deep_dark` | cave |
| `#cobblemon:is_deep_ocean` | ocean |
| `#cobblemon:is_desert` | desert |
| `#cobblemon:is_dripstone` | cave |
| `#cobblemon:is_end` | end |
| `#cobblemon:is_floral` | flower |
| `#cobblemon:is_forest` | forest |
| `#cobblemon:is_freezing` | snow |
| `#cobblemon:is_freshwater` | desert, forest, jungle, river, swamp |
| `#cobblemon:is_frozen_ocean` | ocean |
| `#cobblemon:is_glacial` | snow |
| `#cobblemon:is_grassland` | plains |
| `#cobblemon:is_highlands` | mountain |
| `#cobblemon:is_hills` | mountain |
| `#cobblemon:is_island` | badlands, beach, cave, desert, jungle, mountain, nether, plains, river, snow |
| `#cobblemon:is_jungle` | jungle |
| `#cobblemon:is_lukewarm_ocean` | ocean |
| `#cobblemon:is_lush` | cave, jungle, swamp |
| `#cobblemon:is_magical` | beach, cave, forest, jungle, mountain, plains, river, snow, taiga |
| `#cobblemon:is_mountain` | mountain |
| `#cobblemon:is_mushroom` | cave |
| `#cobblemon:is_ocean` | ocean |
| `#cobblemon:is_overworld` | badlands, beach, cave, desert, flower, forest, jungle, mountain, ocean, plains, river, snow, swamp, taiga |
| `#cobblemon:is_peak` | mountain |
| `#cobblemon:is_plains` | plains |
| `#cobblemon:is_plateau` | mountain |
| `#cobblemon:is_river` | river |
| `#cobblemon:is_savanna` | plains |
| `#cobblemon:is_shrubland` | plains |
| `#cobblemon:is_sky` | mountain, river |
| `#cobblemon:is_snowy` | snow |
| `#cobblemon:is_snowy_forest` | forest, snow |
| `#cobblemon:is_snowy_taiga` | snow, taiga |
| `#cobblemon:is_spooky` | forest, plains, swamp, taiga |
| `#cobblemon:is_swamp` | swamp |
| `#cobblemon:is_taiga` | taiga |
| `#cobblemon:is_temperate` | forest, plains |
| `#cobblemon:is_thermal` | cave, desert, mountain, river, snow, taiga |
| `#cobblemon:is_tropical_island` | beach, jungle, mountain |
| `#cobblemon:is_tundra` | snow |
| `#cobblemon:is_volcanic` | cave, jungle, mountain, plains, snow |
| `#cobblemon:is_warm_ocean` | ocean |
| `#cobblemon:nether/is_basalt` | nether |
| `#cobblemon:nether/is_crimson` | nether |
| `#cobblemon:nether/is_desert` | nether |
| `#cobblemon:nether/is_forest` | nether |
| `#cobblemon:nether/is_frozen` | nether |
| `#cobblemon:nether/is_fungus` | nether |
| `#cobblemon:nether/is_mountain` | nether |
| `#cobblemon:nether/is_overgrowth` | nether |
| `#cobblemon:nether/is_quartz` | nether |
| `#cobblemon:nether/is_soul_fire` | nether |
| `#cobblemon:nether/is_soul_sand` | nether |
| `#cobblemon:nether/is_toxic` | nether |
| `#cobblemon:nether/is_warped` | nether |
| `#cobblemon:nether/is_wasteland` | nether |
| `#minecraft:is_nether` | nether |
| `#the_bumblezone:the_bumblezone` | (매핑 실패) |
| `aether:skyroot_forest` | forest, mountain |
| `aether:skyroot_grove` | forest, mountain |
| `aether:skyroot_meadow` | mountain, plains |
| `aether:skyroot_woodland` | forest, mountain |
| `biomesoplenty:crystalline_chasm` | mountain |
| `minecraft:frozen_river` | river, snow |
| `minecraft:mushroom_fields` | cave, plains |
| `minecraft:snowy_beach` | beach, snow |
| `minecraft:sunflower_plains` | flower, plains |
| `the_bumblezone:crystal_canyon` | mountain |
| `the_bumblezone:floral_meadow` | flower, plains |
| `the_bumblezone:howling_constructs` | (매핑 실패) |
| `the_bumblezone:pollinated_fields` | flower, plains |

## 매핑 실패(UNMAPPED) 리프 문자열

- `#aether:is_aether`
- `#c:is_magical`
- `#c:is_spooky`
- `#cobblemon:is_warm`
- `#the_bumblezone:the_bumblezone`
- `the_bumblezone:howling_constructs`

## neededInstalledMods 비어있지 않은 스폰 엔트리

(없음 — 데이터셋 전체에서 neededInstalledMods 필드가 항상 빈 배열)

## ko_kr.json에 이름이 없어 영어로 대체된 species slug

- `bellossom valencian`
- `braviary hisuian`
- `butterfree valencian`
- `caterpie valencian`
- `corsola galarian`
- `decidueye hisuian`
- `diglett alolan`
- `dugtrio alolan`
- `electrode hisuian`
- `exeggutor alolan`
- `farfetchd galarian`
- `geodude alolan`
- `gloom valencian`
- `golem alolan`
- `goodra hisuian`
- `graveler alolan`
- `grimer alolan`
- `lilligant hisuian`
- `linoone galarian`
- `marowak alolan`
- `meowth alolan`
- `meowth galarian`
- `metapod valencian`
- `mrmime galarian`
- `muk alolan`
- `ninetales alolan`
- `oddish valencian`
- `persian alolan`
- `ponyta galarian`
- `qwilfish hisuian`
- `raichu alolan`
- `rapidash galarian`
- `raticate alolan`
- `rattata alolan`
- `samurott hisuian`
- `sliggoo hisuian`
- `slowbro galarian`
- `slowking galarian`
- `slowpoke galarian`
- `sneasel hisuian`
- `stunfisk galarian`
- `typhlosion hisuian`
- `vileplume valencian`
- `voltorb hisuian`
- `vulpix alolan`
- `weezing galarian`
- `wooper paldean`
- `zigzagoon galarian`
- `zoroark hisuian`
- `zorua hisuian`

## 0개 바이옴으로 귀결된 species (조사 필요)

총 0건

## 비정상 rarity bucket (common/uncommon/rare/ultra-rare 외)

(없음 — 전체 데이터셋이 4개 표준 버킷만 사용)

