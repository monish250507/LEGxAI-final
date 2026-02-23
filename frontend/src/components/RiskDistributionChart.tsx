'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface RiskDistributionChartProps {
  data: {
    high: number;
    medium: number;
    low: number;
  };
}

export default function RiskDistributionChart({ data }: RiskDistributionChartProps) {
  const chartData = [
    { name: 'High Risk', value: data.high, fill: '#ef4444' },
    { name: 'Medium Risk', value: data.medium, fill: '#f59e0b' },
    { name: 'Low Risk', value: data.low, fill: '#00ff88' }
  ];

  return (
    <div className="bg-black border border-green-800 rounded-lg p-4">
      <h3 className="text-green-400 font-semibold text-lg mb-4">Risk Distribution Analysis</h3>
      
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
                <div className="text-green-400">Count: {value}</div>
              </div>
            )}
          />
          <Bar 
            dataKey="value" 
            fill="#00ff88"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
