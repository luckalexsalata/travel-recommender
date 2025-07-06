'use client';

import { useState } from 'react';

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

interface ChatTabProps {
  recommendations: Recommendation[];
  onNewRecommendation: (rec: Recommendation) => void;
  onClearAll: () => void;
}

export default function ChatTab({ recommendations, onNewRecommendation, onClearAll }: ChatTabProps) {
  const [message, setMessage] = useState('');
  const [numPlaces, setNumPlaces] = useState(3);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/recommendations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: message,
          num_places: numPlaces,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        onNewRecommendation(result);
        setMessage('');
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header with Clear All button */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Чат з AI</h2>
        {recommendations.length > 0 && (
          <button
            onClick={onClearAll}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors text-sm"
          >
            🗑️ Очистити всі
          </button>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex flex-col space-y-4">
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">
              Кількість місць:
            </label>
            <select
              value={numPlaces}
              onChange={(e) => setNumPlaces(Number(e.target.value))}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm text-gray-700"
            >
              <option value={2}>2</option>
              <option value={3}>3</option>
              <option value={4}>4</option>
              <option value={5}>5</option>
            </select>
          </div>
          
          <div className="flex space-x-4 text-gray-900">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Напиши, куди хочеш поїхати... (наприклад: 'Хочу в Рим, люблю історію та макарони')"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !message.trim()}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="space-y-6">
        {recommendations.map((rec, index) => (
          <div key={rec.id} className="space-y-4">
            {/* User Message */}
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                👤
              </div>
              <div className="flex-1 bg-blue-600 text-white rounded-lg p-4">
                <p className="font-medium mb-1">Ти:</p>
                <p>{rec.text}</p>
              </div>
            </div>

            {/* AI Response */}
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                🤖
              </div>
              <div className="flex-1 bg-gray-100 rounded-lg p-4">
                <p className="text-gray-900 font-medium mb-3">AI:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {rec.response_json.map((place, placeIndex) => (
                    <div
                      key={placeIndex}
                      className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <h3 className="font-semibold text-lg text-gray-900 mb-2">
                        {place.name}
                      </h3>
                      <p className="text-gray-700 text-sm mb-2">
                        {place.description}
                      </p>
                      <div className="text-xs text-gray-500">
                        📍 {place.coords.lat.toFixed(4)}, {place.coords.lng.toFixed(4)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Exclusions */}
            {rec.exclude.length > 0 && (
              <div className="ml-11 p-3 bg-red-50 rounded-lg">
                <p className="text-sm text-red-700 font-medium mb-1">
                  Виключені місця:
                </p>
                <div className="flex flex-wrap gap-2">
                  {rec.exclude.map((exclusion, exclusionIndex) => (
                    <span
                      key={exclusionIndex}
                      className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs"
                    >
                      ❌ {exclusion}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Timestamp */}
            <div className="ml-11 text-xs text-gray-500">
              {new Date(rec.created_at).toLocaleString('uk-UA')}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {recommendations.length === 0 && (
        <div className="text-center py-12">
          {/* <p className="text-gray-700">
            Напиши, куди хочеш поїхати, і я порекомендую тобі найкращі місця
          </p> */}
        </div>
      )}
    </div>
  );
} 