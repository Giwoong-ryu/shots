# Implementation Plan - v7.5 ULTIMATE (Sora-2 Edition)

## Goal Description
Implement the **Definitive v7.5 Workflow** using **Sora-2 (Image-to-Video)** as the core engine.
### Manual Verification
-   **Consistency Check**: Generate 3 consecutive shots using the same "Anchor Image". Verify the character remains recognizable.

### 4. Audio Layer (The Soul)
# Implementation Plan - v7.5 ULTIMATE (Sora-2 Edition)

## Goal Description
Implement the **Definitive v7.5 Workflow** using **Sora-2 (Image-to-Video)** as the core engine.
### Manual Verification
-   **Consistency Check**: Generate 3 consecutive shots using the same "Anchor Image". Verify the character remains recognizable.

### 4. Audio Layer (The Soul)
-   **[KEEP]** `GPT-4o Audio` + `OpenAI TTS`.

### 5. Content Layer (The Persona) - **CRITICAL FIX**
-   **Problem**: Current v7 JSON is set to "AI News" (Mark Zuckerberg examples).
-   **Fix**: Rewrite all System Prompts to "Senior Health / Heaven & Hell".
-   **Source**: `Shorts_NextLevel_v7_Phase1.json` (Found exact prompts).
-### 6. Strategy Layer (The "Opal" System) - **FINALIZED**
-   **Concept**: Convert the "Google Opal 11 Agents" model into a streamlined **n8n Agent Swarm**.
-   **The Swarm Architecture**:
    1.  **Agent 1: Trend Researcher (The Scout)**
        -   *Role*: "Find what seniors are clicking *now*."
# Implementation Plan - v7.5 ULTIMATE (Sora-2 Edition)

## Goal Description
Implement the **Definitive v7.5 Workflow** using **Sora-2 (Image-to-Video)** as the core engine.
### Manual Verification
-   **Consistency Check**: Generate 3 consecutive shots using the same "Anchor Image". Verify the character remains recognizable.

### 4. Audio Layer (The Soul)
# 구현 계획 - v7.5 ULTIMATE (Sora-2 에디션)

## 목표 설명
**Sora-2 (Image-to-Video)**를 핵심 엔진으로 사용하는 **결정판 v7.5 워크플로우**를 구현합니다.

## 사용자 검토 필요 (중요)
> [!IMPORTANT]
> **Sora-2 비용 알림**: Sora-2는 프리미엄 모델입니다. 테스트 중 비용을 아끼기 위해 처음에는 `Kling v2`나 `NanoBanana`를 사용할 수 있지만, 최종 품질을 위해 Sora-2로 전환할 것입니다.

## 제안된 변경 사항

### 1. 비디오 레이어 (The Engine) - **핵심 변경**
-   **[삭제]** `Sora-2 (OpenAI)` 플레이스홀더 노드.
-   **[신규]** **직접 OpenAI 폴링 루프 (Direct OpenAI Polling Loop)** (4개 노드):
    1.  `HTTP Request`: POST /v1/videos (생성 시작).
    2.  `Wait`: 30초 대기.
    3.  `HTTP Request`: GET /v1/videos/{id} (상태 확인).
    4.  `If`: 완료될 때까지 루프.
-   **모델 ID**: `sora-2-preview` (또는 현재 활성 ID).
-   **입력**: `image_url` (캐릭터 일관성을 위해 필수).

### 2. 이미지 레이어 (The Face)
-   **[유지]** `NanoBanana Pro` (Fal.ai).
-   **설정**: 텍스트 렌더링 기능 활용 (예: "WARNING" 텍스트가 적힌 HUD).

### 3. 수동 검증
-   **일관성 체크**: 동일한 "앵커 이미지"를 사용하여 3개의 연속 샷을 생성. 캐릭터가 인식 가능한지 확인.

### 4. 오디오 레이어 (The Soul)
-   **[유지]** `GPT-4o Audio` + `OpenAI TTS`.

### 5. 콘텐츠 레이어 (The Persona) - **중요 수정**
-   **문제점**: 현재 v7 JSON은 "AI 뉴스" (마크 저커버그 예시)로 설정되어 있음.
-   **수정**: 모든 시스템 프롬프트를 "시니어 건강 / 천국과 지옥"으로 다시 작성.
-   **소스**: `Shorts_NextLevel_v7_Phase1.json` (정확한 프롬프트 발견됨).

### 6. 전략 레이어 ("Opal" 시스템) - **확정됨**
-   **개념**: "구글 Opal 11 에이전트" 모델을 간소화된 **n8n 에이전트 스웜(Swarm)**으로 변환.
-   **스웜 아키텍처**:
    1.  **에이전트 1: 트렌드 연구원 (정찰병)**
        -   *역할*: "시니어들이 *지금* 클릭하는 것을 찾아라."
        -   *도구*: 구글 트렌드 / 유튜브 검색 (Apify 또는 시뮬레이션).
        -   *목표*: 관심도 높은 주제 식별 (예: "마그네슘 결핍").
    2.  **에이전트 1.5: 경쟁자 정찰병 (검증)**
        -   *역할*: "Playboard.co 데이터 확인."
        -   *로직*: "비슷한 채널이 어제 성장했는가?" (일일 구독자 증가 > 500).
    3.  **에이전트 2: 키워드 분석가 (전략가)**
        -   *역할*: "왜 작동하는지 분석하라."
        -   *로직*: "공포 포인트" vs "희망 포인트"에 대한 딥러닝 분석.
        -   *출력*: "훅" 앵글 (예: "이 증상을 무시하지 마세요").
    4.  **에이전트 3: 콘텐츠 기획자 (감독)**
        -   *역할*: "영상 구조화."
        -   *포맷*: **"교육용 영상" (유형 3)** - 1분, 명확한 메시지.
        -   *구조*: "천국과 지옥" 분할 화면.
    5.  **에이전트 4: 메타데이터 전문가 (마케터)**
        -   *역할*: "SEO & 클릭률."
        -   *제목*: 60자 미만, 키워드 전진 배치.
        -   *설명*: 첫 150자 최적화.
        -   *태그*: 광범위(건강)와 구체적(마그네슘) 태그 혼합.
    6.  **에이전트 5: 글로벌 확장 (현지화 담당)**
        -   *역할*: "일본 시장 적응."
        -   *로직*: "부드러운 훅" (공손함) + "전통 지혜" (주제 변경).

### 7. 콘텐츠 레이어 ("고해상도" 영혼)
-   **소스**: `shots/쇼츠_고급.json` (상세한 "시스템 프롬프트" 복원).
-   **적응**:
    -   **페르소나**: "보람" (전문 건강 가이드).
    -   **시각 스타일**: "초현실적", "의료 HUD", "영화 같은 조명" 키워드 복원.
    -   **QoE (경험 품질)**: "시작 시간" (훅)이 즉각적(0-3초)이도록 보장.

## 4. 실행 단계

### 1단계: "Sora-2" 수술 (엔진)
*   **대상**: `Shorts_NextLevel_v7_ULTIMATE.json`
*   **조치**: 직접 OpenAI Sora-2를 위한 4노드 폴링 루프 주입.

### 2단계: "Opal" 주입 (두뇌)
*   **대상**: 워크플로우 시작 부분.
*   **조치**: **연구 -> 경쟁자 -> 분석 -> 기획 -> 현지화** 체인 구현.
    *   *참고*: `PROTOCOL_OPAL.md`에 정의된 특정 페르소나를 가진 `n8n AI Agent` 노드 사용.

### 3단계: "고해상도" 복원 (영혼)
*   **대상**: 생성 노드.
*   **조치**:
    1.  `shots/쇼츠_고급.json`에서 상세 프롬프트 추출.
    2.  "시니어 건강" 주제와 "Opal" SEO 규칙으로 다듬기.
    3.  v7.5에 주입.

### 4단계: 최종 마무리
*   **조치**: `Shorts_NextLevel_v7_5_ULTIMATE.json`으로 저장.
*   **문서**: 설정 가이드 업데이트.

## 5. 리스크 평가 (일본 시장)
*   **저작권**: 일본은 "공정 이용"이 없음. **완화책**: 100% AI 생성 비주얼(Sora-2/NanoBanana) 사용. 스톡 클립 금지.
*   **어조**: 한국식 "충격" 스타일은 무례함. **완화책**: 에이전트 5가 "공손함 필터" (부드러운 훅) 적용.
*   **포화도**: 일본은 덜 포화되었지만 진입이 어려움. **완화책**: 일반적인 건강 팁보다는 "전통 지혜" (예: 낫토, 라디오 체조) 타겟팅.
