"use client";

import { useState } from "react";
import type { Unit, Message, CEFR } from "@/lib/types";
import { sendTurn } from "@/lib/api";
import UnitPicker from "@/components/UnitPicker";
import MessageList from "@/components/MessageList";
import MessageInput from "@/components/MessageInput";

export default function Home() {
  const [level] = useState<CEFR>("A1.1");
  const [selectedUnit, setSelectedUnit] = useState<Unit | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    if (!selectedUnit) return;

    // Add user message immediately
    const userMessage: Message = { role: "user", content };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Send to backend
      const response = await sendTurn({
        unit_id: selectedUnit.id,
        learner_level: level,
        message: content,
        history: messages,
      });

      // Add assistant response
      const assistantMessage: Message = {
        role: "assistant",
        content: response.reply,
      };
      setMessages([...newMessages, assistantMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
      // Add error message
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white px-6 py-4 shadow-md">
        <h1 className="text-2xl font-bold">Sprachassistent</h1>
        <p className="text-blue-100 text-sm">
          Your AI German tutor for Uzbek speakers
        </p>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="w-80 bg-gray-100 border-r overflow-y-auto p-4">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Level
            </label>
            <div className="bg-white rounded-lg px-4 py-2 font-semibold text-blue-600 border border-blue-200">
              {level}
            </div>
          </div>
          <UnitPicker
            level={level}
            selectedUnitId={selectedUnit?.id ?? null}
            onSelectUnit={setSelectedUnit}
          />
        </aside>

        {/* Chat Area */}
        <main className="flex-1 flex flex-col bg-gray-50">
          {selectedUnit ? (
            <>
              {/* Unit Header */}
              <div className="bg-white border-b px-6 py-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  {selectedUnit.title}
                </h2>
                <p className="text-sm text-gray-600 mt-1">
                  {selectedUnit.objectives.join(" • ")}
                </p>
              </div>

              {/* Messages */}
              <MessageList messages={messages} />

              {/* Input */}
              <MessageInput onSend={handleSendMessage} disabled={isLoading} />
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              <p>Select a unit to start learning</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
