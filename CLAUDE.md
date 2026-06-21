# Sprachassistent — project context for Claude Code

AI tutor that teaches German to Uzbek speakers. Lessons are explained in
Uzbek up to A2.2, then progressively in German. Text + audio.

## Architecture
- `backend/` — FastAPI. Orchestrates the tutor LLM + audio services.
- `frontend/` — Next.js (App Router, TS, Tailwind). Not scaffolded yet.

## Key design decisions (don't break these)
- The CURRICULUM IS FIXED. The LLM teaches *within* a unit and must not invent
  the syllabus. Units live in `backend/app/curriculum/units.py` (move to
  Postgres later). Seed new levels by adding Unit objects.
- The Uzbek->German switch is driven by `default_instruction_language(level)`
  in `backend/app/prompts/tutor_prompt.py`, overridable per user. Do NOT
  hardcode a cutoff anywhere else.
- The tutor wraps German examples in `[[de]]...[[/de]]`. `services/tts.py`
  splits on those tags so German goes to the German voice and the rest to the
  Uzbek voice. Keep this contract intact on both ends.
- Learner speaks German (well supported by Whisper). Avoid relying on Uzbek STT.

## Run
    cd backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env   # add your keys
    uvicorn app.main:app --reload

## Next tasks
1. [DONE] TTS wired (ElevenLabs) in services/tts.py + /audio/speak route.
   Set ELEVENLABS_API_KEY + TTS_DE_VOICE_ID + TTS_UZ_VOICE_ID in .env to use it.
2. Wire Whisper in services/stt.py + a /lessons/audio route.
3. Move curriculum + learner progress into Postgres.
4. Scaffold the Next.js frontend (chat UI + tap-to-hear audio).
5. Add a vocab SRS table.
