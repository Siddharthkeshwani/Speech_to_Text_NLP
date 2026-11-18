# stt.py
# Speech to text for one short clip. Used by app.py and by phase4_gate.py.

import difflib
import json
import os
import time
import unicodedata

import numpy as np
import soundfile as sf

SAMPLE_RATE = 16000       # speech models expect 16,000 samples per second
MIN_SECONDS = 1           # shorter clips are refused
MAX_SECONDS = 15          # longer clips are refused
QUIET_LEVEL = 0.005       # below this average loudness the clip is "too quiet"
LOW_SCORE = 0.6           # a language detection score below this needs a confirm
INDIC_MODEL = "ai4bharat/indic-conformer-600m-multilingual"

# plain-words messages, from the wireframes
MESSAGES = {
    "too_short": "That was very short. Please say a full sentence.",
    "too_long": "That was long. Please say it in one or two sentences.",
    "too_quiet": "I could not hear you. Please try again, closer to the phone.",
    "unsupported": "I cannot understand this language yet. Let me connect you to a person.",
    "trouble": "I am having trouble. Let me connect you to a person.",
}

config_path = os.path.join(os.path.dirname(__file__), "language_config.json")
with open(config_path, encoding="utf-8") as f:
    LANGS = json.load(f)

whisper_models = {}       # loaded Whisper models, one per size
indic_model = None        # the IndicConformer model, loaded only if needed


def load_wav(path):
    audio, rate = sf.read(path, dtype="float32")
    if audio.ndim == 2:                       # stereo to mono
        audio = audio.mean(axis=1)
    if rate != SAMPLE_RATE:                   # change to 16,000 samples per second
        new_length = int(len(audio) * SAMPLE_RATE / rate)
        positions = np.linspace(0, len(audio) - 1, new_length)
        audio = np.interp(positions, np.arange(len(audio)), audio).astype("float32")
    return audio


def check_audio(audio):
    flags = []
    seconds = len(audio) / SAMPLE_RATE
    if seconds < MIN_SECONDS:
        flags.append("too_short")
    if seconds > MAX_SECONDS:
        flags.append("too_long")
    if len(audio) == 0 or np.sqrt(np.mean(audio ** 2)) < QUIET_LEVEL:
        flags.append("too_quiet")
    if len(audio) > 0 and np.mean(np.abs(audio) > 0.99) > 0.01:
        flags.append("clipped")
    return flags


def clean_audio(audio):
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.9            # make the volume even
    loud = np.where(np.abs(audio) > 0.05)[0]
    if len(loud) > 0:                         # cut silence at the start and end
        margin = int(0.2 * SAMPLE_RATE)
        start = max(loud[0] - margin, 0)
        end = min(loud[-1] + margin, len(audio))
        audio = audio[start:end]
    return audio.astype("float32")


def normalise_text(text):
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())


def get_whisper(size):
    if size not in whisper_models:
        import whisper
        whisper_models[size] = whisper.load_model(size)
    return whisper_models[size]


def detect_language(audio):
    import whisper
    model = get_whisper("base")
    mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio), n_mels=model.dims.n_mels)
    mel = mel.to(model.device)
    tokens, probs = model.detect_language(mel)
    ranked = sorted(probs.items(), key=lambda item: item[1], reverse=True)
    return ranked[:2]                         # the top two guesses


def transcribe_whisper(audio, whisper_code, size):
    model = get_whisper(size)
    result = model.transcribe(audio, language=whisper_code, fp16=False)
    segments = result["segments"]
    count = max(len(segments), 1)
    avg_logprob = sum(s["avg_logprob"] for s in segments) / count
    no_speech = sum(s["no_speech_prob"] for s in segments) / count
    return result["text"], avg_logprob, no_speech


def get_indic():
    global indic_model
    if indic_model is None:
        from transformers import AutoModel
        indic_model = AutoModel.from_pretrained(INDIC_MODEL, trust_remote_code=True)
    return indic_model


def transcribe_indic(audio, indic_code):
    import torch
    model = get_indic()
    wav = torch.tensor(audio).unsqueeze(0)    # shape (1, number of samples)
    ctc_text = str(model(wav, indic_code, "ctc")).strip()
    rnnt_text = str(model(wav, indic_code, "rnnt")).strip()
    agree = difflib.SequenceMatcher(None, ctc_text, rnnt_text).ratio()
    return rnnt_text, agree


def transcribe(audio_path, lang, engine=None, size=None):
    result = {"ok": False, "text_raw": "", "text": "", "engine": "", "seconds": 0.0,
              "flags": [], "avg_logprob": None, "no_speech_prob": None, "indic_agree": None,
              "detected": None, "detect_score": None, "confirm_language": False, "message": ""}

    # 1. read and check the audio
    try:
        audio = load_wav(audio_path)
    except Exception:
        result["message"] = MESSAGES["trouble"]
        return result
    result["flags"] = check_audio(audio)
    for problem in ["too_short", "too_long", "too_quiet"]:
        if problem in result["flags"]:
            result["message"] = MESSAGES[problem]
            return result
    audio = clean_audio(audio)

    # 2. find the language (the dropdown always wins over auto-detect)
    try:
        if lang == "auto":
            top_two = detect_language(audio)
            lang = top_two[0][0]
            result["detected"] = lang
            result["detect_score"] = round(float(top_two[0][1]), 3)
            pair = {top_two[0][0], top_two[1][0]}
            if pair == {"hi", "ur"} or result["detect_score"] < LOW_SCORE:
                result["confirm_language"] = True
        if lang not in LANGS:
            result["message"] = MESSAGES["unsupported"]
            return result
    except Exception:
        result["message"] = MESSAGES["trouble"]
        return result

    # 3. pick the engine and run it
    cfg = LANGS[lang]
    engine = engine or cfg["engine"]
    size = size or cfg["size"]
    try:
        if engine == "indic":
            if cfg["indic_code"] is None:
                result["message"] = MESSAGES["unsupported"]
                return result
            get_indic()                       # load first, so loading time is not counted
            start = time.time()
            text, result["indic_agree"] = transcribe_indic(audio, cfg["indic_code"])
            result["engine"] = "indic-conformer"
        else:
            if cfg["whisper_code"] is None:
                result["message"] = MESSAGES["unsupported"]
                return result
            get_whisper(size)
            start = time.time()
            text, result["avg_logprob"], result["no_speech_prob"] = transcribe_whisper(audio, cfg["whisper_code"], size)
            result["engine"] = "whisper-" + size
        result["seconds"] = round(time.time() - start, 2)
    except Exception:
        result["message"] = MESSAGES["trouble"]
        return result

    # 4. keep the raw text and a lightly cleaned copy
    result["text_raw"] = text
    result["text"] = normalise_text(text)
    result["ok"] = True
    return result