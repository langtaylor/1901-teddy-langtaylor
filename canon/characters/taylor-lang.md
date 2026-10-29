# Taylor Lang — 의상 정본 (v3)

> 결정일: 2026-10-29 (CEO 결정)
> **기준 앵커: lang_anchor_fullbody_v3.png** (Qwen_Edit_2511_00036 채택)
> 이전 원본: lang_anchor_fullbody_v2.png (올리브 카고 바지 버전, 보관만)

## 결정 사항

| 부위 | 결정 | 비고 |
|---|---|---|
| 얼굴·헤어·자세 | v2 100% 유지 | 검은 곱슬머리, 옅은 수염, 비스듬한 미소 |
| 상의 | v2 100% 유지 | 올리브 워크셔츠, 가슴 포켓 2개, 소매 걷음, 낡은 녹 얼룩 텍스처 |
| 이너 | 유지 | 검은 티셔츠 |
| 하의 | **변경 완료** | 따뜻한 차콜 그레이 워크팬츠, 일자 핏, 무광, **얼룩 없이 깨끗함** |
| 카고 포켓 | **제거 완료** | 허벅지 대형 포켓 없음 |
| 허리 포켓 | **추가 완료** | 랭 기준 오른쪽 허리(화면에서는 왼쪽)에 얇은 세로 포켓 1개 + 정밀 수리 펜 |
| 앰버 포인트 | 앵커에는 없음 | 클로즈업·작업 장면에서만 펜 끝 라이트로 표현 |
| 신발 | v2 유지 | 다크 브라운 레더 부츠 |

## 의도

- 군인이 아니라 수리기사로 읽힐 것 (설명 없이 의상만으로)
- 상하의 색 분리로 작은 화면·썸네일에서도 실루엣이 읽힐 것
- 바지 밝기는 셔츠와 비슷하거나 살짝 어둡게: 시선이 다리가 아니라 얼굴로 가도록
- 셔츠만 낡고 바지는 깨끗함: 얼룩을 바지에 넣으면 찢어진 청바지처럼 보여 기각

## 색상 코드 (참고값)

- 올리브 셔츠: #3B4228 계열
- 차콜 팬츠: #161617 계열 (다크 차콜)
- 브라운 부츠: #3A2620 계열
- 앰버 포인트: #FFB000 계열 (클로즈업에서 아주 작은 면적만)

## 기각된 안 (다시 시도하지 말 것)

- 밝은 그레이 바지: 셔츠보다 밝아 시선이 다리로 감, 사무용 슬랙스 느낌
- 얼룩·해짐 있는 바지: 찢어진 청바지·빈티지 느낌
- 거의 검정 바지: 이너·부츠와 뭉쳐 다리 형태가 안 읽힘
- 청바지: 2040년 시대감이 사라짐

## 전신 신규 생성용 프롬프트 (다른 포즈·장면에서 재사용)

v3 앵커를 레퍼런스 이미지로 함께 넣을 것.

```
Taylor Lang, man in his 30s, messy black wavy hair, light stubble, sly half smile, lean build,
dark olive work shirt with two chest pockets, sleeves rolled up to forearms, worn rust-stained texture,
black t-shirt underneath, clean warm charcoal gray straight work pants without cargo pockets,
small slim vertical pocket at right hip with a precision repair pen,
dark brown leather boots, android repair technician, year 2040,
anime illustration, clean lineart, full body, white background
```

### Negative

```
cargo pockets, thigh pockets, military, camouflage, army, olive pants, green pants,
jeans, denim, stains on pants, ripped pants, distressed pants, light gray pants, black pants,
tactical gear, bulky pockets, extra legs, deformed hands, blurry, different art style
```

## Qwen Image Edit 2511 부분 수정 요령 (이번 작업에서 확인)

- 지시문 형식으로 쓸 것: "Change only ..., keep everything else exactly the same."
- Load Image에서 마스크 칠하기 → Set Latent Noise Mask로 KSampler에 연결해야 마스크 밖이 안 바뀜
- 모양까지 바꿀 때 denoise 1.00, 색만 바꿀 때 0.60
- multiple-angles LoRA는 정면 편집 시 strength 0
- 얼룩 같은 세부는 낮은 denoise로 지워지지 않음: 얼룩 넣기 전 그림으로 돌아가서 다시 작업