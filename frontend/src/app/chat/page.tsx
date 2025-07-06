'use client';

import { useState } from 'react';
import Link from 'next/link';
import ChatTab from '../components/ChatTab';

interface Place {
  name: string;
  description: string;
  coords: {
    lat: number;
    lng: number;
  };
}

interface Recommendation {
  id: number;
  text: string;
  exclude: string[];
  num_places: number;
  response_json: Place[];
  created_at: string;
}

export default function ChatPage() {
  const [chatRecommendations, setChatRecommendations] = useState<Recommendation[]>([]);

  const handleNewRecommendation = (rec: Recommendation) => {
    setChatRecommendations(prev => [rec, ...prev]);
  };

  const handleClearAll = () => {
    setChatRecommendations([]);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🗺️ Travel Recommender
          </h1>
          <p className="text-gray-700">
            Отримай персональні туристичні рекомендації з штучним інтелектом
          </p>
        </div>

        {/* Navigation */}
        <div className="bg-white border-b border-gray-200 mb-6">
          <div className="max-w-4xl mx-auto px-4">
            <div className="flex space-x-8">
              <Link
                href="/chat"
                className="py-4 px-1 border-b-2 font-medium text-sm border-blue-500 text-blue-600"
              >
                💬 Чат
              </Link>
              <Link
                href="/history"
                className="py-4 px-1 border-b-2 font-medium text-sm border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              >
                📚 Історія
              </Link>
            </div>
          </div>
        </div>

        {/* Chat Content */}
        <ChatTab
          recommendations={chatRecommendations}
          onNewRecommendation={handleNewRecommendation}
          onClearAll={handleClearAll}
        />
      </div>
    </div>
  );
} 