"""
Speech-to-text for the speaking exercises. The learner speaks GERMAN, which
is well supported (Whisper). For real pronunciation scoring use Azure
Pronunciation Assessment instead of plain transcription.
"""
import os
import io
from openai import OpenAI


def transcribe_german(audio_bytes: bytes) -> str:
    """
    Transcribe German audio using OpenAI Whisper.

    Args:
        audio_bytes: Audio file bytes (webm, mp3, wav, etc.)

    Returns:
        Transcribed German text
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not configured")

    client = OpenAI(api_key=api_key)

    # Whisper expects a file-like object
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.webm"  # Provide a filename for format detection

    # Transcribe with language hint for better accuracy
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="de",  # German language hint
    )

    return transcript.text
