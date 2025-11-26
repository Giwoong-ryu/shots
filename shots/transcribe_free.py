import whisper
import json

print("🎤 로컬 Whisper 모델로 변환 중... (완전 무료!)")
print("=" * 80)

# Whisper 모델 로드 (medium 모델 사용 - 정확도와 속도 균형)
print("📥 Whisper 모델 로딩 중...")
model = whisper.load_model("medium")  # base, small, medium, large 중 선택 가능

# 오디오 파일 경로
audio_file = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의.mp3"

print(f"🎧 오디오 파일: {audio_file}")
print("⏳ 변환 중... (몇 분 소요될 수 있습니다)")
print()

# 변환 실행
result = model.transcribe(
    audio_file,
    language="ko",  # 한국어
    verbose=True,   # 진행 상황 표시
    word_timestamps=True  # 단어별 타임스탬프
)

print("\n" + "=" * 80)
print("✅ 변환 완료!")
print("=" * 80)
print()

# 전체 텍스트 출력
print("📝 전체 텍스트:")
print("-" * 80)
print(result["text"])
print("-" * 80)
print()

# 결과 저장
output_txt = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의_transcript.txt"
output_json = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의_transcript.json"

# 텍스트 파일 저장
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(result["text"])

# JSON 파일 저장 (세그먼트 정보 포함)
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"💾 저장 완료:")
print(f"  - 텍스트: {output_txt}")
print(f"  - JSON: {output_json}")
print()

# 통계 정보
segments = result.get("segments", [])
print(f"📊 통계:")
print(f"  - 총 글자 수: {len(result['text']):,}자")
print(f"  - 총 세그먼트: {len(segments)}개")
print(f"  - 언어: {result.get('language', 'ko')}")
print()

print("🎉 완료! 이제 텍스트 파일을 확인하세요!")
