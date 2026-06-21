"""
Text-to-speech via ElevenLabs.

Two voices: German for the [[de]]...[[/de]] examples, Uzbek for explanations.
The tutor wraps German examples in [[de]] tags; split_by_language() separates
them so each chunk goes to the right voice/model.

Notes:
- German: eleven_multilingual_v2 (high quality, German is on its language list).
- Uzbek: lower-resource, so it uses a broader model (eleven_v3) by default.
  Verify Uzbek voice quality before relying on it — pick a voice from the
  library that actually supports uz.
- Results are cached on disk by content hash so repeated German examples don't
  cost a new generation each time.
"""
import os
import re
import hashlib
from dataclasses import dataclass
from pathlib import Path

import requests

DE_PATTERN = re.compile(r"\[\[de\]\](.*?)\[\[/de\]\]", re.DOTALL)

_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
_BASE = "https://api.elevenlabs.io/v1/text-to-speech"
_CACHE_DIR = Path(os.environ.get("AUDIO_CACHE_DIR", ".audio_cache"))
_OUTPUT_FORMAT = os.environ.get("TTS_OUTPUT_FORMAT", "mp3_44100_128")


@dataclass(frozen=True)
class VoiceConfig:
    voice_id: str
    model_id: str
    language_code: str  # ISO 639-1, enforces language + text normalization


# Configure per language via env. Fill the voice IDs from GET /v1/voices.
VOICES: dict[str, VoiceConfig] = {
    "de": VoiceConfig(
        voice_id=os.environ.get("TTS_DE_VOICE_ID", ""),
        model_id=os.environ.get("TTS_DE_MODEL", "eleven_multilingual_v2"),
        language_code="de",
    ),
    "uz": VoiceConfig(
        voice_id=os.environ.get("TTS_UZ_VOICE_ID", ""),
        model_id=os.environ.get("TTS_UZ_MODEL", "eleven_v3"),
        language_code="uz",
    ),
}


def split_by_language(text: str) -> list[tuple[str, str]]:
    """Returns [(lang, chunk), ...] where lang is 'de' or 'uz'."""
    out, idx = [], 0
    for m in DE_PATTERN.finditer(text):
        if m.start() > idx:
            out.append(("uz", text[idx:m.start()].strip()))
        out.append(("de", m.group(1).strip()))
        idx = m.end()
    if idx < len(text):
        out.append(("uz", text[idx:].strip()))
    return [(lang, chunk) for lang, chunk in out if chunk]


def _cache_path(lang: str, text: str, cfg: VoiceConfig) -> Path:
    key = f"{lang}|{cfg.voice_id}|{cfg.model_id}|{text}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
    return _CACHE_DIR / f"{digest}.mp3"


def synthesize(text: str, lang: str) -> bytes:
    """Return MP3 bytes for `text` in the given language ('de' | 'uz')."""
    if lang not in VOICES:
        raise ValueError(f"unsupported lang: {lang}")
    cfg = VOICES[lang]
    if not cfg.voice_id:
        raise RuntimeError(f"No voice_id configured for '{lang}' (set TTS_{lang.upper()}_VOICE_ID)")

    cache_file = _cache_path(lang, text, cfg)
    if cache_file.exists():
        return cache_file.read_bytes()

    resp = requests.post(
        f"{_BASE}/{cfg.voice_id}",
        params={"output_format": _OUTPUT_FORMAT},
        headers={"xi-api-key": _API_KEY, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": cfg.model_id,
            "language_code": cfg.language_code,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs {resp.status_code}: {resp.text[:300]}")

    audio = resp.content
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_bytes(audio)
    return audio
