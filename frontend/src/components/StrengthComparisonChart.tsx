'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface StrengthComparisonChartProps {
  data: {
    offensive_strength: number;
    defensive_strength: number;
  };
}

export default function StrengthComparisonChart({ data }: StrengthComparisonChartProps) {
  const chartData = [
    { name: 'Offensive Strength', value: data.offensive_strength, fill: '#ef4444' },
    { name: 'Defensive Strength', value: data.defensive_strength, fill: '#3b82f6' }
  ];

  return (
    <div className="bg-black border border-green-800 rounded-lg p-4">
      <h3 className="text-green-400 font-semibold text-lg mb-4">Strength Comparison Analysis</h3>
      
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData}>
          <XAxis 
            dataKey="name" 
            stroke="#00ff88" 
            tick={{ fill: '#00ff88' }}
          />
          <YAxis 
            stroke="#00ff88" 
            tick={{ fill: '#00ff88' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'rgba(0, 0, 0, 0.8)', 
              border: '1px solid #00ff88',
              borderRadius: '4px'
            }}
            formatter={(value: any, name: any) => (
              <div className="text-xs">
                <div className="font-semibold">{name}</div>
                <div>Score: {value.toFixed(2)}</div>
              </div>
            )}
          />
          <Bar 
            dataKey="value" 
            fill="#00ff88"
            radius={[4, 4, 0, 0]}
          />
          <Legend />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
