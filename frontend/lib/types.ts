export type CEFR = "A1.1" | "A1.2" | "A2.1" | "A2.2" | "B1.1" | "B1.2" | "B2.1" | "B2.2";

export interface Unit {
  id: string;
  level: CEFR;
  title: string;
  objectives: string[];
  target_vocab: string[];
}

export interface Message {
  role: "user" | "assistant";
  content: string;
}

export interface TurnRequest {
  unit_id: string;
  learner_level: CEFR;
  message: string;
  history: Message[];
}

export interface TurnResponse {
  reply: string;
  audio_chunks: AudioChunk[];
}

export interface AudioChunk {
  lang: "de" | "uz";
  text: string;
}

export interface SpeakRequest {
  lang: "de" | "uz";
  text: string;
}
