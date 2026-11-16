# smoke_test.py
# Checks that speech-to-text, translation and scikit-learn all work on this laptop.

import os
import sys
import time

# make the terminal print Hindi / other scripts without crashing
sys.stdout.reconfigure(encoding="utf-8")

# we store the result of each test here, so we can print a table at the end
results = []


def test_whisper():
    print("\n--- TEST 1: Whisper (speech to text) ---")
    audio_file = "data/sample_audio/test.wav"

    # if there is no audio file, we cannot test, so we stop this test
    if not os.path.exists(audio_file):
        print("Audio file not found:", audio_file)
        print("Record a short clip and save it there, then run again.")
        results.append(["Whisper", "SKIPPED", "-"])
        return

    try:
        import whisper

        start = time.time()
        model = whisper.load_model("base")
        load_time = time.time() - start
        print("Model loaded in", round(load_time, 1), "seconds")

        start = time.time()
        output = model.transcribe(audio_file)
        transcribe_time = time.time() - start

        print("Text heard:", output["text"].strip())
        print("Language detected:", output["language"])
        print("Transcribed in", round(transcribe_time, 1), "seconds")
        results.append(["Whisper", "PASS", str(round(transcribe_time, 1)) + " s"])
    except Exception as error:
        print("Whisper failed:", error)
        results.append(["Whisper", "FAIL", "-"])


def test_translation():
    print("\n--- TEST 2: deep-translator (to English) ---")
    hindi_text = "मेरा कार्ड खो गया है"

    try:
        from deep_translator import GoogleTranslator

        start = time.time()
        english_text = GoogleTranslator(source="auto", target="en").translate(hindi_text)
        total_time = time.time() - start

        print("Original:", hindi_text)
        print("English:", english_text)
        print("Translated in", round(total_time, 2), "seconds")

        # our target from the plan is under 2 seconds
        if total_time < 2:
            print("Under 2 seconds: good")
        else:
            print("Slower than 2 seconds: note it down")
        results.append(["Translation", "PASS", str(round(total_time, 2)) + " s"])
    except Exception as error:
        print("Translation failed:", error)
        results.append(["Translation", "FAIL", "-"])


def test_sklearn():
    print("\n--- TEST 3: scikit-learn (tiny model) ---")

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression

        sentences = [
            "my card is lost",
            "i lost my debit card",
            "what is my balance",
            "tell me my account balance",
            "block my card",
            "i want to block my credit card",
        ]
        labels = ["lost", "lost", "balance", "balance", "block", "block"]

        start = time.time()
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)
        model = LogisticRegression()
        model.fit(X, labels)

        new_sentence = ["i lost my credit card"]
        new_X = vectorizer.transform(new_sentence)
        prediction = model.predict(new_X)
        probability = model.predict_proba(new_X).max() * 100
        total_time = time.time() - start

        print("Sentence:", new_sentence[0])
        print("Prediction:", prediction[0])
        print("Confidence:", round(probability, 1), "%")
        print("Done in", round(total_time, 3), "seconds")
        results.append(["scikit-learn", "PASS", str(round(total_time, 3)) + " s"])
    except Exception as error:
        print("scikit-learn failed:", error)
        results.append(["scikit-learn", "FAIL", "-"])


test_whisper()
test_translation()
test_sklearn()

print("\n=========== SUMMARY ===========")
for row in results:
    print(row[0].ljust(14), row[1].ljust(8), row[2])