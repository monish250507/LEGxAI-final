'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Document {
  id: string;
  filename: string;
  upload_time: string;
  status: 'processing' | 'completed' | 'error';
  clauses_count?: number;
  constitution?: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    // Check authentication and get user data
    const token = localStorage.getItem('lexai_token');
    const userData = localStorage.getItem('lexai_user');
    
    if (!token || !userData) {
      router.push('/login');
      return;
    }
    
    try {
      setUser(JSON.parse(userData));
    } catch (err) {
      console.error('Error parsing user data:', err);
      router.push('/login');
      return;
    }

    // Fetch recent analyses
    const fetchDocuments = async () => {
      try {
        // Get documents from localStorage (from uploads)
        const storedDocs = JSON.parse(localStorage.getItem('lexai_documents') || '[]');
        
        // Add some mock documents if none exist
        if (storedDocs.length === 0) {
          const mockDocuments: Document[] = [
            {
              id: 'demo_1',
              filename: 'Employment_Agreement.pdf',
              upload_time: '2024-01-15T10:30:00Z',
              status: 'completed',
              clauses_count: 12,
              constitution: 'India'
            },
            {
              id: 'demo_2',
              filename: 'Service_Contract.pdf',
              upload_time: '2024-01-14T15:45:00Z',
              status: 'completed',
              clauses_count: 8,
              constitution: 'USA'
            },
            {
              id: 'demo_3',
              filename: 'NDA_Document.pdf',
              upload_time: '2024-01-13T09:20:00Z',
              status: 'processing',
              clauses_count: 0,
              constitution: 'UK'
            }
          ];
          setDocuments(mockDocuments);
        } else {
          setDocuments(storedDocs);
        }
      } catch (error) {
        console.error('Error fetching documents:', error);
        // Fallback to mock data
        setDocuments([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-400';
      case 'processing':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-900/20';
      case 'processing':
        return 'bg-yellow-900/20';
      case 'error':
        return 'bg-red-900/20';
      default:
        return 'bg-gray-900/20';
    }
  };

  const handleDocumentClick = (documentId: string) => {
    router.push(`/analysis/${documentId}`);
  };

  const handleUpload = () => {
    router.push('/upload');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-green-400 text-lg">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="border-b border-green-900 bg-black">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-black font-bold text-sm">L</span>
              </div>
              <div>
                <h1 className="text-green-400 font-bold text-xl">LexAI Dashboard</h1>
                {user && (
                  <p className="text-gray-400 text-sm">Welcome back, {user.name}!</p>
                )}
              </div>
            </div>
            <button 
              onClick={handleUpload}
              className="bg-black border border-green-500 text-green-400 px-4 py-2 rounded-lg hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_15px_rgba(0,255,136,0.3)] transition-all duration-300"
            >
              📤 Upload New
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 bg-black border-r border-green-900 min-h-screen p-4">
          <div className="mb-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-black font-bold text-xl">L</span>
              </div>
              <div>
                <h2 className="text-green-400 font-bold text-lg">LexAI</h2>
                <p className="text-gray-500 text-xs">Legal Document Analysis</p>
              </div>
            </div>
          </div>

          <nav className="space-y-2">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: '📊' },
              { id: 'upload', label: 'Upload', icon: '📤' },
              { id: 'history', label: 'History', icon: '📜' },
              { id: 'settings', label: 'Settings', icon: '⚙️' }
            ].map((item) => (
              <button
                key={item.id}
                className="w-full text-left px-4 py-3 mb-1 bg-black border border-green-900 text-gray-300 rounded-lg hover:border-green-500 hover:text-green-400 transition-all duration-200"
                onClick={() => router.push(`/${item.id}`)}
              >
                <div className="flex items-center gap-3">
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                </div>
              </button>
            ))}
          </nav>
        </div>

        {/* Main Area */}
        <div className="flex-1 p-6">
          <div className="max-w-6xl mx-auto">
            <div className="mb-8">
              <h2 className="text-green-400 font-bold text-2xl mb-2">Recent Analyses</h2>
              <p className="text-gray-500 text-sm">Your latest document analyses</p>
            </div>

            {/* Documents Grid */}
            {documents.length === 0 ? (
              <div className="text-center py-16">
                <div className="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-gray-500 text-3xl">📄</span>
                </div>
                <h3 className="text-gray-400 text-lg font-semibold mb-2">No documents yet</h3>
                <p className="text-gray-500 text-sm mb-6">Upload your first legal document to get started</p>
                <button 
                  onClick={handleUpload}
                  className="bg-black border border-green-500 text-green-400 px-6 py-3 rounded-lg hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_20px_rgba(0,255,136,0.4)] transition-all duration-300"
                >
                  📤 Upload Document
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {documents.map((doc) => (
                  <div
                    key={doc.id}
                    onClick={() => handleDocumentClick(doc.id)}
                    className="bg-black border border-green-900 rounded-xl p-6 hover:border-green-500 hover:shadow-[0_0_20px_rgba(0,255,136,0.2)] transition-all duration-300 cursor-pointer"
                  >
                    {/* Document Icon */}
                    <div className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center mb-4">
                      <span className="text-gray-400 text-xl">📄</span>
                    </div>

                    {/* Document Info */}
                    <div className="space-y-3">
                      <h3 className="text-white font-semibold text-lg truncate">{doc.filename}</h3>
                      
                      <div className="flex items-center justify-between">
                        <span className="text-gray-500 text-sm">{doc.upload_time}</span>
                        <div className={`px-2 py-1 rounded text-xs font-medium ${getStatusBg(doc.status)}`}>
                          <span className={getStatusColor(doc.status)}>
                            {doc.status.toUpperCase()}
                          </span>
                        </div>
                      </div>

                      {doc.clauses_count !== undefined && (
                        <div className="flex items-center gap-4 text-sm">
                          <span className="text-gray-400">Clauses: {doc.clauses_count}</span>
                          {doc.constitution && (
                            <span className="text-green-400">📜 {doc.constitution}</span>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Action Button */}
                    <button className="w-full mt-4 bg-gray-800 border border-green-800 text-green-400 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200">
                      View Analysis →
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
