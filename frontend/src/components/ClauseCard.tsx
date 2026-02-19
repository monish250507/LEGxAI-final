import React from 'react';
import { Clause } from '../types';
import { Button } from './ui/button';
import { getRiskColor, getRiskBgColor, truncateText } from '../utils';

interface ClauseCardProps {
  clause: Clause;
  onAnalyze?: (clause: Clause) => void;
  className?: string;
}

export const ClauseCard: React.FC<ClauseCardProps> = ({ 
  clause, 
  onAnalyze, 
  className = '' 
}) => {
  const riskColor = getRiskColor(clause.risk_level);
  const riskBgColor = getRiskBgColor(clause.risk_level);

  return (
    <div 
      className={`
        bg-black border border-green-500 rounded-lg p-4 mb-4
        hover:shadow-[0_0_15px_rgba(0,255,136,0.3)] 
        transition-all duration-300 cursor-pointer
        ${className}
      `}
      onClick={() => onAnalyze?.(clause)}
    >
      {/* Header with type and risk level */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2">
          <span className="text-green-400 text-xs font-mono bg-green-950 px-2 py-1 rounded">
            {clause.type?.toUpperCase() || 'UNKNOWN'}
          </span>
          <span className="text-gray-400 text-xs">
            Rank #{clause.rank}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">
            Priority: {clause.priority_score?.toFixed(1) || '0.0'}
          </span>
          <div 
            className={`
              px-2 py-1 rounded text-xs font-semibold
              ${riskBgColor}
            `}
            style={{ color: riskColor }}
          >
            {clause.risk_level?.toUpperCase() || 'UNKNOWN'}
          </div>
        </div>
      </div>

      {/* Clause Text */}
      <div className="mb-4">
        <p className="text-white text-sm leading-relaxed">
          {truncateText(clause.text, 200)}
        </p>
      </div>

      {/* Constitution Reference */}
      {clause.constitution_reference && (
        <div className="mb-4 p-2 bg-gray-900 rounded border border-gray-700">
          <p className="text-green-400 text-xs font-mono">
            📜 {clause.constitution_reference}
          </p>
        </div>
      )}

      {/* Explanation */}
      {clause.explanation && (
        <div className="mb-4">
          <h4 className="text-green-400 text-sm font-semibold mb-2">
            📋 Explanation
          </h4>
          <p className="text-gray-300 text-sm leading-relaxed">
            {truncateText(clause.explanation, 300)}
          </p>
        </div>
      )}

      {/* Offensive Analysis */}
      {clause.offensive_analysis && (
        <div className="mb-4">
          <h4 className="text-red-400 text-sm font-semibold mb-2">
            ⚔️ Offensive Analysis
          </h4>
          <p className="text-gray-300 text-sm leading-relaxed">
            {truncateText(clause.offensive_analysis, 300)}
          </p>
        </div>
      )}

      {/* Defensive Analysis */}
      {clause.defensive_analysis && (
        <div className="mb-4">
          <h4 className="text-blue-400 text-sm font-semibold mb-2">
            🛡️ Defensive Analysis
          </h4>
          <p className="text-gray-300 text-sm leading-relaxed">
            {truncateText(clause.defensive_analysis, 300)}
          </p>
        </div>
      )}

      {/* Action Button */}
      {onAnalyze && (
        <div className="mt-4">
          <Button 
            variant="outline"
            size="sm"
            onClick={() => onAnalyze(clause)}
            className="w-full"
          >
            🔍 Analyze in Context
          </Button>
        </div>
      )}
    </div>
  );
};

export default ClauseCard;
