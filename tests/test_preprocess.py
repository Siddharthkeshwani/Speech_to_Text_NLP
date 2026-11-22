# tests/test_preprocess.py
# Tests for preprocess.py

from preprocess import preprocess


def test_example_from_the_project_document():
    assert preprocess("I LOVE This Product!!!") == "love product"


def test_not_is_kept():
    assert preprocess("My card is not working") == "card not working"


def test_cant_is_kept():
    words = preprocess("I can't find my card").split()
    assert "cant" in words


def test_never_and_without_are_kept():
    assert "never" in preprocess("I never made this payment").split()
    assert "without" in preprocess("Money taken without my permission").split()


def test_spaced_ifsc_is_joined():
    assert "ifsc" in preprocess("need branch i f s c code").split()


def test_spaced_upi_and_pin_are_joined():
    assert "upi" in preprocess("u p i payment failed").split()
    assert "pin" in preprocess("how to generate p i n").split()


def test_banking_words_survive():
    words = preprocess("Tell me the IFSC code of my branch").split()
    for w in ["ifsc", "code", "branch"]:
        assert w in words


def test_plural_becomes_single():
    assert preprocess("my transactions") == "transaction"


def test_joining_can_be_turned_off():
    assert "ifsc" not in preprocess("i f s c", join=False).split()


def test_empty_text_gives_empty_text():
    assert preprocess("") == ""
    assert preprocess("   ") == ""