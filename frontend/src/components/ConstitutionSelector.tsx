import React from 'react';

interface Constitution {
  code: string;
  name: string;
  flag: string;
}

interface ConstitutionSelectorProps {
  selectedConstitution: string;
  onConstitutionChange: (constitution: string) => void;
  className?: string;
}

export const ConstitutionSelector: React.FC<ConstitutionSelectorProps> = ({ 
  selectedConstitution, 
  onConstitutionChange, 
  className = ''
}) => {
  const constitutions: Constitution[] = [
    { code: 'India', name: 'India', flag: '🇮🇳' },
    { code: 'China', name: 'China', flag: '🇨🇳' },
    { code: 'Japan', name: 'Japan', flag: '🇯🇵' },
    { code: 'Russia', name: 'Russia', flag: '🇷🇺' }
  ];

  return (
    <div className={`space-y-2 ${className}`}>
      <label className="text-green-400 text-sm font-medium mb-3 block">
        Select Constitution for Analysis
      </label>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {constitutions.map((constitution) => (
          <button
            key={constitution.code}
            onClick={() => onConstitutionChange(constitution.code)}
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
  );
};

export default ConstitutionSelector;
