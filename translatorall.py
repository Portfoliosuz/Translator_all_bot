from google_trans_new import google_translator
def detect(text):
    translator = google_translator()
    detected = translator.detect(text)
    return detected
def translatornew(text, to_lang):
    translator = google_translator()
    translator1 = translator.translate(
        text=text, lang_tgt=to_lang, lang_src=detect(text)[0])
    return translator1
