'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to chat page
    router.push('/chat');
  }, [router]);

  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="text-center">
        <div className="text-6xl mb-4">🗺️</div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Travel Recommender
        </h1>
        <p className="text-gray-600">Перенаправлення на чат...</p>
      </div>
    </div>
  );
}
