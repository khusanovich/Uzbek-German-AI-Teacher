"use client";

import { useState } from "react";
import { speakText } from "@/lib/api";

interface GermanTextCardProps {
  text: string;
}

export default function GermanTextCard({ text }: GermanTextCardProps) {
  const [isPlaying, setIsPlaying] = useState(false);

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

  return (
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
    </span>
  );
}
