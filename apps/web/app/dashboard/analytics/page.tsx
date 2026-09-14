import React from 'react';

export default async function AnalyticsPage() {
  const stats = {
    totalConversations: 142,
    totalTokens: 45200,
    averageLatency: "850ms",
    successRate: "94%"
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 md:p-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-gray-900">Analytics Dashboard</h2>
        <p className="text-gray-500 mt-2">Monitor your AI Receptionist's performance.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white border rounded-lg shadow-sm p-6">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="text-sm font-medium text-gray-900">Total Conversations</h3>
            <span className="text-gray-400">💬</span>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-900">{stats.totalConversations}</div>
            <p className="text-xs text-gray-500 mt-1">+20.1% from last month</p>
          </div>
        </div>
        
        <div className="bg-white border rounded-lg shadow-sm p-6">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="text-sm font-medium text-gray-900">Token Usage</h3>
            <span className="text-gray-400">⚡</span>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-900">{stats.totalTokens.toLocaleString()}</div>
            <p className="text-xs text-gray-500 mt-1">Est. Cost: ${(stats.totalTokens / 1000 * 0.002).toFixed(2)}</p>
          </div>
        </div>

        <div className="bg-white border rounded-lg shadow-sm p-6">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="text-sm font-medium text-gray-900">Avg. Latency</h3>
            <span className="text-gray-400">⏱️</span>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-900">{stats.averageLatency}</div>
            <p className="text-xs text-gray-500 mt-1">-50ms from last week</p>
          </div>
        </div>

        <div className="bg-white border rounded-lg shadow-sm p-6">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="text-sm font-medium text-gray-900">Resolution Rate</h3>
            <span className="text-gray-400">📈</span>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-900">{stats.successRate}</div>
            <p className="text-xs text-gray-500 mt-1">+2% from last week</p>
          </div>
        </div>
      </div>
      
    </div>
  );
}
