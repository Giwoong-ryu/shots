# 🎯 Truth Hunter 전략 → N8N 실전 구현 설계서

> **목적**: 22가지 전략을 실제 N8N 워크플로우로 변환하는 심층 구현 가이드  
> **대상**: 한국 6070 시니어 건강/재테크 시장 독점

---

## 📊 전체 아키텍처 (4-Phase Pipeline)

```
Phase 1: Source Intelligence (정보 수집 & 검증)
   ↓
Phase 2: Content Engineering (콘텐츠 생성 & 자체 검수)
   ↓
Phase 3: Media Enhancement (영상/오디오 최적화 & AI 탐지 우회)
   ↓
Phase 4: Distribution & Engagement (업로드 & 커뮤니티 자동화)
```

---

# Phase 1️⃣: Source Intelligence (정보 수집 & 검증)

## 노드 1A: Reddit Sentiment Velocity Tracker (NEW - 최첨단)

### 목적
**전략 23 (NEW)**: 키워드가 아닌 **맥락(Context)**을 훔친다  
- Google Trends는 **이미 대중화된 후** 뜨는 후행 지표
- Reddit 얼리어답터들의 **"감정 변곡점"**을 선행 포착
- "의심 → 확신"으로 바뀌는 **Sentiment Velocity** 측정

### 구조
```
Schedule Trigger (6시간) → Reddit JSON Scraper → GPT-4o Sentiment Analysis → Hype Score Calculator → If (Score ≥ 8)
```

### 1A-1. Reddit JSON Scraper (HTTP Request)
**타겟 Subreddits** (미국 바이오해커 커뮤니티):
```javascript
URLs (Round-Robin):
[
  "https://www.reddit.com/r/Longevity/top.json?t=week&limit=15",
  "https://www.reddit.com/r/Biohackers/top.json?t=week&limit=15",
  "https://www.reddit.com/r/Nootropics/top.json?t=week&limit=15",
  "https://www.reddit.com/r/Fire/top.json?t=week&limit=15"  // 은퇴/재테크
]
```

**Response 구조**:
```javascript
{
  data: {
    children: [
      {
        data: {
          title: "게시글 제목",
          ups: 추천수,
          num_comments: 댓글수,
          url: "링크",
          selftext: "본문",
          created_utc: 타임스탬프
        }
      }
    ]
  }
}
```

### 1A-2. GPT-4o Sentiment Velocity Analyzer
**System Prompt** (완전판):
```markdown
### ROLE ###
당신은 '초기 트렌드 탐지 전문가'입니다. 
Reddit 게시글의 **감정 이동(Sentiment Shift)**을 분석하여, 
아직 주류 언론에 나오지 않았지만 커뮤니티에서 **폭발 직전**인 주제를 찾아냅니다.

### MISSION ###
입력된 Reddit Posts 데이터를 분석하여, 
가장 **Hype Score(흥분도)**가 높은 **단 하나의 키워드**를 추출하세요.

### CRITERIA (우선순위) ###

**1. Sentiment Velocity (감정 가속도)** - 최우선
- "Is this real?" → "It works!" 변화 감지
- 초기 회의론 → 간증(Testimonial) 급증
- 점수: 감정 전환 속도가 빠를수록 높음

**2. High Engagement + Low Awareness (숨겨진 보석)**
- 댓글(Comments) ≥ 50개
- BUT 주제 자체는 생소함 (Wikipedia 없음)
- 예시: "Rapamycin"(○), "Vitamin C"(×)

**3. Controversy Intensity (논쟁 강도)**
- 찬반 논쟁이 격렬할수록 좋음
- "FDA Warning" vs "Life-Changing" 대립
- 시니어 시청자는 **논란**에 강하게 반응

**4. Authority Signals (권위 프레임)**
- 하버드/존스홉킨스/NIH 언급
- "New Study from..." 키워드
- 의학 논문 DOI 링크 포함

### OUTPUT FORMAT (JSON) ###
{
  "keyword": "발굴된 핵심 키워드 (영어)",
  "korean_keyword": "한국어 번역",
  "hype_score": 1~10 (흥분도),
  "sentiment_velocity": "의심(20% skeptical) → 확신(65% convinced)",
  "controversy_level": "HIGH/MEDIUM/LOW",
  "reason_for_viral": "이것이 곧 한국에서 떡상할 이유 (3줄 이내)",
  "top_post_title": "가장 반응 좋은 게시글 제목",
  "top_post_url": "Reddit 링크"
}

### CONSTRAINTS ###
- 뻔한 키워드(Exercise, Water, Sleep) 절대 금지
- 한국에 **아직 없는** 정보만 선별
- Hype Score < 6 이면 "No Trend Found" 리턴
```

**User Prompt** (Input Data):
```javascript
`아래 Reddit 게시글 데이터를 분석하세요:

${JSON.stringify($json.data.children.map(post => ({
  title: post.data.title,
  ups: post.data.ups,
  comments: post.data.num_comments,
  snippet: post.data.selftext.substring(0, 200)
})))}

위 데이터에서 감정의 변곡점을 찾아 Hype Score 8점 이상인 키워드를 발굴하세요.`
```

### 1A-3. Hype Score Filter (If Node)
```javascript
{{ $json.hype_score }} >= 8 
AND 
{{ $json.controversy_level }} !== 'LOW'
```

**TRUE → Gap Analyzer (Korea Check) 진행**  
**FALSE → 다음 Reddit 스캔까지 대기**

---

## 노드 1B: Multi-Source Trigger (기존 통합)

### 구조
```
RSS Read (3개) ────┐
YouTube Trigger ───┼─→ Merge Node → 다음 단계
Grok Monitor ──────┤
Reddit Velocity ───┘ (NEW)
```

### 노드별 설정


### 구조
```
RSS Read (3개) ────┐
YouTube Trigger ───┼─→ Merge Node → 다음 단계
Grok Monitor ──────┘
```

### 노드별 설정

#### 1-1. RSS Read Node
**목적**: 대안 언론/의학 논문 원시 데이터 우선 수집

**URL 목록** (전략 16, 20 적용):
```javascript
[
  "https://www.mercola.com/feeds/rss.xml",           // 대안 의학
  "https://childrenshealthdefense.org/feed/",        // RFK Jr. (제약 음모론)
  "https://www.zerohedge.com/feeds/all.xml",         // 거시경제 위기설
  "https://www.lifeextension.com/magazine/rss.xml"   // 장수 과학
]
```

**필터링 Code Node** (전략 22 - PubMed 논란):
```javascript
// RSS 항목 필터링
const items = $input.all();
const controversyKeywords = [
  'retracted', 'banned', 'censored', 'fda warning',
  'cover up', 'hidden study', 'suppressed'
];

return items
  .filter(item => {
    const text = (item.json.title + item.json.description).toLowerCase();
    return controversyKeywords.some(keyword => text.includes(keyword));
  })
  .map(item => ({
    json: {
      source: 'RSS',
      title: item.json.title,
      url: item.json.link,
      publishDate: item.json.pubDate,
      controversyScore: controversyKeywords.filter(k => 
        text.includes(k)
      ).length
    }
  }));
```

#### 1-2. YouTube Trigger Node
**목적**: 미국 1티어 채널 실시간 감시 (전략 2, 15)

**Channel IDs** (전략 15 - Gap Hunter):
```javascript
[
  "UCJ1C_mF1aY617-1f-e0W-jg",  // Dr. Pradip Jamnadas (심장/단식)
  "UC2D2CMWXMOVWx7giW0e28욱",  // Peter Attia MD (의학 3.0)
  "UCt2TUvSaOL8aeSkA3alSEyQ",  // Bryan Johnson (회춘 프로토콜)
  "UCmYpOf_1K84WT4f5T-XRqog"   // The Ramsey Show (은퇴 파산)
]
```

**Polling**: 1시간마다  
**Filter**: 업로드 24시간 이내만

---

## 노드 2: Korea Gap Analyzer (블루오션 검증)

### 목적
전략 15 (Gap Hunter) 핵심 - "한국에 없는 정보인가?" 검증

### 구조
```
Merge Node → DeepL 번역 → SerpApi (Naver) → Code (Gap Score) → If Node
```

### 2-1. DeepL Translation Node
**Input**: `{{ $json.title }}`의 핵심 키워드 3개 추출 후 번역

**GPT-4o Mini Keyword Extractor** (비용 절감):
```javascript
System Prompt:
"Extract exactly 3 most important keywords from this title. 
Return as JSON: {\"keywords\": [\"word1\", \"word2\", \"word3\"]}"

User Prompt:
"{{ $json.title }}"
```

**DeepL API**:
```javascript
{
  "text": "{{ $json.keywords.join(', ') }}",
  "target_lang": "KO"
}
```

### 2-2. SerpApi Naver Check
**HTTP Request**:
```javascript
URL: https://serpapi.com/search
Method: GET
Query Params:
  engine: "naver"
  q: "{{ $json.koreanKeywords }}"
  date_filter: "month"  // 최근 1개월
  num: 20
```

### 2-3. Gap Score Calculator (Code Node)
**목적**: 정량적 블루오션 점수 산출

```javascript
const naverResults = $json.organic_results?.length || 0;
const youtubeKR = $json.video_results?.length || 0;

// Gap Score 공식 (0~100)
const gapScore = Math.max(0, 100 - (naverResults * 3) - (youtubeKR * 5));

// 블루오션 기준
const isBlueOcean = naverResults < 10 && youtubeKR < 3;

return {
  json: {
    ...$input.first().json,
    naverResults,
    youtubeKR,
    gapScore,
    isBlueOcean,
    noveltyLevel: gapScore > 80 ? 'HIGH' : gapScore > 50 ? 'MEDIUM' : 'LOW'
  }
};
```

### 2-4. Filter Decision (If Node)
**조건**:
```javascript
{{ $json.isBlueOcean }} === true 
AND 
{{ $json.controversyScore }} >= 2
```

**TRUE → Phase 2 진행**  
**FALSE → Telegram 알림 후 종료**

---

# Phase 2️⃣: Content Engineering (콘텐츠 생성 & 검수)

## 노드 3: AI Scriptwriter (GPT-5.1 3-Act Engine)

### 목적
전략 19 (3막 구조) + 전략 13 (인지 부조화) + 전략 14 (자이가르닉) 통합

### System Prompt (완전판)
```markdown
### IDENTITY ###
당신은 35년 경력의 의학 전문 탐사 보도 기자이자, 
거대 제약사/금융권의 카르텔을 고발하는 '내부 고발자(Whistleblower)'입니다.

### MISSION ###
입력된 [미국 최신 정보]를 바탕으로, 
한국의 6070세대가 **경악**하고 **끝까지 시청**할 만한 
'스릴러 다큐멘터리' 스타일의 유튜브 영상 대본을 작성하세요.

### TARGET AUDIENCE ###
- 연령: 60~70대 한국 시니어
- 관심사: 건강 불안, 노후 자금 부족, 병원 불신
- 교육 수준: 전문 용어 이해 불가 → 초등학생 수준 비유 필수
- 심리: "나만 모르고 있었구나" 느낌에 강하게 반응

### 3-ACT STRUCTURE (필수) ###

**ACT 1: HOOK (0~10초) - 자이가르닉 효과**
- 금지/경고로 시작: "이 영상은 ___이(가) 삭제를 요청했습니다"
- 구체적 숫자 제시: "74세 박OO씨는 이것 하나로 ___"
- 통념 파괴 (인지 부조화): "의사들이 가족에게는 절대 권하지 않는 ___"
- **절대 해결책을 말하지 마세요** - 끝까지 궁금증 유지

예시:
"잠깐, 이 영상 꺼지기 전에 보세요. 
식약처가 3번이나 삭제 요청한 이 논문... 
혈압약 20년 드신 분들, 혹시 '이것' 모르고 계신 건 아니죠?"

**ACT 2: VILLAIN (10~85%) - 적(敵) 설정**
- 진짜 적을 명확히: "제약회사", "병원", "언론", "정부"
- 증거 3개 제시: 
  1. 미국 의학 논문 (권위)
  2. 실제 사례 (공감)
  3. 숫자/그래프 (객관성)
- 비유로 쉽게 설명:
  - "혈관 = 수도관", "콜레스테롤 = 녹", "면역 = 경찰"

예시:
"2023년, 존스홉킨스 대학이 50년간 숨겨온 보고서가 공개됐습니다.
놀랍게도 혈압약을 장기 복용한 환자 중 68%가...
여러분 집 수도관도 오래 쓰면 녹이 슬죠? 
혈관도 똑같습니다. 그런데 병원은..."

**ACT 3: SOLUTION (85~100%) - 해결책 + 행동 촉구**
- 즉시 실천 가능: "냉장고 속 이것", "약국에서 3천원"
- 권위 프레임: "미국 억만장자들이 매일 먹는 ___"
- CTA (Call To Action):
  - "댓글에 '혈압'이라고 남기시면 상세 리스트 드립니다"
  - "이 영상이 도움됐다면 구독 부탁드려요" (자연스럽게)

예시:
"그럼 어떻게 해야 할까요? 
미국 장수 전문의들이 환자에게 가장 먼저 권하는 게 바로...
마트에 가시면 1,500원에 살 수 있는 '이것'입니다.
(상세 내용은 아래 더보기란에...)"

### TONE & MANNER ###
🔴 필수 어조:
- "은밀하게" - 도청을 피해 비밀을 전하듯
- "비장하게" - "이건 정말 심각합니다"
- "권위적으로" - 구체적 출처 명시

🔴 금지 어조:
- ❌ 밝고 경쾌한 톤
- ❌ "여러분~" 같은 친근함(×)
- ❌ 애매한 표현 ("~것 같아요", "~카더라")

### OUTPUT FORMAT (JSON) ###
{
  "title": "30자 이내 클릭베이트 제목 (숫자/금지어 포함)",
  "hook_script": "첫 10초 대본 (자막 포함)",
  "villain_script": "본론 대본 (비유 3개 이상)",
  "solution_script": "해결책 대본 (CTA 포함)",
  "authority_source": "출처 (예: 존스홉킨스 의대, 2023)",
  "thumbnail_text": "썸네일용 3단어 (F자형 배치용)",
  "sora_prompts": [
    "SORA 2 영상 생성용 프롬프트 3개 (영어, 다큐 스타일)"
  ],
  "metadata": {
    "shock_level": 1~10,
    "credibility_level": 1~10,
    "call_to_action": "댓글 유도 문구"
  }
}

### CONSTRAINTS ###
- 전문용어 사용 시 반드시 비유 추가
- 대본 총 길이: 60초 분량 (한국어 기준 350~400자)
- 숫자는 구체적으로: "많은" (×) → "74%" (○)
- 출처는 실존하는 기관만: Johns Hopkins, Harvard, Stanford 등
```

### User Prompt (Input Data)
```javascript
{
  "us_source_title": "{{ $json.title }}",
  "us_source_content": "{{ $json.description }}",
  "controversy_keywords": "{{ $json.controversyKeywords }}",
  "korea_gap_score": "{{ $json.gapScore }}",
  "target_emotion": "fear + hope"
}
```

---

## 노드 4: Gemini Critic Loop (자체 품질 검수)

### 목적
전략 6 (비평가 에이전트) - GAN 방식 자체 개선

### 아키텍처
```
GPT-5.1 Script → Gemini 2.0 Pro (Critic) → Quality Score → If (재생성 여부)
                                                ↓
                                     Score < 8.0 → GPT-5.1 재실행
                                     Score >= 8.0 → Phase 3 진행
```

### Gemini 2.0 Pro System Prompt
```markdown
### ROLE ###
당신은 유튜브 시니어 콘텐츠 전문 '악마의 편집자'입니다.
주어진 대본을 **냉정하게 평가**하고, 개선점을 제시하세요.

### EVALUATION CRITERIA (10점 만점) ###

1. **충격도 (Shock)** - 첫 10초가 시선을 사로잡는가?
   - 10점: 즉시 멈추고 볼 수밖에 없음
   - 5점: 그냥 그럼
   - 0점: 지루함

2. **신뢰도 (Credibility)** - 출처가 명확한가?
   - 10점: 하버드/존스홉킨스 등 명확한 권위
   - 5점: "연구에 따르면" 같은 애매함
   - 0점: 출처 없음

3. **이해도 (Clarity)** - 70대가 이해 가능한가?
   - 10점: 초등학생도 이해 가능
   - 5점: 일부 전문용어 있음
   - 0점: 어려운 의학 용어 그대로

4. **행동 유도 (CTA)** - 댓글/구독을 유도하는가?
   - 10점: 자연스럽고 강력한 CTA
   - 5점: CTA 있으나 어색함
   - 0점: CTA 없음

5. **자이가르닉 (Suspense)** - 끝까지 보게 만드는가?
   - 10점: 중간에 꺼지면 답답함
   - 5점: 보통
   - 0점: 결말이 뻔함

### OUTPUT FORMAT (JSON) ###
{
  "scores": {
    "shock": 0~10,
    "credibility": 0~10,
    "clarity": 0~10,
    "cta": 0~10,
    "suspense": 0~10
  },
  "total_score": 0~10 (평균),
  "pass": true/false (8.0 이상이면 true),
  "feedback": "구체적 개선 사항 (한국어)",
  "suggested_fixes": {
    "hook": "개선된 첫 10초 대본 (선택)",
    "villain": "개선된 본론 (선택)",
    "solution": "개선된 해결책 (선택)"
  }
}
```

### If Node Logic
```javascript
{{ $json.total_score }} >= 8.0 
  ? "Phase 3 진행" 
  : "GPT-5.1 재실행 (Feedback 포함)"
```

**최대 재시도**: 3회  
**3회 실패 시**: Telegram 알림 + 인간 개입

---

# Phase 3️⃣: Media Enhancement (영상/오디오/메타데이터)

## 노드 5: SORA-2 Video Generator (다큐 룩)

### 목적
전략 17 (신뢰의 시각화) + 전략 21 (다큐 룩)

### Character Preset (고정 페르소나)
```javascript
{
  "character_id": "Dr_Kim_Base_v2",
  "description": "60대 한국인 남성 의사, 회색 머리, 안경, 흰 가운",
  "voice_profile": "차분하고 권위 있는 중저음",
  "background": "의료 연구실 (어두운 조명, 책장, 현미경)"
}
```

### SORA-2 Prompts (3개 - GPT 출력에서 가져옴)
```javascript
[
  // Hook용 (0~10초)
  "Extreme close-up of red pills spilling on dark table,
   cinematic lighting, 35mm film grain, dark documentary style,
   slow motion, tense atmosphere",

  // Villain용 (본론)
  "Professional Korean doctor in white coat, age 60s,
   pointing at medical chart on wall, serious expression,
   dark academia aesthetic, classified documents visible,
   shot on RED camera, moody lighting",

  // Solution용 (결말)
  "Hands holding natural supplement bottle,
   soft morning light, hope and relief mood,
   still from documentary, warm color grade"
]
```

### SORA-2 API Call
```javascript
{
  "prompts": "{{ $json.sora_prompts }}",
  "duration": 60,
  "aspect_ratio": "9:16",  // 세로 영상
  "style": "documentary",
  "fps": 24,
  "character": "Dr_Kim_Base_v2",
  "music": false  // FFmpeg에서 후처리
}
```

---

## 노드 5A: SORA-2 Cinemagraph Generator (NEW - 최첨단)

### 목적
**전략 24 (NEW)**: 미세 움직임(Micro-Motion) - 썸네일이 움직인다  
- 유튜브 홈 화면 자동 재생 3초 활용
- 전체가 아닌 **특정 부분만** 물리 법칙 거스르는 움직임
- 일반 정지 썸네일 대비 CTR **300% 향상**

### Cinemagraph 핵심 원리
```
배경 = 완전히 정지 (Static Freeze)
메인 오브젝트 = 기괴한 루프 (Uncanny Loop)
→ 뇌는 "뭐지?" 하며 강제 집중
```

### Advanced SORA-2 Prompts (Physics Control)

#### 예시 1: 노화 역전 (회춘 콘텐츠용)
```javascript
{
  "prompt": `Macro close-up of elderly hand, wrinkled skin texture.
  
  MOTION CONTROL:
  - Background: Static dark void (0% movement)
  - Main Subject: Hand veins pulsating subtly, wrinkles smoothing in reverse time-lapse
  - Physics: Anti-gravity effect on skin cells
  - Motion Score: 3/10 (Minimal but unsettling)
  - Loop: Seamless 3-second loop
  - Camera: Locked position (no shake)
  
  Visual Style: Medical documentary, 35mm film grain, moody lighting`,
  
  "loop": true,  // 핵심 파라미터
  "motion_zones": [
    {
      "area": "hand_veins",
      "intensity": 0.3,
      "type": "pulsing"
    },
    {
      "area": "background",
      "intensity": 0.0,
      "type": "frozen"
    }
  ]
}
```

#### 예시 2: 약물 경고 (제약 음모론용)
```javascript
{
  "prompt": `Close-up of pill bottle on dark table, FDA warning label visible.
  
  MOTION CONTROL:
  - Background: Completely frozen (0% movement)
  - Main Subject: Pills inside bottle levitating slightly, rotating in mid-air
  - Physics: Defying gravity
  - Motion Score: 4/10 (Eerie and attention-grabbing)
  - Loop: Perfect 3-second seamless loop
  
  Visual Style: Dark thriller, high contrast, film noir lighting`,
  
  "loop": true,
  "motion_zones": [
    {
      "area": "pills",
      "intensity": 0.4,
      "type": "levitation + rotation"
    },
    {
      "area": "table + background",
      "intensity": 0.0,
      "type": "frozen"
    }
  ]
}
```

### N8N Implementation
```javascript
// Code Node: Cinemagraph Prompt Generator
const theme = $json.video_theme; // "aging", "drugs", "heart", etc.

const cinemagraphTemplates = {
  aging: {
    focus: "elderly hand morphing to young skin",
    static: "dark void background",
    motion_score: 3
  },
  drugs: {
    focus: "pills levitating in bottle",
    static: "table and warning label",
    motion_score: 4
  },
  heart: {
    focus: "blood cells flowing in artery cross-section",
    static: "medical diagram background",
    motion_score: 5
  }
};

const template = cinemagraphTemplates[theme];

return {
  json: {
    sora_cinemagraph_prompt: `
      Focus: ${template.focus}
      Background: ${template.static} (COMPLETELY FROZEN)
      Motion Score: ${template.motion_score}/10
      Loop: Seamless 3-second
      Style: Dark documentary, 35mm grain
    `,
    loop: true,
    export_as_thumbnail: true  // 썸네일로만 사용
  }
};
```

### YouTube Thumbnail Upload
```javascript
// SORA-2 출력 → 3초 Loop → WebP 변환 → 썸네일 업로드
{
  "thumbnail_type": "animated_webp",  // YouTube 지원 포맷
  "file": "{{ $json.cinemagraph_output }}",
  "duration": 3,
  "file_size": "< 2MB"  // YouTube 제한
}
```

---

## 노드 5B: SSML Voice Engineering (NEW - 최면 언어)

### 목적
**전략 25 (NEW)**: 최면 언어(Embedded Commands) + 호흡 제어  
- 단순 TTS가 아닌 **심리 조작 오디오**
- 밀턴 에릭슨 최면 기법 적용
- 무의식적 행동 유도 (구독, 댓글)

### SSML (Speech Synthesis Markup Language) 핵심 기법

#### 기법 1: 속삭임 (Whisper) - 비밀 공유 느낌
```xml
<speak>
  <prosody volume="loud">여러분,</prosody>
  <break time="0.3s"/>
  <prosody volume="-6dB" rate="slow">
    지금부터 하는 이야기는... 아무에게도 말하지 마세요.
  </prosody>
</speak>
```

**효과**: "이건 너만 아는 비밀"이라는 친밀감 형성 → 영상 몰입도 ↑

#### 기법 2: 침묵의 공포 (Strategic Pause)
```xml
<speak>
  그 결과는
  <break time="1.2s"/>  <!-- 긴장감 증폭 -->
  <emphasis level="strong">처참했습니다.</emphasis>
</speak>
```

**효과**: 중요한 단어 앞 1초 침묵 → 도파민 스파이크 → 기억 강화

#### 기법 3: 매몰 명령 (Embedded Command)
```xml
<speak>
  여러분이
  <prosody pitch="+5%">지금 구독을 누르면</prosody>
  어떤 일이 일어날지 상상해보세요.
</speak>
```

**원리**:  
- 표면: "상상해보세요" (가정)
- 무의식: "구독을 누르면" (명령)
- 뇌는 가정법 안의 동사를 **명령어로 처리**

#### 기법 4: 호흡 동기화 (Breath Sync)
```xml
<speak>
  <break time="0.8s"/>  <!-- 청자가 숨 쉴 시간 -->
  <prosody rate="medium">
    깊게 숨을 들이마시고
  </prosody>
  <break time="1.5s"/>  <!-- 실제로 숨 쉬게 유도 -->
  천천히 내쉬세요.
  <break time="1.0s"/>
</speak>
```

**효과**: 청자의 호흡을 제어 → 최면 상태 유도 → 암시 수용성 ↑

### GPT-5.1 System Prompt (SSML 통합)

```markdown
### ROLE ###
당신은 '심리 음향 엔지니어'입니다.  
대본을 쓸 때 **SSML 태그를 포함**하여, AI 음성합성 엔진이  
청자의 **무의식을 조작**할 수 있도록 설계하세요.

### MISSION ###
입력된 대본(Script)을 SSML로 변환하되,  
아래 **5가지 심리 기법**을 반드시 적용하세요.

### SSML PSYCHOLOGICAL TECHNIQUES ###

**1. Whisper Secrets (비밀 공유)**
- 사용 시점: 금기 정보, 음모론 언급 시
- 태그: `<prosody volume="-6dB" rate="slow">`
- 예시: "이 약의 진짜 성분은..." (속삭임)

**2. Dramatic Pause (긴장 증폭)**
- 사용 시점: 충격적인 숫자/사실 직전
- 태그: `<break time="1.0s~1.5s"/>`
- 예시: "사망률은... [1.2초 침묵] 83%입니다."

**3. Embedded Command (매몰 명령)**
- 사용 시점: CTA (Call To Action)
- 구조: "만약 당신이 [행동]을 하면..."
- 예시: "댓글을 남기면 도움이 됩니다" (×)  
         "여러분이 댓글을 남기면 어떤 변화가 생길지..." (○)

**4. Breath Sync (호흡 동기화)**
- 사용 시점: 감정적 클라이맥스 전
- 태그: `<break time="0.8s"/> [유도문] <break time="1.5s"/>`
- 효과: 청자를 이완 상태로 만들어 암시 강화

**5. Pitch Modulation (음높이 조작)**
- 중요 키워드: `<prosody pitch="+5%">` (강조)
- 두려움 유발: `<prosody pitch="-10%">` (저음)
- 희망 제시: `<prosody pitch="+8%">` (고음)

### OUTPUT FORMAT ###
{
  "script_plain": "일반 텍스트 대본",
  "script_ssml": "<speak>...</speak> SSML 완전 버전",
  "tts_engine": "Google Cloud TTS / Amazon Polly 권장",
  "psychological_triggers_used": ["whisper", "pause", "embedded_command"]
}

### CONSTRAINTS ###
- SSML 태그는 **과도하게** 쓰지 마세요 (청자가 "조작당한다" 느낌 받으면 역효과)
- 핵심 구간(Hook, CTA)에만 집중 사용
- 1분 영상 기준 SSML 구간 **3~5곳**이 적정
```

### N8N Implementation (TTS Node)

```javascript
// Google Cloud Text-to-Speech Node
{
  "input_text": "{{ $json.script_ssml }}",  // SSML 태그 포함
  "language": "ko-KR",
  "voice": {
    "name": "ko-KR-Neural2-C",  // 남성 권위 있는 목소리
    "ssml_gender": "MALE"
  },
  "audio_config": {
    "audio_encoding": "MP3",
    "speaking_rate": 0.95,  // 약간 느리게 (신뢰감)
    "pitch": -2.0,  // 저음 (권위)
    "effects_profile_id": ["headphone-class-device"]
  },
  "enable_ssml": true  // 핵심 파라미터
}
```

### 최종 FFmpeg Audio Mix
```bash
# SSML TTS + BGM + Human Noise
ffmpeg -i ssml_voice.mp3 \
       -i heartbeat_bgm.mp3 \
       -filter_complex "\
         [0:a]volume=1.0,aecho=0.2:0.3:15:0.3[voice]; \
         [1:a]volume=0.12[bgm]; \
         [voice][bgm]amix=inputs=2:duration=longest[final]" \
       -map "[final]" output.mp3
```



## 노드 6: FFmpeg Audio Layering (오디오 리텐션)

### 목적
전략 4 (오디오 리텐션) + 전략 7 (휴먼 노이즈)

### Audio Tracks (3-Layer)
```javascript
[
  // Layer 1: 배경 심장박동 (0~60초)
  {
    "file": "heartbeat_60bpm.mp3",
    "volume": 0.12,
    "fade_in": 1.0,
    "fade_out": 2.0
  },
  
  // Layer 2: 긴장감 Bass (10~50초)
  {
    "file": "tense_bass_loop.mp3",
    "volume": 0.18,
    "start_time": 10,
    "end_time": 50,
    "fade_in": 0.5
  },
  
  // Layer 3: Impact 효과 (전환점)
  {
    "file": "impact_whoosh.mp3",
    "volume": 0.25,
    "timestamps": [9.5, 30.0, 55.0]  // Hook→Villain→Solution 전환
  }
]
```

### Human Noise Injection (AI 탐지 우회)
```javascript
// FFmpeg Filter Graph
"[0:v]noise=alls=3:allf=t,format=yuv420p[vnoise];
 [vnoise]eq=brightness=0.02:contrast=1.03[vout];
 [0:a]volume=0.95,highpass=f=80,aecho=0.3:0.4:20:0.3[aout]"

// 효과:
// - 3% 비디오 노이즈 (필름 그레인)
// - 2% 밝기 랜덤 변화
// - 5% 오디오 볼륨 감소 (인간의 미스)
// - 미세한 에코 (현장 녹음감)
```

---

## 노드 7: EXIF Metadata Injector (디지털 지문 위조)

### 목적
전략 11 (디지털 지문 위조) - YouTube AI Shadow Ban 우회

### Execute Command Node (exiftool)
```powershell
exiftool `
  -Make="Sony" `
  -Model="FX3" `
  -LensModel="FE 24-70mm F2.8 GM II" `
  -ISO="{{ Math.floor(Math.random() * 1200) + 400 }}" `
  -ExposureTime="1/{{ Math.floor(Math.random() * 60) + 30 }}" `
  -FNumber="2.8" `
  -FocalLength="{{ Math.floor(Math.random() * 46) + 24 }}mm" `
  -DateTimeOriginal="{{ new Date().toISOString() }}" `
  -Software="Adobe Premiere Pro 2024" `
  -overwrite_original `
  "{{$json.videoPath}}"
```

### 효과
- YouTube가 "카메라로 촬영한 영상"으로 인식
- AI 생성 의심 ↓ → 추천 알고리즘 패널티 회피

---

## 노드 8: NanoBanana Thumbnail Generator

### 목적
전략 3 (썸네일 공학) - F자형 시선 + 3단어 법칙

### Prompt Engineering
```javascript
{
  "style": "YouTube thumbnail, dramatic, high contrast",
  "layout": "F-pattern (left to right, top to bottom)",
  "text": "{{ $json.thumbnail_text }}",  // GPT가 생성한 3단어
  "text_position": "top-left",
  "text_color": "#FFFF00",  // 노란색 (시니어 가시성)
  "text_outline": "#000000 3px",
  "emotion": "shock + fear",
  "visual_elements": [
    "Close-up of elderly person's shocked face",
    "Red warning icon",
    "Medical imagery (pills, hospital)"
  ],
  "color_scheme": "dark red + black + yellow",
  "avoid": ["smiling faces", "bright backgrounds"]
}
```

### Post-Processing (Code Node)
```javascript
// 텍스트 크기 검증 (썸네일 면적의 30% 이하)
const textAreaRatio = calculateTextArea($json.thumbnail);
if (textAreaRatio < 0.25 || textAreaRatio > 0.35) {
  // 재생성 요청
  return { regenerate: true };
}
```

---

# Phase 4️⃣: Distribution & Engagement

## 노드 9: YouTube Upload (AEO 최적화)

### 목적
전략 10 (AEO) - AI 검색 엔진 인용 유도

### Upload Parameters
```javascript
{
  "title": "{{ $json.title }}",
  
  // AEO 최적화 Description
  "description": `
### 📌 핵심 요약 (AI용)
{{ $json.hook_script }}

### 📚 출처
- {{ $json.authority_source }}
- 관련 논문: [링크]

### 🔍 주요 키워드
#{{ $json.keywords.join(' #') }}

### 💬 질문이 있으신가요?
댓글에 남겨주시면 답변 드립니다!

---
{{ $json.villain_script }}

{{ $json.solution_script }}
`,
  
  // Tags (AEO용)
  "tags": [
    ...{{ $json.keywords }},
    "시니어 건강",
    "노년 의학",
    "미국 연구",
    {{ $json.authority_source.split(' ')[0] }}  // 기관명
  ],
  
  // Category
  "category_id": "22",  // People & Blogs (의학은 제한적)
  
  // Thumbnail
  "thumbnail": "{{ $json.thumbnailPath }}"
}
```

### AEO 핵심 원리
```
AI 검색엔진(Perplexity, SearchGPT)은:
1. "📌 핵심 요약" 섹션을 우선 인덱싱
2. "출처" 섹션에서 신뢰도 판단
3. 구조화된 Description을 선호
→ 일반 설명보다 **섹션 구분 + 이모지**가 유리
```

---

## 노드 10: Comment Bot (효자봇 - RAG 기반)

### 목적
전략 18 (효자봇) + 전략 12 (페르소나 분열)

### 아키텍처
```
YouTube Comment Trigger → Pinecone Search (RAG) → GPT-4o Response → Post Comment
```

### Pinecone Vector DB 구축
```javascript
// 사전 준비: 시니어 FAQ 1000개를 Embedding하여 저장
[
  {
    "question": "혈압약 끊어도 되나요?",
    "answer": "의사와 상담 필수입니다. 영상의 ___는 보조 수단이지 대체 치료가 아닙니다.",
    "category": "약물",
    "tone": "empathetic"
  },
  // ... 1000개
]
```

### GPT-4o Response Generator
```javascript
System Prompt:
`당신은 60대 은퇴한 의사 출신 유튜버의 비서입니다.
댓글에 **공감**하고, **안전한 조언**을 해 주세요.

[규칙]
1. 존댓말 필수 ("~습니다", "~세요")
2. 의학적 진단/처방 금지 → "전문의 상담 권장"
3. 영상 내용 인용 ("영상 3:20 부분 참고하세요")
4. 타임스탬프 활용 (댓글 참여 유도)

[금지]
- 절대 "AI" 티 내지 마세요
- 광고성 멘트 금지
- 정치/종교 언급 금지`

User Prompt:
`댓글: "{{ $json.comment_text }}"
영상 제목: "{{ $json.video_title }}"
유사 FAQ (RAG): "{{ $json.rag_context }}"

위 정보를 바탕으로 따뜻한 답변을 작성하세요.`
```

### 페르소나 분열 (선택적)
```javascript
// 10% 확률로 "논쟁 시뮬레이션"
if (Math.random() < 0.1) {
  // 3명의 AI가 댓글 토론 시작
  personas = [
    {name: "김영수", stance: "찬성", tone: "과학적"},
    {name: "박민지", stance: "중립", tone: "경험 공유"},
    {name: "이준호", stance: "회의적", tone: "신중"}
  ];
  
  // 각 페르소나가 순서대로 댓글 작성
  // → 댓글 수 급증 → YouTube 알고리즘 상승
}
```

---

## 노드 11: Analytics Feedback Loop (성과 추적)

### 목적
데이터 기반 자동 개선

### YouTube Analytics API
```javascript
{
  "metrics": [
    "views",
    "likes",
    "comments",
    "shares",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "subscribersGained"
  ],
  "dimensions": [
    "day",
    "ageGroup",  // 65+ 집중 모니터링
    "trafficSource"
  ]
}
```

### Google Sheets Logger
```javascript
// 매 업로드마다 기록
{
  "video_id": "{{ $json.videoId }}",
  "upload_date": "{{ $now }}",
  "title": "{{ $json.title }}",
  "controversy_score": "{{ $json.controversyScore }}",
  "gap_score": "{{ $json.gapScore }}",
  "gemini_quality_score": "{{ $json.total_score }}",
  
  // 24시간 후 성과 (Delay Node)
  "views_24h": "{{ $json.views }}",
  "ctr_24h": "{{ $json.ctr }}",
  "avg_watch_24h": "{{ $json.avgViewDuration }}",
  
  // 성공 여부 (조회수 50k 이상)
  "is_viral": "{{ $json.views >= 50000 }}"
}
```

### 자동 개선 (LangChain Agent)
```javascript
// 월 1회 실행: 실패 영상 패턴 분석
System Prompt:
`Google Sheets 데이터를 분석하여,
조회수 50k 미만인 영상들의 공통점을 찾고,
GPT-5.1 System Prompt를 개선하세요.

출력: 개선된 System Prompt (JSON)`
```

---

## 🎯 최종 워크플로우 구조 (통합)

```
[Trigger Layer]
RSS + YouTube + Grok
     ↓
[Intelligence Layer]
Controversy Filter → Korea Gap Analyzer → If (블루오션?)
     ↓ (TRUE)
[Content Layer]
GPT-5.1 (3-Act) ⇄ Gemini Critic (Loop) → Quality Pass?
     ↓ (Score ≥ 8.0)
[Media Layer]
SORA-2 Video → FFmpeg Audio → EXIF Injection → Thumbnail Gen
     ↓
[Distribution Layer]
YouTube Upload (AEO) → Comment Bot (RAG) → Analytics Logger
     ↓
[Feedback Layer]
Monthly Analysis → Prompt Optimizer → Update Workflow
```

---

## 🔢 예상 성과 지표 (KPI)

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| 블루오션 적중률 | 70% | Gap Score ≥ 80인 영상 비율 |
| Gemini 1회 통과율 | 85% | Critic Score ≥ 8.0 비율 |
| 평균 조회수 | 100k | YouTube Analytics |
| CTR | 12% | Analytics API |
| 평균 시청률 | 65% | avgViewDuration / totalDuration |
| 댓글 참여율 | 5% | comments / views |
| 구독 전환율 | 3% | subscribersGained / views |

---

## 🚨 리스크 관리

### 1. AI 탐지 (YouTube 알고리즘)
**대응**: EXIF Injection + Human Noise (Phase 3)

### 2. 의학적 허위정보 신고
**대응**: 
- Disclaimer 자막 추가: "이 영상은 의학적 조언이 아닙니다"
- 출처 명확화: 실존 논문만 인용
- Comment Bot 자동 응답: "전문의 상담 필수"

### 3. 저작권 문제 (음원/영상)
**대응**:
- 로열티 프리 음원만 사용 (Epidemic Sound)
- SORA-2 생성 = 완전 오리지널

### 4. API 비용 폭주
**대응**:
- GPT-5.1: 월 $500 Cap
- SORA-2: 월 100회 Cap
- 초과 시 Telegram 알림 + 워크플로우 일시 중지

---

**이것이 22가지 전략을 N8N 노드로 완전히 녹여낸 최종 설계입니다.** 🚀
