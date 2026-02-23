import React, { useState, useCallback } from 'react';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  onUpload: (file: File, constitution: string) => void;
  className?: string;
  disabled?: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ 
  onFileSelect, 
  onUpload, 
  className = '',
  disabled = false 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!disabled) {
      setIsDragging(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, [disabled]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0 && !disabled) {
      const file = files[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  }, [onFileSelect, disabled]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0 && !disabled) {
      const file = files[0];
      setSelectedFile(file);
      onFileSelect(file);
    }
  };

  const handleUploadClick = () => {
    if (selectedFile && !disabled) {
      onUpload(selectedFile, 'India'); // Default constitution
    }
  };

  return (
    <div 
      className={`
        relative border-2 border-dashed rounded-xl p-8 transition-all duration-300
        ${disabled 
          ? 'border-gray-700 bg-gray-900 cursor-not-allowed opacity-50' 
          : isDragging 
            ? 'border-green-400 bg-green-950 bg-green-950/10' 
            : 'border-green-800 bg-black hover:border-green-600 hover:bg-green-950/20'
        }
        ${className}
      `}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {/* Upload Icon */}
      <div className="text-center mb-4">
        <div className={`
          w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300
          ${disabled ? 'bg-gray-700' : 'bg-gray-800'}
        `}>
          <svg 
            className={`w-8 h-8 ${disabled ? 'text-gray-500' : 'text-green-400'}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M7 16a4 4 0 014-4 4 0M21 12a9 9 0 11-18 0 011-18 0M3 12a4 4 0 014-4 4 0" 
            />
          </svg>
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
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
        disabled={disabled}
      />

      {/* Selected File Preview */}
      {selectedFile && (
        <div className="mt-6 p-4 bg-gray-900 border border-gray-700 rounded-lg">
          <h4 className="text-green-400 font-semibold mb-2">Selected File</h4>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gray-700 rounded-lg flex items-center justify-center">
              <span className="text-gray-400 text-xl">
                {selectedFile.type?.startsWith('image/') ? '🖼️' : '📄'}
              </span>
            </div>
            <div className="flex-1">
              <p className="text-white font-medium truncate">{selectedFile.name}</p>
              <p className="text-gray-500 text-sm">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUploadClick}
        disabled={!selectedFile || disabled}
        className="w-full mt-6 bg-black border border-green-500 text-green-400 py-3 rounded-lg font-semibold hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_25px_rgba(0,255,136,0.4)] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        📤 Upload Document for Analysis
      </button>
    </div>
  );
};

export default UploadZone;
