'use client';

import { useState, useEffect } from 'react';

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

interface HistoryTabProps {
  onDeleteRecommendation: (id: number) => void;
}

export default function HistoryTab({ onDeleteRecommendation }: HistoryTabProps) {
  const [history, setHistory] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/recommendations/history');
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      } else {
        console.error('Error fetching history:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/recommendations/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setHistory(prev => prev.filter(rec => rec.id !== id));
        onDeleteRecommendation(id);
      } else {
        console.error('Error deleting recommendation:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <div className="text-gray-500">Завантаження історії...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Історія рекомендацій</h2>
        <div className="text-sm text-gray-500">
          Всього: {history.length} запитів
        </div>
      </div>

      {/* History List */}
      <div className="space-y-6">
        {history.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-700">Історія порожня</p>
          </div>
        ) : (
          history.map((rec) => (
            <div key={rec.id} className="bg-white border border-gray-200 rounded-lg p-6">
              {/* Header with delete button */}
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      👤
                    </div>
                    <div className="flex-1 bg-blue-600 text-white rounded-lg p-3">
                      <p className="font-medium mb-1">Запит:</p>
                      <p>{rec.text}</p>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(rec.id)}
                  className="ml-4 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition-colors text-sm"
                >
                  🗑️
                </button>
              </div>

              {/* AI Response */}
              <div className="flex items-start space-x-3 mb-4">
                <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  🤖
                </div>
                <div className="flex-1 bg-gray-100 rounded-lg p-4">
                  <p className="text-gray-900 font-medium mb-3">AI відповідь:</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {rec.response_json.map((place, placeIndex) => (
                      <div
                        key={placeIndex}
                        className="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow"
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
                <div className="ml-11 p-3 bg-red-50 rounded-lg mb-4">
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

              {/* Metadata */}
              <div className="ml-11 flex justify-between items-center text-xs text-gray-500">
                <span>Кількість місць: {rec.num_places}</span>
                <span>{new Date(rec.created_at).toLocaleString('uk-UA')}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 