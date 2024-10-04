from faster_whisper import WhisperModel
model_size = "tiny"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, _ = model.transcribe("audio.mp3", beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500),language="pt")
for segment in segments:
    print(segment.text)