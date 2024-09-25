# ******************************************************************************************
# FileName     : makeAudio.py
# Description  : 사운드 미터 테스트용 오디오 샘플 만들기
# Author       : 손철수
# Created Date : 2024.09.25 : 손철수 : 최초작성
# Reference    : 
# Modified     : 
# ******************************************************************************************
from pydub import AudioSegment
from pydub.generators import Sine

def generate_tone(freq, duration_ms):
    return Sine(freq).to_audio_segment(duration=duration_ms)

# 주파수 설정 (Hz)
low_freq = 200
high_freq = 2000

# 각 톤의 지속 시간 (밀리초)
duration = 5000  # 5초

# 낮은 주파수와 높은 주파수 톤 생성
low_tone = generate_tone(low_freq, duration)
high_tone = generate_tone(high_freq, duration)

# 두 톤을 연결
combined = low_tone + high_tone

# 결과를 WAV 파일로 저장
output_file = "low_high_frequency_tones.wav"
combined.export(output_file, format="wav")