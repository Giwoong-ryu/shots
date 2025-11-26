import openai
import json
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"

# 오디오 파일 경로
audio_file_path = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의.mp3"

print("🎤 오디오 파일을 텍스트로 변환 중...")
print(f"파일: {audio_file_path}\n")

try:
    with open(audio_file_path, "rb") as audio_file:
        # Whisper API로 변환 (verbose_json으로 타임스탬프 포함)
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            language="ko",
            timestamp_granularities=["word"]
        )
    
    # 결과 출력
    print("✅ 변환 완료!\n")
    print("=" * 80)
    print(transcript.text)
    print("=" * 80)
    
    # 결과를 파일로 저장
    output_txt = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의_transcript.txt"
    output_json = r"C:\Users\user\Desktop\gpt\n8n-copilot\shots\쇼츠강의_transcript.json"
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(transcript.text)
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(transcript.model_dump(), f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 텍스트 저장: {output_txt}")
    print(f"📄 JSON 저장: {output_json}")
    
    # 기본 통계
    word_count = len(transcript.text.split())
    print(f"\n📊 통계:")
    print(f"  - 총 글자 수: {len(transcript.text):,}자")
    print(f"  - 총 단어 수: {word_count:,}개")
    print(f"  - 예상 길이: {transcript.duration:.1f}초 ({transcript.duration/60:.1f}분)")
    
except FileNotFoundError:
    print(f"❌ 오류: 파일을 찾을 수 없습니다.")
    print(f"경로: {audio_file_path}")
except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")
