import React from 'react';
import { Clause } from '../types';
import ClauseCard from './ClauseCard';

interface ClauseListProps {
  clauses: Clause[];
  selectedClauseId?: string;
  onClauseSelect?: (clauseId: string) => void;
  className?: string;
}

export const ClauseList: React.FC<ClauseListProps> = ({ 
  clauses, 
  selectedClauseId,
  onClauseSelect,
  className = ''
}) => {
  if (!clauses || clauses.length === 0) {
    return (
      <div className={`text-center py-12 ${className}`}>
        <div className="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-gray-500 text-3xl">📄</span>
        </div>
        <h3 className="text-gray-400 text-lg font-semibold mb-2">No clauses found</h3>
        <p className="text-gray-500 text-sm">
          Upload a document to see clause analysis
        </p>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="mb-6">
        <h2 className="text-green-400 font-bold text-xl mb-2">
          Clause Analysis ({clauses.length} clauses)
        </h2>
        <p className="text-gray-500 text-sm">
          Click any clause to see detailed analysis and AI insights
        </p>
      </div>

      <div className="space-y-4">
        {clauses.map((clause) => (
          <ClauseCard
            key={clause.clause_id}
            clause={clause}
            onAnalyze={() => onClauseSelect?.(clause.clause_id)}
            className={
              selectedClauseId === clause.clause_id 
                ? 'ring-2 ring-green-400 ring-offset-2' 
                : ''
            }
          />
        ))}
      </div>

      {/* Summary Stats */}
      <div className="border-t border-green-900 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-black border border-green-900 rounded-lg p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">
                {clauses.filter(c => c.risk_level === 'high').length}
              </div>
              <div className="text-gray-500 text-sm">High Risk</div>
            </div>
          </div>
          <div className="bg-black border border-green-900 rounded-lg p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-400 mb-2">
                {clauses.filter(c => c.risk_level === 'medium').length}
              </div>
              <div className="text-gray-500 text-sm">Medium Risk</div>
            </div>
          </div>
          <div className="bg-black border border-green-900 rounded-lg p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">
                {clauses.filter(c => c.risk_level === 'low').length}
              </div>
              <div className="text-gray-500 text-sm">Low Risk</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClauseList;
