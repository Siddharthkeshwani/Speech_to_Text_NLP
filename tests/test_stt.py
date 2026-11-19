# tests/test_stt.py
# Tests for stt.py. They use made-up sound and a fake Whisper model,
# so they need no microphone, no internet and no model download.

import numpy as np
import soundfile as sf

import stt


def make_tone(seconds, loudness=0.3):
    t = np.arange(int(seconds * 16000)) / 16000
    return (loudness * np.sin(2 * np.pi * 220 * t)).astype("float32")


class FakeModel:
    def transcribe(self, audio, language=None, fp16=False):
        return {"text": " my card is lost ", "segments": [{"avg_logprob": -0.2, "no_speech_prob": 0.01}]}


def use_fake_whisper(monkeypatch):
    monkeypatch.setattr(stt, "get_whisper", lambda size: FakeModel())


def save_clip(tmp_path, audio, rate=16000):
    path = str(tmp_path / "clip.wav")
    sf.write(path, audio, rate)
    return path


# ---------- audio checks ----------

def test_short_clip_is_flagged():
    assert "too_short" in stt.check_audio(make_tone(0.5))


def test_long_clip_is_flagged():
    assert "too_long" in stt.check_audio(make_tone(16))


def test_silence_is_too_quiet():
    assert "too_quiet" in stt.check_audio(np.zeros(16000 * 3, dtype="float32"))


def test_normal_clip_has_no_flags():
    assert stt.check_audio(make_tone(3)) == []


def test_clipped_clip_is_flagged():
    loud = np.ones(16000 * 3, dtype="float32")
    assert "clipped" in stt.check_audio(loud)


def test_clean_audio_sets_the_peak():
    cleaned = stt.clean_audio(make_tone(3, loudness=0.1))
    assert abs(np.max(np.abs(cleaned)) - 0.9) < 0.01


def test_clean_audio_cuts_silence():
    padded = np.concatenate([np.zeros(16000 * 2), make_tone(1), np.zeros(16000 * 2)]).astype("float32")
    assert len(stt.clean_audio(padded)) < len(padded)


def test_stereo_and_other_rates_are_converted(tmp_path):
    stereo = np.stack([make_tone(2), make_tone(2)], axis=1)
    path = save_clip(tmp_path, stereo, rate=8000)
    audio = stt.load_wav(path)
    assert audio.ndim == 1
    assert abs(len(audio) - 4 * 16000) < 5      # 2 s at 8 kHz is 16,000 samples; it should become about 64,000


def test_text_is_tidied():
    assert stt.normalise_text("  my   card \n is lost ") == "my card is lost"


# ---------- the transcribe function, with a fake Whisper ----------

def test_transcribe_returns_text(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    path = save_clip(tmp_path, make_tone(3))
    result = stt.transcribe(path, "en")
    assert result["ok"] is True
    assert result["text"] == "my card is lost"
    assert result["text_raw"] == " my card is lost "
    assert result["engine"] == "whisper-small"
    assert result["avg_logprob"] == -0.2


def test_short_clip_gets_a_plain_message(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    path = save_clip(tmp_path, make_tone(0.4))
    result = stt.transcribe(path, "en")
    assert result["ok"] is False
    assert result["message"] == stt.MESSAGES["too_short"]


def test_missing_file_gets_the_trouble_message():
    result = stt.transcribe("no_such_file.wav", "en")
    assert result["ok"] is False
    assert result["message"] == stt.MESSAGES["trouble"]


def test_auto_detect_uses_the_detected_language(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    monkeypatch.setattr(stt, "detect_language", lambda audio: [("mr", 0.9), ("hi", 0.05)])
    path = save_clip(tmp_path, make_tone(3))
    result = stt.transcribe(path, "auto")
    assert result["detected"] == "mr"
    assert result["confirm_language"] is False


def test_hindi_and_urdu_ask_for_a_confirm(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    monkeypatch.setattr(stt, "detect_language", lambda audio: [("hi", 0.95), ("ur", 0.04)])
    path = save_clip(tmp_path, make_tone(3))
    assert stt.transcribe(path, "auto")["confirm_language"] is True


def test_low_score_asks_for_a_confirm(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    monkeypatch.setattr(stt, "detect_language", lambda audio: [("ta", 0.4), ("te", 0.3)])
    path = save_clip(tmp_path, make_tone(3))
    assert stt.transcribe(path, "auto")["confirm_language"] is True


def test_unsupported_language(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    monkeypatch.setattr(stt, "detect_language", lambda audio: [("fr", 0.9), ("en", 0.05)])
    path = save_clip(tmp_path, make_tone(3))
    result = stt.transcribe(path, "auto")
    assert result["ok"] is False
    assert result["message"] == stt.MESSAGES["unsupported"]


def test_manipuri_has_no_whisper_support(tmp_path, monkeypatch):
    use_fake_whisper(monkeypatch)
    path = save_clip(tmp_path, make_tone(3))
    result = stt.transcribe(path, "mni", engine="whisper", size="base")
    assert result["ok"] is False
    assert result["message"] == stt.MESSAGES["unsupported"]


def test_engine_failure_gets_the_trouble_message(tmp_path, monkeypatch):
    def broken(size):
        raise RuntimeError("model failed")
    monkeypatch.setattr(stt, "get_whisper", broken)
    path = save_clip(tmp_path, make_tone(3))
    result = stt.transcribe(path, "en")
    assert result["ok"] is False
    assert result["message"] == stt.MESSAGES["trouble"]