import React from 'react';
import DocumentViewerSimple from './DocumentViewerSimple';
import ClauseList from './ClauseList';
import { Clause } from '../types';

interface AnalysisLayoutProps {
  documentText: string;
  clauses: Clause[];
  selectedClauseId?: string;
  onClauseSelect?: (clauseId: string) => void;
  className?: string;
}

export const AnalysisLayout: React.FC<AnalysisLayoutProps> = ({ 
  documentText, 
  clauses, 
  selectedClauseId,
  onClauseSelect,
  className = ''
}) => {
  return (
    <div className={`min-h-screen bg-black ${className}`}>
      <div className="flex h-full">
        {/* Left Side - Document Viewer */}
        <div className="w-1/2 border-r border-green-900 bg-gray-950 p-6 overflow-y-auto">
          <DocumentViewerSimple
            documentText={documentText}
            clauses={clauses}
          />
        </div>

        {/* Right Side - Clause Analysis Panel */}
        <div className="w-1/2 bg-black p-6 overflow-y-auto">
          <div className="max-w-4xl mx-auto">
            <div className="mb-6">
              <h2 className="text-green-400 font-bold text-2xl mb-2">
                Clause Analysis
              </h2>
              <p className="text-gray-500 text-sm mb-6">
                {clauses.length} clauses analyzed • Select any clause for detailed insights
              </p>
            </div>

            {/* Selected Clause Details */}
            {selectedClauseId && (
              <div className="mb-8">
                {(() => {
                  const selectedClause = clauses.find(c => c.clause_id === selectedClauseId);
                  if (!selectedClause) return null;

                  return (
                    <div className="bg-black border border-green-500 rounded-xl p-6 hover:shadow-[0_0_20px_rgba(0,255,136,0.2)] transition-all duration-300">
                      {/* Clause Header */}
                      <div className="border-b border-green-900 pb-4 mb-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-green-400 text-sm font-mono bg-green-950 px-2 py-1 rounded">
                            {selectedClause.type?.toUpperCase() || 'UNKNOWN'}
                          </span>
                          <div className="flex items-center gap-2">
                            <span className="text-gray-500 text-xs">
                              #{selectedClause.rank}
                            </span>
                            <div 
                              className="px-2 py-1 rounded text-xs font-semibold"
                              style={{ 
                                backgroundColor: selectedClause.color + '20',
                                color: 'white'
                              }}
                            >
                              {selectedClause.risk_level?.toUpperCase() || 'UNKNOWN'}
                            </div>
                            <span className="text-gray-500 text-xs">
                              Priority: {selectedClause.priority_score?.toFixed(1) || '0.0'}
                            </span>
                          </div>
                        </div>
                        
                        <h3 className="text-white font-semibold text-lg mb-3">
                          Clause Text
                        </h3>
                        <p className="text-gray-300 leading-relaxed mb-4">
                          {selectedClause.text}
                        </p>
                      </div>

                      {/* Constitution Reference */}
                      {selectedClause.constitution_reference && (
                        <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 mb-4">
                          <h4 className="text-green-400 text-sm font-semibold mb-2">
                            📜 Constitution Reference
                          </h4>
                          <p className="text-green-300 text-sm font-mono">
                            {selectedClause.constitution_reference}
                          </p>
                        </div>
                      )}

                      {/* Explanation */}
                      {selectedClause.explanation && (
                        <div className="mb-4">
                          <h4 className="text-green-400 text-sm font-semibold mb-2">
                            📋 Explanation
                          </h4>
                          <p className="text-gray-300 leading-relaxed text-sm">
                            {selectedClause.explanation}
                          </p>
                        </div>
                      )}

                      {/* Offensive Analysis */}
                      {selectedClause.offensive_analysis && (
                        <div className="mb-4">
                          <h4 className="text-red-400 text-sm font-semibold mb-2">
                            ⚔️ Offensive Analysis
                          </h4>
                          <p className="text-gray-300 leading-relaxed text-sm">
                            {selectedClause.offensive_analysis}
                          </p>
                        </div>
                      )}

                      {/* Defensive Analysis */}
                      {selectedClause.defensive_analysis && (
                        <div className="mb-4">
                          <h4 className="text-blue-400 text-sm font-semibold mb-2">
                            🛡️ Defensive Analysis
                          </h4>
                          <p className="text-gray-300 leading-relaxed text-sm">
                            {selectedClause.defensive_analysis}
                          </p>
                        </div>
                      )}

                      {/* Action Buttons */}
                      <div className="flex gap-3 pt-4 border-t border-green-900">
                        <button className="flex-1 bg-gray-800 border border-green-800 text-green-400 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200">
                          🤖 Ask AI About This Clause
                        </button>
                        <button className="flex-1 bg-gray-800 border border-green-800 text-green-400 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200">
                          💬 Discuss with Legal Expert
                        </button>
                      </div>
                    </div>
                  );
                })()}
              </div>
            )}

            {/* All Clauses List */}
            <div>
              <h3 className="text-green-400 font-semibold text-lg mb-4">
                All Clauses
              </h3>
              <ClauseList
                clauses={clauses}
                selectedClauseId={selectedClauseId}
                onClauseSelect={onClauseSelect}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisLayout;
