import type { CEFR, Unit, TurnRequest, TurnResponse, SpeakRequest } from "./types";

const API_BASE = "http://localhost:8000";

export async function getUnits(level: CEFR): Promise<Unit[]> {
  const res = await fetch(`${API_BASE}/lessons/units/${level}`);
  if (!res.ok) throw new Error("Failed to fetch units");
  return res.json();
}

export async function sendTurn(req: TurnRequest): Promise<TurnResponse> {
  const res = await fetch(`${API_BASE}/lessons/turn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error("Failed to send turn");
  return res.json();
}

export async function speakText(req: SpeakRequest): Promise<Blob> {
  const res = await fetch(`${API_BASE}/audio/speak`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error("Failed to get audio");
  return res.blob();
}

export async function transcribeAudio(audioBlob: Blob): Promise<string> {
  const formData = new FormData();
  formData.append("file", audioBlob, "recording.webm");

  const res = await fetch(`${API_BASE}/audio/listen`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Failed to transcribe audio");
  const data = await res.json();
  return data.text;
}
