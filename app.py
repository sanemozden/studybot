import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3-flash-preview"  # çalışmazsa AI Studio'da gördüğün başka bir Flash modelini yaz

PROMPT = """Sen bir çalışma asistanısın. Kullanıcının verdiği konu için:
1. 4-5 cümlelik sade bir özet yaz.
2. 3 tane çoktan seçmeli soru hazırla (her birinde 4 şık).

SADECE şu JSON formatında cevap ver, başka hiçbir şey yazma:
{
  "ozet": "...",
  "sorular": [
    {"soru": "...", "siklar": ["A", "B", "C", "D"], "dogru": 0, "aciklama": "..."}
  ]
}
"dogru" alanı doğru şıkkın indeksidir (0-3). Dil: {DIL}. Özet, sorular, şıklar ve açıklamaların hepsi bu dilde olsun."""

# Sayfadaki tüm yazılar burada. Yeni dil eklemek için bir blok daha eklemen yeterli.
YAZILAR = {
    "Türkçe": {
        "konu": "Hangi konuyu çalışmak istiyorsun?",
        "ornek": "örn. Fotosentez",
        "olustur": "Oluştur",
        "bekle": "Hazırlanıyor...",
        "hata": "Bir hata oluştu",
        "ozet": "Özet",
        "sorular": "Sorular",
        "kontrol": "Cevapları kontrol et",
        "dogru": "Doğru ✅",
        "yanlis": "Yanlış ❌",
        "dogru_cevap": "Doğru cevap",
        "soru": "soru",
        "skor": "Skorun",
        "anahtar_yok": "GEMINI_API_KEY bulunamadı. .env dosyasını kontrol et.",
    },
    "Deutsch": {
        "konu": "Welches Thema möchtest du lernen?",
        "ornek": "z. B. Vorstellungsgespräch",
        "olustur": "Erstellen",
        "bekle": "Wird vorbereitet...",
        "hata": "Ein Fehler ist aufgetreten",
        "ozet": "Zusammenfassung",
        "sorular": "Fragen",
        "kontrol": "Antworten prüfen",
        "dogru": "Richtig ✅",
        "yanlis": "Falsch ❌",
        "dogru_cevap": "Richtige Antwort",
        "soru": "Frage",
        "skor": "Dein Ergebnis",
        "anahtar_yok": "GEMINI_API_KEY nicht gefunden. Bitte die .env-Datei prüfen.",
    },
    "English": {
        "konu": "Which topic do you want to study?",
        "ornek": "e.g. Photosynthesis",
        "olustur": "Generate",
        "bekle": "Preparing...",
        "hata": "An error occurred",
        "ozet": "Summary",
        "sorular": "Questions",
        "kontrol": "Check answers",
        "dogru": "Correct ✅",
        "yanlis": "Wrong ❌",
        "dogru_cevap": "Correct answer",
        "soru": "Question",
        "skor": "Your score",
        "anahtar_yok": "GEMINI_API_KEY not found. Please check your .env file.",
    },
}


def icerik_uret(konu: str, dil: str) -> dict:
    client = genai.Client(api_key=api_key)
    cevap = client.models.generate_content(
        model=MODEL,
        contents=f"Konu: {konu}",
        config=types.GenerateContentConfig(
            system_instruction=PROMPT.replace("{DIL}", dil),
            response_mime_type="application/json",
        ),
    )
    metin = cevap.text.replace("```json", "").replace("```", "").strip()
    return json.loads(metin)


# Dil seçimi en üstte: hem sayfa yazıları hem botun cevapları buna göre değişir
dil = st.selectbox("🌐 Dil / Sprache / Language", list(YAZILAR.keys()))
t = YAZILAR[dil]

st.title("📚 StudyBot")

if not api_key:
    st.error(t["anahtar_yok"])
    st.stop()

konu = st.text_input(t["konu"], placeholder=t["ornek"])

if st.button(t["olustur"]) and konu:
    with st.spinner(t["bekle"]):
        try:
            st.session_state["veri"] = icerik_uret(konu, dil)
            st.session_state["kontrol"] = False
        except Exception as e:
            st.error(f"{t['hata']}: {e}")

veri = st.session_state.get("veri")
if veri:
    st.subheader(t["ozet"])
    st.write(veri["ozet"])

    st.subheader(t["sorular"])
    for i, s in enumerate(veri["sorular"]):
        st.radio(f"{i + 1}. {s['soru']}", s["siklar"], index=None, key=f"s{i}")

    if st.button(t["kontrol"]):
        st.session_state["kontrol"] = True

    if st.session_state.get("kontrol"):
        dogru_sayi = 0
        for i, s in enumerate(veri["sorular"]):
            secim = st.session_state.get(f"s{i}")
            dogru_sik = s["siklar"][s["dogru"]]
            if secim == dogru_sik:
                dogru_sayi += 1
                st.success(f"{t['soru']} {i + 1}: {t['dogru']}")
            else:
                st.error(f"{t['soru']} {i + 1}: {t['yanlis']} | {t['dogru_cevap']}: {dogru_sik}")
            st.caption(s["aciklama"])
        st.metric(t["skor"], f"{dogru_sayi} / {len(veri['sorular'])}")
