import React, { useState } from 'react';
import { Clause } from '../types';

interface DocumentViewerProps {
  documentText: string;
  clauses: Clause[];
  selectedClauseId?: string;
  onClauseSelect?: (clauseId: string) => void;
  className?: string;
}

export const DocumentViewerSimple: React.FC<DocumentViewerProps> = ({ 
  documentText, 
  clauses, 
  selectedClauseId,
  onClauseSelect,
  className = ''
}) => {
  const [hoveredClauseId, setHoveredClauseId] = useState<string | null>(null);

  const handleClauseClick = (clause: Clause) => {
    if (onClauseSelect) {
      onClauseSelect(clause.clause_id);
    }
  };

  return (
    <div className={`bg-black border border-green-900 rounded-xl p-6 ${className}`}>
      <div className="mb-6">
        <h2 className="text-green-400 font-bold text-xl mb-2">Document Viewer</h2>
        <p className="text-gray-500 text-sm">
          {clauses.length} clauses found • Click any clause to analyze
        </p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-6 mb-6">
        <div className="max-h-96 overflow-y-auto">
          <div 
            className="text-white text-sm leading-relaxed whitespace-pre-wrap"
            dangerouslySetInnerHTML={{ 
              __html: documentText 
            }}
          />
        </div>
      </div>

      <div className="border-t border-green-900 pt-4">
        <h3 className="text-green-400 font-semibold text-sm mb-3">Clause Color Legend</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span className="text-gray-400 text-xs">High Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
            <span className="text-gray-400 text-xs">Medium Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 rounded"></div>
            <span className="text-gray-400 text-xs">Low Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-500 rounded"></div>
            <span className="text-gray-400 text-xs">Unknown Risk</span>
          </div>
        </div>
      </div>

      {clauses.length > 0 && (
        <div className="border-t border-green-900 pt-4">
          <h3 className="text-green-400 font-semibold text-sm mb-3">Interactive Clauses</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {clauses.map((clause) => {
              const key = clause.clause_id;
              const isSelected = selectedClauseId === key;
              
              return (
                <div key={key}>
                  <div
                    onClick={() => handleClauseClick(clause)}
                    onMouseEnter={() => setHoveredClauseId(key)}
                    onMouseLeave={() => setHoveredClauseId(null)}
                    className={`
                      p-3 rounded-lg border-2 cursor-pointer transition-all duration-200
                      ${isSelected 
                        ? 'border-green-400 bg-green-950' 
                        : 'border-gray-700 hover:border-green-600 hover:bg-gray-900'
                      }
                    `}
                    style={{
                      borderLeftColor: clause.color,
                      borderLeftWidth: '4px'
                    }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-green-400 text-xs font-mono bg-green-950 px-2 py-1 rounded">
                          {clause.type?.toUpperCase() || 'UNKNOWN'}
                        </span>
                        <span className="text-gray-500 text-xs">
                          #{clause.rank}
                        </span>
                        <div 
                          className="px-2 py-1 rounded text-xs font-semibold"
                          style={{ 
                            backgroundColor: clause.color + '20',
                            color: 'white'
                          }}
                        >
                          {clause.risk_level?.toUpperCase() || 'UNKNOWN'}
                        </div>
                      </div>
                    </div>
                  </div>
                  <p className="text-gray-300 text-sm leading-relaxed">
                    {clause.text}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="text-center text-gray-500 text-xs mt-4">
        <p>💡 Click on any highlighted clause in the document to see detailed analysis</p>
        <p>🎨 Hover over clauses to preview them</p>
      </div>
    </div>
  );
};

export default DocumentViewerSimple;
