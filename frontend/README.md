# Sprachassistent Frontend

Next.js frontend for the German language tutor application.

## Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **React** (client-side state management)

## Setup

```bash
cd frontend
npm install
npm run dev
```

The app will be available at http://localhost:3000

## Features

- **Unit Picker**: Loads units from the backend API based on CEFR level
- **Chat Interface**: Send messages and receive tutor responses
- **German Text Cards**: German examples wrapped in `[[de]]...[[/de]]` are rendered as interactive cards with play buttons
- **Audio Playback**: Click play buttons to hear German text spoken via TTS
- **Real-time State**: All conversation state managed in React (no localStorage)

## API Integration

The frontend connects to the backend at `http://localhost:8000`:

- `GET /lessons/units/{level}` - Fetch units for a level
- `POST /lessons/turn` - Send a message and get tutor response
- `POST /audio/speak` - Get audio for text (German or Uzbek)

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       # Root layout with metadata
│   ├── page.tsx         # Main chat page
│   └── globals.css      # Tailwind imports
├── components/
│   ├── UnitPicker.tsx   # Unit selection component
│   ├── MessageList.tsx  # Chat message display
│   ├── MessageInput.tsx # Message input field
│   └── GermanTextCard.tsx # German text with audio button
├── lib/
│   ├── types.ts         # TypeScript type definitions
│   ├── api.ts           # Backend API functions
│   └── parseMessage.tsx # Parse [[de]] tags into cards
└── package.json
```

## Development

Make sure the backend is running on port 8000 before starting the frontend.
