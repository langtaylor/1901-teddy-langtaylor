수백 편까지 제작할 계획이라면 `scripts/ep01.md` 방식은 지금부터 바꾸는 것이 좋습니다.

제 원픽은 에피소드 단위 독립 폴더 + 중앙 세계관(Canon) + 제작 파이프라인 분리 구조입니다.

특히 「테일러 랭」은 일반 소설이 아니라 10분짜리 SF 추리 애니메이션 + IT·AI 교육 + ComfyUI 영상 제작이므로, 대본뿐 아니라 음성·장면·기술 감수·연속성까지 관리해야 합니다.

## 1. 추천하는 최종 디렉터리 구조

TAYLOR LANG STUDIO — 프로젝트 구조

```
taylor-lang/
│
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
│
├── canon/                   # 세계관 정본
│   ├── HARNESS.md
│   ├── characters/
│   │   ├── lang.md
│   │   ├── faye.md
│   │   └── bird.md
│   ├── world/
│   │   ├── timeline.md
│   │   ├── langtailor.md
│   │   └── robotics.md
│   ├── rules/
│   │   ├── storytelling.md
│   │   └── technical-accuracy.md
│   └── continuity.md
│
├── arcs/                    # 장기 서사
│   ├── ARC001/
│   │   └── outline.md
│   └── ARC002/
│       └── outline.md
│
├── episodes/                # 모든 에피소드
│   ├── EP0001/
│   │   ├── episode.yaml
│   │   ├── synopsis.md
│   │   ├── screenplay.md
│   │   ├── scenes.yaml
│   │   ├── shots.yaml
│   │   └── production/
│   │       ├── voice/
│   │       ├── prompts/
│   │       └── edit/
│   │
│   ├── EP0002/
│   ├── EP0003/
│   └── ...
│
├── assets/                  # 공용 제작 자산
│   ├── characters/
│   ├── backgrounds/
│   ├── music/
│   └── comfyui-workflows/
│
├── templates/
│   ├── episode.yaml
│   ├── synopsis.md
│   ├── screenplay.md
│   └── shots.yaml
│
├── catalog/
│   ├── episodes.csv
│   └── glossary.md
│
└── tools/
    ├── new_episode.py
    ├── validate_canon.py
    └── build_catalog.py
```

이 구조의 핵심은 EP0001 하나가 하나의 완결된 제작 프로젝트가 된다는 점입니다.

에피소드가 10개든 500개든 동일한 구조를 반복하면 됩니다.

## 2. 왜 시즌별 폴더가 아니라 EP0001인가?

처음에는 `season01/ep01`도 괜찮습니다. 하지만 10년 이상 연재하면 시즌 구성이 바뀌거나 특별편이 생길 수 있습니다.

그래서 에피소드 자체에는 바뀌지 않는 고유 번호를 부여합니다.

| ID     | 작품 제목     | 시즌  | 기술     |
| ------ | --------- | --- | ------ |
| EP0001 | 보이지 않는 사람 | S01 | PATH   |
| EP0002 | 잃어버린 기억   | S01 | RAG    |
| EP0003 | 두 개의 진실   | S01 | Git    |
| EP0004 | 격리된 방     | S01 | Docker |
| EP0100 | 미정        | 미정  | 미정     |

EP0002 이후의 제목과 기술은 구조를 설명하기 위한 가칭이며 확정된 시나리오가 아닙니다.

폴더명은 유지하고 시즌·제목·서사 아크 정보는 `episode.yaml`에서 관리합니다.

## 3. 에피소드마다 반드시 필요한 메타데이터

예를 들어 `episodes/EP0001/episode.yaml`을 다음처럼 구성합니다.

```
id: EP0001
title: "보이지 않는 사람"
series: "TAYLOR LANG"

season: 1
arc: null
status: draft

duration_target_sec: 600

genre:
  - sci-fi
  - mystery
  - technical-drama

characters:
  - lang
  - faye
  - bird
  - R-17

technology:
  primary: "PATH environment variable"
  secondary:
    - "Linux process execution"
    - "Debugging"

narrative:
  viewpoint: "lang-first-person"
  narration_ratio: 0.70
  dialogue_ratio: 0.15
  ambience_ratio: 0.15

production:
  video_engine: "ComfyUI"
  target_resolution: "1920x1080"
  status: "not-started"

youtube:
  status: "not-published"
  url: null
```

이 데이터가 있으면 나중에 300편이 되어도 다음과 같은 작업을 자동화할 수 있습니다.

- Docker를 다룬 에피소드 검색
- 페이가 등장하는 모든 에피소드 조회
- 미완성 에피소드만 추출
- 유튜브 업로드 여부 및 기술 주제 중복 점검
- 연속된 사건(아크)에 속한 에피소드 추적

## 4. 가장 중요한 것은 시나리오와 제작 데이터를 분리하는 것입니다

synopsis.md — 사건 설계

사건 발생, 용의자에 해당하는 기술적 가설, 단서, 반전, 해결을 정의합니다. 실제 대사가 없는 이야기의 설계도입니다.

screenplay.md — 최종 대본

랭의 1인칭 내레이션, 페이·버드의 직접 대사, 장면 지시를 기록합니다. LLM이 대본을 수정하는 기준 문서입니다.

scenes.yaml / shots.yaml — 장면과 컷

장면을 고유 ID로 구분하고, 각 컷의 길이·카메라 구도·등장인물·대사 참조·ComfyUI 프롬프트를 연결합니다.

production/ — 실제 제작

TTS 음성, 이미지 생성 프롬프트, 영상 컷 목록, 편집 타임라인과 출력물 위치를 관리합니다.

예를 들어 `EP0001-S03-C005`라는 고유 컷 ID를 만들면, 나중에 랭의 내레이션 하나를 수정할 때도 어떤 영상 컷과 음성 파일을 다시 만들어야 하는지 추적하기 쉬워집니다.

## 5. 수백 편을 연재할 때 가장 중요한 구조: Canon과 Continuity

여기서는 반드시 구분해야 합니다.

- Canon: 바뀌면 안 되는 세계관, 캐릭터 성격, 호칭, 기술 추리 원칙
- Continuity: 각 에피소드에서 실제로 벌어진 사건과 그 결과

예를 들어 40화에서 페이가 공방을 떠났다면, 41화 이후에는 그 사실이 반영되어야 합니다.

그러나 페이가 공방을 떠났다고 해서 본래 캐릭터 설정을 마음대로 삭제하면 안 됩니다.

따라서 각 에피소드가 최종 승인되면 중요한 사건만 연속성 기록에 반영해야 합니다. LLM이 임의로 세계관을 수정하지 못하도록 Canon 변경은 별도 승인을 받는 구조가 좋습니다.

## 6. 여러 LLM의 역할도 분리할 수 있습니다

### 권장 제작 파이프라인

01 · 세계관 / 사건 기획

Canon 확인 → synopsis.md

02 · 시나리오 작성

screenplay.md → 기술·논리 감수 → 승인

03 · 영상 설계

scenes.yaml → shots.yaml → TTS 타이밍

04 · RTX 5090 제작

ComfyUI → 이미지·영상·음성 합성 → 편집

05 · 검수 및 공개

스토리·기술 검수 → YouTube → Continuity 반영

ChatGPT, Claude, Gemini, Grok 중 어느 모델이 작업하든 동일한 `episode.yaml`과 Canon을 읽게 하면 됩니다. 특정 LLM에 캐릭터나 에피소드 설정을 종속시키지 않는 구조입니다.

또한 Git에는 MD, YAML, 코드, 가벼운 제작 설정만 저장하는 것을 권합니다. ComfyUI의 대용량 MP4, WAV, 중간 렌더링 파일은 RTX 5090의 작업 SSD나 NAS에 별도로 두고, 에피소드 ID와 컷 ID로 연결하세요.

## 최종 원픽

`episodes/EP0001/` 독립 에피소드 구조를 지금부터 채택하겠습니다.

그리고 설계 원칙은 다음 세 가지로 충분합니다.

1. Canon은 공통, 에피소드는 독립: 수백 편이 되어도 중복된 캐릭터·세계관 설정을 만들지 않습니다.
2. 대본과 제작물은 분리: 이야기를 수정하더라도 영상 파이프라인 전체를 다시 설계하지 않습니다.
3. LLM은 협업자, Git은 기록 저장소: 모델이 바뀌더라도 공식 설정과 승인된 대본은 동일하게 유지합니다.

특히 `new_episode.py`를 만들어 `EP0002`를 생성하면, 필요한 MD·YAML 템플릿과 제작 폴더가 자동으로 만들어지게 하세요.

결국 목표는 "에피소드를 하나 만들 때마다 새 프로젝트를 고민하는 것"이 아니라, "사건 하나만 결정하면 정해진 제작 파이프라인으로 들어가는 것"입니다. 이것이 「테일러 랭」을 수백 편까지 지속 가능한 개인 제작 스튜디오로 만드는 구조입니다.

## TAYLOR LANG META HARNESS

### 1. 목적
수백 편 이상의 애니메이션을 일관된
구조로 제작하고 관리한다.

### 2. 문서 역할
- harness/: 프로젝트 운영 규칙
- canon/: 공식 작품 세계관
- arcs/: 장기 서사
- episodes/: 독립 에피소드
- templates/: 제작 템플릿
- catalog/: 전체 작품 색인
- tools/: 제작 자동화

### 3. 에피소드 규칙
- ID: EP0001부터 순차 부여
- 폴더 이름 변경 금지
- 시즌과 제목은 메타데이터로 관리
- 대본과 영상 제작 데이터 분리

### 4. 변경 권한
- Canon 변경은 사용자 승인 필요
- Meta Harness 변경은 사용자 승인 필요
- 기존 에피소드 임의 덮어쓰기 금지

### 5. 신규 에피소드
templates/를 기준으로 생성한다.
기존 에피소드 구조를 재사용한다.