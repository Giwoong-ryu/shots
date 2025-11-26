# 🧠 INTELLIGENCE ENGINE: Integration Guide

> **목표**: `Intelligence_Engine_v1.json` (뇌)을 `Shorts_NextLevel_v8.json` (몸)에 연결하여 완전 자동화를 달성합니다.

---

## 1. 설치 및 설정 (Setup)

### 1.1. Import
1.  N8N 대시보드에서 `Import from File` 클릭.
2.  `shots/Intelligence_Engine_v1.json` 파일 선택.
3.  워크플로우가 로드되면 **"Intelligence_Engine_v1"**이라는 이름으로 저장.

### 1.2. Credentials (자격 증명)
이 워크플로우는 실제 데이터를 긁어오기 위해 API 키가 필요합니다.

*   **Reddit Node**:
    *   `Credential Type`: **Reddit OAuth2 API**.
    *   `Client ID` / `Secret`: Reddit Apps(https://www.reddit.com/prefs/apps)에서 생성 (Script App).
    *   *팁*: 귀찮으면 일단 `Reddit Scraper` 노드를 비활성화하고 수동 입력으로 테스트하세요.

*   **YouTube Node**:
    *   `Credential Type`: **YouTube OAuth2 API**.
    *   `API Key`: Google Cloud Console에서 생성.

---

## 2. 메인 워크플로우와 연결 (Integration)

### 2.1. 방법 A: "Execute Workflow" 노드 사용 (추천)
메인 워크플로우(`Shorts_NextLevel_v8`)를 엽니다.

1.  **시작점 찾기**: `Manual Trigger`와 `Define Search Topic1` 사이.
2.  **노드 추가**: `Execute Workflow` 노드를 추가합니다.
3.  **설정**:
    *   `Source`: **Database**.
    *   `Workflow`: **Intelligence_Engine_v1** 선택.
4.  **연결**:
    *   `Manual Trigger` -> `Execute Workflow` -> `Define Search Topic1`.
5.  **데이터 매핑**:
    *   `Define Search Topic1` 노드를 엽니다.
    *   `search_topic` 값을 지우고, `Execute Workflow`에서 나온 `trend_report` 값을 드래그 앤 드롭합니다.

### 2.2. 방법 B: "수동 복사" (간편)
1.  `Intelligence_Engine_v1`을 먼저 실행합니다.
2.  결과(`trend_report`)를 복사합니다.
3.  메인 워크플로우의 `Define Search Topic1` 노드에 붙여넣습니다.

---

## 3. 기대 효과 (Expected Outcome)

*   **Before**: "요즘 뜨는 거 뭐 있지?" (구글 검색 30분)
*   **After**: 버튼 하나 누르면 **"이번 주 레딧/유튜브 통합 보고서"**가 생성되고, Agent 0이 이를 분석하여 **"지금 당장 해야 할 주제"**를 선정합니다.

---

**[Next Step]**
이제 모든 준비가 끝났습니다.
1.  **Phase 1**: 프롬프트 이식 (완료).
2.  **Phase 2**: 지능 엔진 장착 (완료).
3.  **Phase 3**: **"Run"** 버튼을 누르고 결과를 지켜보세요. 🚀
