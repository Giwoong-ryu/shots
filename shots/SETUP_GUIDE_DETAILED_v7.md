# 📋 Shorts NextLevel v7 ULTIMATE - 상세 설정 가이드

## 목차
1. [Google Sheets 설정](#1-google-sheets-설정)
2. [YouTube 계정 설정](#2-youtube-계정-설정)
3. [Google Drive 폴더 구조](#3-google-drive-폴더-구조)
4. [n8n Credential 설정](#4-n8n-credential-설정)
5. [워크플로우 테스트](#5-워크플로우-테스트)

---

## 1. Google Sheets 설정

### 1-1. 새 스프레드시트 생성

1. **[Google Sheets](https://sheets.google.com/) 접속**
2. **"빈 스프레드시트"** 클릭
3. 제목을 **"YouTube Shorts Automation"**으로 변경

### 1-2. 시트 구조 설정

**Sheet1** (메인 로그 시트)에 다음 **헤더 행** 추가:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| row_number | timestamp | topic | narration | script_generated | video_url | youtube_url | status |

#### 각 열 설명:
- **row_number**: 자동 생성되는 행 번호
- **timestamp**: 생성 시간
- **topic**: 영상 주제
- **narration**: 생성된 나레이션 스크립트
- **script_generated**: 스크립트 생성 완료 여부 (TRUE/FALSE)
- **video_url**: 생성된 비디오 파일 URL
- **youtube_url**: 업로드된 YouTube 링크
- **status**: 진행 상태 (processing/completed/failed)

### 1-3. 스프레드시트 ID 복사

1. 스프레드시트 URL 확인:
   ```
   https://docs.google.com/spreadsheets/d/1AyIUgp55Rr88R5KMGvkBfMLCucWXsT0_AjhaLhV-_J8/edit
   ```

2. **스프레드시트 ID** 복사:
   ```
   1AyIUgp55Rr88R5KMGvkBfMLCucWXsT0_AjhaLhV-_J8
   ```
   (URL의 `/d/` 와 `/edit` 사이 부분)

### 1-4. 공유 설정

1. 우측 상단 **"공유"** 버튼 클릭
2. **"일반 액세스"** → **"링크가 있는 모든 사용자"** 선택
3. 권한: **"편집자"** 선택
4. **"완료"** 클릭

---

## 2. YouTube 계정 설정

### 2-1. YouTube 채널 생성 (없는 경우)

1. **[YouTube Studio](https://studio.youtube.com/) 접속**
2. 채널이 없다면 **"채널 만들기"** 클릭
3. 채널 이름 입력 (예: "AI 뉴스 쇼츠")
4. **"만들기"** 클릭

### 2-2. YouTube Data API v3 활성화

1. **[Google Cloud Console](https://console.cloud.google.com/) 접속**
2. 프로젝트 선택 또는 새로 생성
3. **"API 및 서비스"** → **"라이브러리"** 클릭
4. **"YouTube Data API v3"** 검색
5. **"사용 설정"** 클릭

### 2-3. OAuth 2.0 클라이언트 ID 생성

1. **"API 및 서비스"** → **"사용자 인증 정보"** 클릭
2. **"사용자 인증 정보 만들기"** → **"OAuth 클라이언트 ID"** 선택
3. 애플리케이션 유형: **"웹 애플리케이션"** 선택
4. 이름: **"n8n YouTube Upload"**
5. **승인된 리디렉션 URI** 추가:
   ```
   https://your-n8n-instance.com/rest/oauth2-credential/callback
   ```
   (n8n 인스턴스 URL로 변경)
6. **"만들기"** 클릭
7. **클라이언트 ID**와 **클라이언트 보안 비밀** 복사 및 저장

### 2-4. n8n에서 YouTube OAuth2 Credential 생성

1. n8n → **Settings** → **Credentials** → **Add Credential**
2. **"Google OAuth2 API"** 선택
3. 다음 정보 입력:
   - **Client ID**: 위에서 복사한 클라이언트 ID
   - **Client Secret**: 위에서 복사한 클라이언트 보안 비밀
   - **Scope**: `https://www.googleapis.com/auth/youtube.upload`
4. **"Connect my account"** 클릭
5. Google 계정으로 로그인 및 권한 승인
6. **"Save"** 클릭

### 2-5. YouTube 업로드 기본 설정

**YouTube Upload (KR)** 노드에서 설정:

#### 기본 설정:
- **Title**: `{{ $json.title }}` (메타데이터에서 자동 생성)
- **Description**: `{{ $json.description }}`
- **Tags**: `{{ $json.tags }}`
- **Category**: `22` (People & Blogs) 또는 `25` (News & Politics)
- **Privacy Status**: `private` (초기 테스트) → `public` (실제 운영)
- **Region Code**: `KR` (한국)

#### 고급 설정 (선택):
- **Made for Kids**: `false`
- **Self Declared Made for Kids**: `false`
- **Embeddable**: `true`
- **Public Stats Viewable**: `true`
- **Notify Subscribers**: `false` (초기 테스트 시)

---

## 3. Google Drive 폴더 구조

### 3-1. 폴더 생성

**[Google Drive](https://drive.google.com/)** 에서 다음 폴더 구조 생성:

```
📁 YouTube Shorts Automation/
├── 📁 1_Scripts/          (생성된 스크립트 저장)
├── 📁 2_Images/           (생성된 이미지 저장)
├── 📁 3_Videos/           (생성된 비디오 저장)
├── 📁 4_Audio/            (TTS 오디오 저장)
├── 📁 5_Subtitles/        (자막 파일 저장)
└── 📁 6_Final_Videos/     (최종 합성 비디오)
```

### 3-2. 폴더 ID 복사

각 폴더의 **폴더 ID** 복사:

1. 폴더 열기
2. URL 확인:
   ```
   https://drive.google.com/drive/folders/1_Y0Qcp-clH_8GX65U4IjODANTL2tLO7A
   ```
3. **폴더 ID** 복사:
   ```
   1_Y0Qcp-clH_8GX65U4IjODANTL2tLO7A
   ```

### 3-3. 공유 설정

각 폴더에 대해:
1. 우클릭 → **"공유"**
2. **"링크가 있는 모든 사용자"** → **"편집자"**
3. **"완료"**

---

## 4. n8n Credential 설정

### 4-1. OpenAI API

1. **[OpenAI Platform](https://platform.openai.com/api-keys) 접속**
2. **"Create new secret key"** 클릭
3. 이름: **"n8n Shorts Automation"**
4. API 키 복사 (예: `sk-proj-...`)
5. n8n에서:
   - Credential Type: **"OpenAI API"**
   - API Key: 복사한 키 입력

### 4-2. Google Service Account (Vertex AI)

1. **[Google Cloud Console](https://console.cloud.google.com/) 접속**
2. **"IAM 및 관리자"** → **"서비스 계정"**
3. 기존 서비스 계정 선택 또는 새로 생성
4. **"키"** 탭 → **"키 추가"** → **"JSON"**
5. JSON 파일 다운로드
6. n8n에서:
   - Credential Type: **"Google Service Account API"**
   - Region: **"Asia Pacific (Seoul) - asia-northeast3"**
   - Service Account Email: JSON의 `client_email`
   - Private Key: JSON의 `private_key` (전체 복사)

### 4-3. Google OAuth2 (Sheets, Drive, YouTube)

1. n8n → **Add Credential** → **"Google OAuth2 API"**
2. **Client ID**와 **Client Secret** 입력 (위에서 생성한 것)
3. **Scope** 추가:
   ```
   https://www.googleapis.com/auth/spreadsheets
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/youtube.upload
   ```
4. **"Connect my account"** 클릭
5. Google 계정 로그인 및 권한 승인

---

## 5. 워크플로우 테스트

### 5-1. 테스트 데이터 준비

Google Sheets의 **첫 번째 데이터 행**에 입력:

| row_number | timestamp | topic | narration | script_generated | video_url | youtube_url | status |
|------------|-----------|-------|-----------|------------------|-----------|-------------|--------|
| 1 | | 커피에 설탕을 넣으면 안 되는 이유 | | FALSE | | | pending |

### 5-2. 워크플로우 실행

1. n8n에서 **"Execute Workflow"** 클릭
2. 또는 **Webhook** 노드를 통해 수동 트리거:
   ```bash
   curl -X POST https://your-n8n-instance.com/webhook/shorts-automation \
     -H "Content-Type: application/json" \
     -d '{"row_number": 1, "topic": "커피에 설탕을 넣으면 안 되는 이유"}'
   ```

### 5-3. 진행 상황 모니터링

1. **n8n 실행 로그** 확인
2. **Google Sheets** 업데이트 확인:
   - `script_generated`: TRUE로 변경
   - `narration`: 생성된 스크립트 입력
   - `status`: processing → completed
3. **Google Drive** 폴더에 파일 생성 확인
4. **YouTube Studio**에서 업로드된 영상 확인

### 5-4. 예상 실행 시간

- **스크립트 생성**: ~10초
- **이미지 생성**: ~30초 (6개)
- **비디오 생성**: ~60초 (Sora-2)
- **TTS 생성**: ~5초
- **자막 생성**: ~10초
- **FFmpeg 합성**: ~20초
- **YouTube 업로드**: ~30초

**총 예상 시간**: **약 3-5분**

---

## 6. 문제 해결

### 6-1. Google Sheets 오류

**증상**: "Permission denied" 또는 "Sheet not found"

**해결**:
1. 스프레드시트 공유 설정 확인 (링크가 있는 모든 사용자 → 편집자)
2. n8n Google OAuth2 credential 재인증
3. 스프레드시트 ID 정확성 확인

### 6-2. YouTube 업로드 오류

**증상**: "Quota exceeded" 또는 "Upload failed"

**해결**:
1. YouTube Data API v3 할당량 확인 (일일 10,000 units)
2. OAuth2 scope에 `youtube.upload` 포함 확인
3. 비디오 파일 크기 확인 (최대 256GB, 권장 2GB 이하)

### 6-3. Vertex AI 오류

**증상**: "Authentication failed" 또는 "Model not found"

**해결**:
1. 서비스 계정에 **"Vertex AI User"** 역할 부여 확인
2. Vertex AI API 활성화 확인
3. Region 설정 확인 (asia-northeast3)

---

## 7. 비용 최적화 팁

### 7-1. API 호출 최소화

- **스크립트 캐싱**: 동일한 주제는 재사용
- **이미지 재사용**: 유사한 주제는 이미지 공유
- **배치 처리**: 여러 영상을 한 번에 생성

### 7-2. 할당량 관리

- **YouTube 업로드**: 일일 50개 제한 (기본 할당량)
- **OpenAI API**: Rate limit 고려 (분당 요청 수)
- **Vertex AI**: 프로젝트별 할당량 확인

### 7-3. 테스트 모드

- **Private 업로드**: 초기 테스트는 private으로
- **작은 배치**: 한 번에 1-3개씩 테스트
- **로그 확인**: 각 단계별 비용 추적

---

## 8. 다음 단계

1. ✅ **모든 Credential 설정 완료**
2. ✅ **Google Sheets 및 Drive 폴더 생성**
3. ✅ **YouTube 채널 및 API 활성화**
4. 🔄 **워크플로우 첫 실행 테스트**
5. 📊 **결과 분석 및 최적화**
6. 🚀 **자동화 스케줄 설정** (Daily Trigger)

---

**작성일**: 2025-11-24  
**버전**: v7 ULTIMATE  
**예상 비용**: 영상당 ₩1,025 (YouTube만) / ₩1,075 (Blotato 포함)
