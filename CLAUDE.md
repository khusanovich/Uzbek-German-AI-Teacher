# Sprachassistent — project context for Claude Code

AI tutor that teaches German to Uzbek speakers. Lessons are explained in
Uzbek up to A2.2, then progressively in German. Text + audio.

## Architecture
- `backend/` — FastAPI. Orchestrates the tutor LLM + audio services.
- `frontend/` — Next.js (App Router, TS, Tailwind). Chat UI with unit picker, message list, and audio playback.

## Key design decisions (don't break these)
- The CURRICULUM IS FIXED. The LLM teaches *within* a unit and must not invent
  the syllabus. Units are stored in Postgres (models.py). To seed new levels,
  add Unit objects to curriculum/units.py and run seed_db.py.
- The Uzbek->German switch is driven by `default_instruction_language(level)`
  in `backend/app/prompts/tutor_prompt.py`, overridable per user. Do NOT
  hardcode a cutoff anywhere else.
- The tutor wraps German examples in `[[de]]...[[/de]]`. `services/tts.py`
  splits on those tags so German goes to the German voice and the rest to the
  Uzbek voice. Keep this contract intact on both ends.
- Learner speaks German (well supported by Whisper). Avoid relying on Uzbek STT.

## Run

Backend:
    cd backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env   # add your keys + DATABASE_URL
    python seed_db.py      # initialize database and seed A1.1 units
    uvicorn app.main:app --reload

Frontend:
    cd frontend
    npm install
    npm run dev

## Next tasks
1. [DONE] TTS wired (ElevenLabs) in services/tts.py + /audio/speak route.
   Set ELEVENLABS_API_KEY + TTS_DE_VOICE_ID + TTS_UZ_VOICE_ID in .env to use it.
2. [DONE] Scaffold the Next.js frontend (chat UI + tap-to-hear audio).
3. [DONE] Wire Whisper in services/stt.py + /audio/listen route for pronunciation practice.
4. [DONE] Move curriculum + learner progress into Postgres (models.py, database.py, seed_db.py).
5. Add a vocab SRS table.
