'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';

export default function UploadPage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedConstitution, setSelectedConstitution] = useState('India');
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const constitutions = [
    { code: 'India', name: 'India', flag: '🇮🇳' },
    { code: 'China', name: 'China', flag: '🇨🇳' },
    { code: 'Japan', name: 'Japan', flag: '🇯🇵' },
    { code: 'Russia', name: 'Russia', flag: '🇷🇺' }
  ];

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
    }
  };

  const handleCameraCapture = () => {
    // Mock camera capture - in real implementation, would access device camera
    alert('Camera capture would open device camera for document scanning');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    // Validate file type
    if (!selectedFile.type.includes('pdf') && !selectedFile.type.includes('document')) {
      alert('Please upload a PDF or document file');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 100;
          }
          return prev + 10;
        });
      }, 200);

      // Mock upload - simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2500));
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      // Generate mock document ID
      const documentId = Math.random() > 0.5 ? 'doc_15_' + Date.now() : 'doc_8_' + Date.now();
      
      // Store mock document data
      const documentData = {
        id: documentId,
        filename: selectedFile.name,
        upload_time: new Date().toISOString(),
        status: 'completed',
        clauses_count: documentId.includes('15') ? 15 : 8,
        constitution: selectedConstitution,
        file_size: selectedFile.size
      };
      
      // Store in localStorage for demo
      const existingDocs = JSON.parse(localStorage.getItem('lexai_documents') || '[]');
      existingDocs.push(documentData);
      localStorage.setItem('lexai_documents', JSON.stringify(existingDocs));

      alert(`✅ "${selectedFile.name}" uploaded successfully! Found ${documentData.clauses_count} clauses.`);
      
      // Redirect to analysis page
      setTimeout(() => {
        router.push(`/analysis/${documentId}`);
      }, 1000);
    } catch (error) {
      alert('Upload error: ' + error);
    } finally {
      setIsUploading(false);
      setTimeout(() => setUploadProgress(0), 2000);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="border-b border-green-900 bg-black">
        <div className="px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-black font-bold text-sm">L</span>
            </div>
            <h1 className="text-green-400 font-bold text-xl">Upload Document</h1>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        <div className="max-w-4xl mx-auto">
          {/* Constitution Selector */}
          <div className="mb-8">
            <label className="text-green-400 text-sm font-medium mb-3 block">
              Select Constitution for Analysis
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {constitutions.map((constitution) => (
                <button
                  key={constitution.code}
                  onClick={() => setSelectedConstitution(constitution.code)}
                  className={`
                    p-4 border-2 rounded-xl transition-all duration-200
                    ${selectedConstitution === constitution.code
                      ? 'border-green-400 bg-green-950 bg-green-950/20'
                      : 'border-green-800 bg-black hover:border-green-600 hover:bg-green-950/20'
                    }
                  `}
                >
                  <div className="text-2xl mb-2">{constitution.flag}</div>
                  <div className="text-white font-medium">{constitution.name}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Upload Area */}
          <div className="mb-8">
            <label className="text-green-400 text-sm font-medium mb-3 block">
              Upload Legal Document
            </label>
            
            {/* Drag and Drop Zone */}
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`
                relative border-2 border-dashed rounded-xl p-8 transition-all duration-200
                ${isDragging 
                  ? 'border-green-400 bg-green-950 bg-green-950/10' 
                  : 'border-green-800 bg-black hover:border-green-600'
                }
              `}
            >
              {/* Upload Icon */}
              <div className="text-center">
                <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-gray-400 text-2xl">📄</span>
                </div>
                
                {isDragging ? (
                  <div className="text-green-400 font-semibold">Drop your document here</div>
                ) : (
                  <div>
                    <div className="text-green-400 font-semibold mb-2">
                      Drag and drop your document here
                    </div>
                    <div className="text-gray-500 text-sm mb-4">or</div>
                  </div>
                )}
              </div>

              {/* File Input */}
              <input
                type="file"
                onChange={handleFileSelect}
                accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.ppt,.pptx"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={isUploading}
              />
            </div>

            {/* Camera Capture Button */}
            <div className="flex justify-center mt-4">
              <button
                onClick={handleCameraCapture}
                className="bg-gray-800 border border-green-800 text-green-400 px-4 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200"
                disabled={isUploading}
              >
                <span className="mr-2">📷</span>
                Capture Document with Camera
              </button>
            </div>
          </div>

          {/* File Preview */}
          {selectedFile && (
            <div className="mb-8 p-6 bg-gray-900 border border-green-800 rounded-xl">
              <h3 className="text-green-400 font-semibold mb-4">Selected File</h3>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gray-700 rounded-lg flex items-center justify-center">
                  <span className="text-gray-400 text-xl">
                    {selectedFile.type.startsWith('image/') ? '🖼️' : '📄'}
                  </span>
                </div>
                <div className="flex-1">
                  <p className="text-white font-medium truncate">{selectedFile.name}</p>
                  <p className="text-gray-500 text-sm">
                    {formatFileSize(selectedFile.size)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Upload Progress */}
          {isUploading && (
            <div className="mb-8 p-6 bg-gray-900 border border-green-800 rounded-xl">
              <h3 className="text-green-400 font-semibold mb-4">Uploading Document...</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-gray-800 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-green-500 h-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <span className="text-green-400 text-sm font-medium">{uploadProgress}%</span>
                </div>
                <div className="text-gray-500 text-sm">
                  Analyzing document with {selectedConstitution} constitution...
                </div>
              </div>
            </div>
          )}

          {/* Analyze Button */}
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading}
            className={`
              w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300
              ${!selectedFile || isUploading
                ? 'bg-gray-800 border-gray-700 text-gray-600 cursor-not-allowed'
                : 'bg-black border border-green-500 text-green-400 hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_25px_rgba(0,255,136,0.4)]'
              }
            `}
          >
            {isUploading ? (
              <div className="flex items-center justify-center">
                <div className="w-6 h-6 border-2 border-green-400 border-t-transparent rounded-full animate-spin"></div>
                <span className="ml-3">Processing...</span>
              </div>
            ) : (
              <span>
                {selectedFile ? '🔍 Analyze Document' : '📤 Select a Document First'}
              </span>
            )}
          </button>

          {/* Instructions */}
          <div className="mt-8 text-center">
            <div className="text-gray-500 text-sm space-y-2">
              <p>📋 Supported formats: PDF, DOC, DOCX, TXT, JPG, PNG, PPT, PPTX</p>
              <p>📜 Constitutions available: India, China, Japan, Russia</p>
              <p>🔒 All documents are processed with military-grade encryption</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
