"""
Speech-to-text for the speaking exercises. The learner speaks GERMAN, which
is well supported (Whisper). For real pronunciation scoring use Azure
Pronunciation Assessment instead of plain transcription.
"""


def transcribe_german(audio_bytes: bytes) -> str:
    """TODO: call Whisper (whisper-1 / local faster-whisper)."""
    raise NotImplementedError("Wire Whisper here")
