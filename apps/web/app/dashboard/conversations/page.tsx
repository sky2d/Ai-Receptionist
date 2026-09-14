"use client";

import { useEffect, useState } from "react";

export default function ConversationsDashboard() {
  const [conversations, setConversations] = useState([]);
  const [selectedConvo, setSelectedConvo] = useState(null);
  const [messages, setMessages] = useState([]);
  const [replyText, setReplyText] = useState("");

  const businessId = "demo_business_123"; // MOCKED for Phase 11 scaffolding

  useEffect(() => {
    fetch(`/api/human/conversations/escalated?business_id=${businessId}`)
      .then((res) => res.json())
      .then((data) => setConversations(data.conversations || []))
      .catch((err) => console.error(err));
  }, []);

  const loadConversation = (id) => {
    fetch(`/api/human/conversations/${id}/messages`)
      .then((res) => res.json())
      .then((data) => {
        setMessages(data.messages || []);
        setSelectedConvo(id);
      })
      .catch((err) => console.error(err));
  };

  const sendReply = (resolve = false) => {
    if (!replyText.trim()) return;
    
    fetch(`/api/human/conversations/${selectedConvo}/reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: replyText, resolve })
    }).then(() => {
      setReplyText("");
      loadConversation(selectedConvo);
      if (resolve) {
        setConversations(conversations.filter((c: any) => c.id !== selectedConvo));
        setSelectedConvo(null);
      }
    });
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] bg-white border rounded-lg overflow-hidden shadow-sm">
      {/* Sidebar: Escalated Conversations */}
      <div className="w-1/3 border-r bg-gray-50 flex flex-col">
        <div className="p-4 border-b bg-white">
          <h2 className="text-lg font-bold text-red-600 flex items-center">
            <span className="w-2 h-2 bg-red-600 rounded-full mr-2 animate-pulse"></span>
            Escalated Needs Attention
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="p-4 text-sm text-gray-500 italic text-center mt-4">
              No escalated conversations.
            </div>
          ) : (
            conversations.map((c: any) => (
              <div 
                key={c.id} 
                onClick={() => loadConversation(c.id)}
                className={`p-4 border-b cursor-pointer hover:bg-gray-100 transition-colors ${selectedConvo === c.id ? 'bg-blue-50 border-blue-200 border-l-4 border-l-blue-600' : 'border-l-4 border-l-transparent'}`}
              >
                <div className="font-semibold text-gray-800 text-sm">Conv: {c.id.substring(0, 8)}...</div>
                <div className="text-xs text-gray-500 mt-1">
                  Channel: <span className="uppercase font-medium text-gray-700">{c.channel}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Area: Chat Window */}
      <div className="w-2/3 flex flex-col bg-white">
        {selectedConvo ? (
          <>
            <div className="p-4 border-b bg-gray-50 flex justify-between items-center">
              <span className="font-semibold text-sm text-gray-700">Chat History</span>
              <span className="bg-red-100 text-red-700 text-xs px-2 py-1 rounded-full uppercase font-bold tracking-wider">Escalated</span>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white">
              {messages.map((m: any) => (
                <div key={m.id} className={`flex ${m.sender === 'user' ? 'justify-start' : 'justify-end'}`}>
                  <div className={`p-3 rounded-xl max-w-[75%] shadow-sm text-sm ${
                    m.sender === 'user' 
                      ? 'bg-gray-100 text-gray-800 rounded-tl-sm' 
                      : m.content.startsWith('[Human]') 
                        ? 'bg-emerald-600 text-white rounded-tr-sm' 
                        : 'bg-blue-600 text-white rounded-tr-sm'
                  }`}>
                    <div className="text-[10px] opacity-75 mb-1 font-semibold uppercase tracking-wider">
                      {m.sender === 'user' ? 'Customer' : m.content.startsWith('[Human]') ? 'You (Human)' : 'AI Agent'}
                    </div>
                    <div className="whitespace-pre-wrap">{m.content.replace('[Human] ', '')}</div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="p-4 border-t bg-gray-50 flex gap-2">
              <input 
                type="text"
                className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder="Type your message as a human agent..."
                onKeyDown={(e) => e.key === 'Enter' && sendReply(false)}
              />
              <button 
                onClick={() => sendReply(false)}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                Send
              </button>
              <button 
                onClick={() => sendReply(true)}
                className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-md hover:bg-emerald-700 transition-colors focus:ring-2 focus:ring-emerald-500 focus:outline-none whitespace-nowrap"
              >
                Send & Resolve
              </button>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-400 bg-gray-50/50">
             <svg className="w-12 h-12 mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
             </svg>
             <p className="text-sm font-medium">Select a conversation to intercept</p>
          </div>
        )}
      </div>
    </div>
  );
}
