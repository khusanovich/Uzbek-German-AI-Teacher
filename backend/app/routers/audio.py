"""Audio endpoint. Frontend calls this per chunk for tap-to-hear playback."""
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from app.services.tts import synthesize, split_by_language

router = APIRouter(prefix="/audio", tags=["audio"])


class SpeakRequest(BaseModel):
    lang: str   # "de" | "uz"
    text: str


@router.post("/speak")
def speak(req: SpeakRequest):
    """Return MP3 audio for a single chunk."""
    try:
        audio = synthesize(req.text, req.lang)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(400, str(e))
    return Response(content=audio, media_type="audio/mpeg")


class SplitRequest(BaseModel):
    text: str  # a full tutor reply containing [[de]] tags


@router.post("/split")
def split(req: SplitRequest):
    """Preview how a reply splits into de/uz chunks (no audio generated)."""
    return {"chunks": [{"lang": l, "text": t} for l, t in split_by_language(req.text)]}
