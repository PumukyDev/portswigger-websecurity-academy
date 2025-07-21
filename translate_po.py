import os
import polib
import requests
import time

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

if not DEEPL_API_KEY:
    raise ValueError("Error: DEEPL_API_KEY environment variable is not set.")

def translate_text(text, source="ES", target="EN"):
    if not text.strip():
        return text
    try:
        response = requests.post(
            DEEPL_URL,
            data={
                "auth_key": DEEPL_API_KEY,
                "text": text,
                "source_lang": source.upper(),
                "target_lang": target.upper()
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data["translations"][0]["text"]
    except Exception as e:
        print(f"Error translating text: '{text[:30]}...': {e}")
        return text

po_dir = "docs/locale/en/LC_MESSAGES"

for filename in os.listdir(po_dir):
    if filename.endswith(".po"):
        filepath = os.path.join(po_dir, filename)
        po = polib.pofile(filepath)
        for entry in po.untranslated_entries():
            translated = translate_text(entry.msgid)
            entry.msgstr = translated
            time.sleep(0.5)
        po.save()
        print(f"Translated {filename}")
