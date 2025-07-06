'use client';

import Link from 'next/link';
import HistoryTab from '../components/HistoryTab';

export default function HistoryPage() {
  const handleDeleteRecommendation = (id: number) => {
    // This will be handled by the HistoryTab component
    console.log('Deleted recommendation:', id);
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
                className="py-4 px-1 border-b-2 font-medium text-sm border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              >
                💬 Чат
              </Link>
              <Link
                href="/history"
                className="py-4 px-1 border-b-2 font-medium text-sm border-blue-500 text-blue-600"
              >
                📚 Історія
              </Link>
            </div>
          </div>
        </div>

        {/* History Content */}
        <HistoryTab onDeleteRecommendation={handleDeleteRecommendation} />
      </div>
    </div>
  );
} 