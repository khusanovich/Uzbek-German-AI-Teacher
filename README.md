# Sprachassistent

An AI tutor that teaches **German to Uzbek speakers**. Lessons are explained in
Uzbek up to A2.2, then progressively in German. Supports text and audio.

## What's in here

```
sprachassistent/
├── CLAUDE.md                  # project context Claude Code reads each session
├── backend/                   # FastAPI orchestrator
│   ├── app/
│   │   ├── main.py            # app + routes
│   │   ├── prompts/
│   │   │   └── tutor_prompt.py    # ★ level + instruction-language injection
│   │   ├── curriculum/
│   │   │   └── units.py           # ★ fixed CEFR skeleton (A1.1 seeded)
│   │   ├── services/
│   │   │   ├── llm.py             # LLM call (Claude/GPT-4o)
│   │   │   ├── tts.py             # German + Uzbek voice, splits [[de]] tags
│   │   │   └── stt.py             # German Whisper
│   │   └── routers/
│   │       └── lessons.py         # /lessons/units, /lessons/turn
│   ├── requirements.txt
│   └── .env.example
└── frontend/                  # Next.js — not scaffolded yet (see below)
```

The two ★ files are the heart of it: the curriculum is fixed (the model teaches
*within* a unit, never invents the syllabus), and the Uzbek→German switch is a
single function of the learner's level, overridable per user.

## Run the backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

Then `GET http://localhost:8000/lessons/units/A1.1` and
`POST /lessons/turn` to try a lesson turn.

## Add the frontend later

```bash
npx create-next-app@latest frontend --ts --tailwind --app
```

## Continue in VS Code with Claude Code

1. Download/unzip this folder and open it: **File → Open Folder** → pick
   `sprachassistent/` (open the folder, not a loose file).
2. Install the extension: `Cmd+Shift+X`, search **"Claude Code"** (publisher:
   Anthropic), Install. It bundles the CLI, so nothing else to install.
3. Open a file, then click the **Spark (✱) icon** top-right of the editor to
   open the panel. First launch signs you in via browser.
4. Claude Code reads `CLAUDE.md` automatically each session, so it already
   knows the architecture and the rules not to break. Start with a task like
   *"wire ElevenLabs into services/tts.py for the German and Uzbek voices."*

Requires a paid Anthropic plan (Pro or higher) or an API key.
