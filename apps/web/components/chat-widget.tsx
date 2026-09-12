"use client";

import { useState } from "react";

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 bg-primary text-primary-foreground p-4 rounded-full shadow-lg"
      >
        Chat with AI
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 w-80 h-[400px] bg-background border rounded-lg shadow-xl flex flex-col">
      <div className="p-3 border-b bg-primary text-primary-foreground flex justify-between items-center rounded-t-lg">
        <span className="font-semibold">AI Assistant</span>
        <button onClick={() => setIsOpen(false)} className="text-sm">Close</button>
      </div>
      
      <div className="flex-1 p-3 overflow-y-auto">
        {/* Chat messages will appear here */}
        <div className="text-sm text-muted-foreground text-center mt-10">
          Connecting to AI... (WIP)
        </div>
      </div>
      
      <div className="p-3 border-t">
        <input 
          type="text" 
          placeholder="Type a message..." 
          className="w-full p-2 border rounded-md text-sm"
          disabled
        />
      </div>
    </div>
  );
}
