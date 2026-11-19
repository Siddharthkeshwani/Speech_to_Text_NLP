# tests/test_translate.py
# Tests for translate.py. They use fake translators, so they need no internet.

import sys
import time
import types

import pytest

import translate


@pytest.fixture(autouse=True)
def empty_cache():
    translate.cache.clear()
    translate.blocked_until.clear()


def fake_ok(text, lang):
    return "my card is lost"


def fake_fail(text, lang):
    raise RuntimeError("blocked")


def use_engines(monkeypatch, engines):
    monkeypatch.setattr(translate, "ENGINES", engines)


# ---------- the banking word fixes ----------

def test_ifc_becomes_ifsc():
    assert translate.fix_after("Tell me the IFC code of my branch") == "Tell me the IFSC code of my branch"


def test_upid_becomes_upi():
    assert translate.fix_after("Please block my UPID.") == "Please block my UPI ID."


def test_card_ping_becomes_card_pin():
    assert translate.fix_after("I want to change my card, ping.") == "I want to change my card PIN."
    assert translate.fix_after("I want to change my card ping") == "I want to change my card PIN"


def test_cart_becomes_card():
    assert translate.fix_after("My cart is missing.") == "My card is missing."


def test_guide_becomes_card():
    assert translate.fix_after("My guide is not working at the shop.") == "My card is not working at the shop."


def test_spaced_letters_are_joined():
    assert translate.fix_after("i f s c code") == "IFSC code"


def test_hindi_spelling_becomes_english_letters():
    assert translate.fix_before("मुझे आईएफएससी चाहिए") == "मुझे IFSC चाहिए"


# ---------- to_english ----------

def test_english_skips_translation(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_fail]])
    result = translate.to_english("Tell me the IFC code", "en")
    assert result["ok"] is True
    assert result["engine"] == "none"
    assert result["english"] == "Tell me the IFSC code"


def test_translation_works(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_ok]])
    result = translate.to_english("मेरा कार्ड खो गया है", "hi")
    assert result["ok"] is True
    assert result["english"] == "my card is lost"
    assert result["engine"] == "Google"
    assert result["flags"] == []


def test_second_translator_is_used_when_first_fails(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_fail], ["MyMemory", fake_ok]])
    result = translate.to_english("मेरा कार्ड खो गया है", "hi")
    assert result["ok"] is True
    assert result["engine"] == "MyMemory"


def test_both_fail_gives_the_trouble_message(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_fail], ["MyMemory", fake_fail]])
    result = translate.to_english("मेरा कार्ड खो गया है", "hi")
    assert result["ok"] is False
    assert result["message"] == translate.MESSAGES["trouble"]


def test_unsupported_language(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_ok]])
    result = translate.to_english("some text", "mni")
    assert result["ok"] is False
    assert result["message"] == translate.MESSAGES["unsupported"]


def test_empty_text(monkeypatch):
    use_engines(monkeypatch, [["Google", fake_ok]])
    result = translate.to_english("   ", "hi")
    assert result["ok"] is False
    assert result["message"] == translate.MESSAGES["trouble"]


def test_slow_translator_is_stopped(monkeypatch):
    def fake_slow(text, lang):
        time.sleep(1)
        return "too late"
    monkeypatch.setattr(translate, "TIMEOUT_SECONDS", 0.2)
    use_engines(monkeypatch, [["Google", fake_slow], ["MyMemory", fake_ok]])
    result = translate.to_english("मेरा कार्ड खो गया है", "hi")
    assert result["engine"] == "MyMemory"


def test_same_sentence_is_translated_once(monkeypatch):
    calls = []

    def counting(text, lang):
        calls.append(1)
        return "my card is lost"
    use_engines(monkeypatch, [["Google", counting]])
    translate.to_english("मेरा कार्ड खो गया है", "hi")
    translate.to_english("मेरा कार्ड खो गया है", "hi")
    assert len(calls) == 1


def test_no_banking_word_gets_a_flag(monkeypatch):
    def weather(text, lang):
        return "it is a sunny day"
    use_engines(monkeypatch, [["Google", weather]])
    result = translate.to_english("आज धूप है", "hi")
    assert result["flags"] == ["no_banking_word"]


def test_glossary_term_survives_translation(monkeypatch):
    def mangled(text, lang):
        return "tell me the IFC code"
    use_engines(monkeypatch, [["Google", mangled]])
    result = translate.to_english("मुझे आईएफएससी बताओ", "hi")
    assert result["english"] == "tell me the IFSC code"


def test_rajasthani_uses_the_hindi_setting(monkeypatch):
    seen = []

    def spy(text, lang):
        seen.append(lang)
        return "my card is lost"
    use_engines(monkeypatch, [["Google", spy]])
    translate.to_english("मारो कार्ड खो गयो", "raj")
    assert seen == ["raj"]
    assert translate.CODES["raj"][0] == "hi"


def test_mymemory_limit_message_is_an_error(monkeypatch):
    class FakeMyMemory:
        def __init__(self, source, target):
            pass

        def translate(self, text):
            return "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY"

    fake_module = types.ModuleType("deep_translator")
    fake_module.MyMemoryTranslator = FakeMyMemory
    monkeypatch.setitem(sys.modules, "deep_translator", fake_module)
    with pytest.raises(RuntimeError):
        translate.mymemory("some text", "hi")


def test_failed_translator_is_skipped_next_time(monkeypatch):
    calls = []

    def failing(text, lang):
        calls.append(1)
        raise RuntimeError("blocked")
    use_engines(monkeypatch, [["Google", failing], ["MyMemory", fake_ok]])
    translate.to_english("पहला वाक्य", "hi")
    translate.to_english("दूसरा वाक्य", "hi")
    assert len(calls) == 1


def test_all_blocked_translators_are_tried_again(monkeypatch):
    calls = []

    def fails_once(text, lang):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("blocked")
        return "my card is lost"
    use_engines(monkeypatch, [["Google", fails_once]])
    first = translate.to_english("पहला वाक्य", "hi")
    second = translate.to_english("दूसरा वाक्य", "hi")
    assert first["ok"] is False
    assert second["ok"] is True