"use client";

import { useEffect, useRef } from "react";
import type { Message } from "@/lib/types";
import { parseMessage } from "@/lib/parseMessage";

interface MessageListProps {
  messages: Message[];
}

export default function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="text-center text-gray-500 mt-8">
          <p className="text-lg">Start a conversation!</p>
          <p className="text-sm mt-2">
            Type a message below to begin your German lesson.
          </p>
        </div>
      ) : (
        messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-3 ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-white shadow-md text-gray-900"
              }`}
            >
              <div className="text-sm font-semibold mb-1 opacity-75">
                {msg.role === "user" ? "You" : "Tutor"}
              </div>
              <div className="whitespace-pre-wrap leading-relaxed">
                {msg.role === "assistant"
                  ? parseMessage(msg.content)
                  : msg.content}
              </div>
            </div>
          </div>
        ))
      )}
      <div ref={bottomRef} />
    </div>
  );
}
