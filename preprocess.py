# preprocess.py
# Cleans one English sentence. Used by model_building.ipynb and app.py,
# so training and prediction use exactly the same cleaning.

import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# words we must keep, because dropping them changes the meaning
KEEP = {"not", "no", "nor", "never", "cant", "cannot", "without"}
STOP = set(stopwords.words("english")) - KEEP

# banking short forms that speech-to-text often writes with spaces
ACRONYMS = ["ifsc", "upi", "pin", "otp", "kyc", "emi"]

lemmatizer = WordNetLemmatizer()


def join_letters(text):
    for a in ACRONYMS:
        spaced = " ".join(a)                          # "ifsc" becomes "i f s c"
        text = re.sub(r"\b" + spaced + r"\b", a, text)
    return text


def preprocess(text, join=True, remove_stop=True):
    text = str(text).lower()
    text = text.replace("'", "")                      # can't becomes cant
    text = re.sub(r"[^a-z0-9 ]", " ", text)           # remove punctuation
    if join:
        text = join_letters(text)
    words = text.split()
    if remove_stop:
        words = [w for w in words if w not in STOP]
    words = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(words)