"use client";

import { useState, useRef } from "react";
import { speakText, transcribeAudio } from "@/lib/api";

interface GermanTextCardProps {
  text: string;
}

export default function GermanTextCard({ text }: GermanTextCardProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState<string | null>(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handlePlay = async () => {
    if (isPlaying) return;

    setIsPlaying(true);
    try {
      const audioBlob = await speakText({ lang: "de", text });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

      audio.onerror = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

      await audio.play();
    } catch (error) {
      console.error("Failed to play audio:", error);
      setIsPlaying(false);
    }
  };

  const handleRecord = async () => {
    if (isRecording) {
      // Stop recording
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream, {
          mimeType: "audio/webm",
        });

        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, {
            type: "audio/webm",
          });

          // Stop all tracks
          stream.getTracks().forEach((track) => track.stop());

          // Transcribe the audio
          setIsTranscribing(true);
          try {
            const text = await transcribeAudio(audioBlob);
            setTranscription(text);
          } catch (error) {
            console.error("Failed to transcribe audio:", error);
            setTranscription("Error: Failed to transcribe");
          } finally {
            setIsTranscribing(false);
          }
        };

        mediaRecorderRef.current = mediaRecorder;
        mediaRecorder.start();
        setIsRecording(true);
        setTranscription(null); // Clear previous transcription
      } catch (error) {
        console.error("Failed to access microphone:", error);
        alert("Please allow microphone access to record your pronunciation");
      }
    }
  };

  return (
    <div className="inline-block">
      <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-50 border border-blue-200 rounded-lg">
        <span className="font-medium text-blue-900">{text}</span>
        <button
          onClick={handlePlay}
          disabled={isPlaying}
          className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors ${
            isPlaying
              ? "bg-blue-300 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600"
          }`}
          title="Play audio"
        >
          <svg
            className="w-3 h-3 text-white"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            {isPlaying ? (
              <rect x="6" y="4" width="4" height="16" />
            ) : (
              <path d="M8 5v14l11-7z" />
            )}
          </svg>
        </button>
        <button
          onClick={handleRecord}
          disabled={isTranscribing}
          className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors ${
            isRecording
              ? "bg-red-500 hover:bg-red-600 animate-pulse"
              : isTranscribing
              ? "bg-gray-300 cursor-not-allowed"
              : "bg-gray-500 hover:bg-gray-600"
          }`}
          title={isRecording ? "Stop recording" : "Record your pronunciation"}
        >
          <svg
            className="w-3 h-3 text-white"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            {isRecording ? (
              <rect x="6" y="6" width="12" height="12" />
            ) : (
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z" />
            )}
          </svg>
        </button>
      </span>
      {isTranscribing && (
        <div className="mt-2 text-sm text-gray-600 italic">
          Transcribing...
        </div>
      )}
      {transcription && !isTranscribing && (
        <div className="mt-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="text-xs text-gray-500 mb-1">You said:</div>
          <div className="text-sm font-medium text-gray-900">{transcription}</div>
          {transcription.toLowerCase().trim() === text.toLowerCase().trim() && (
            <div className="text-xs text-green-600 mt-1">✓ Perfect match!</div>
          )}
        </div>
      )}
    </div>
  );
}
