import React from 'react';
import { Button } from './ui/button';

interface SidebarProps {
  activeTab?: string;
  onTabChange?: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab = 'dashboard', onTabChange }) => {
  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '📊',
      description: 'View recent analyses'
    },
    {
      id: 'upload',
      label: 'Upload Document',
      icon: '📤',
      description: 'Analyze new documents'
    },
    {
      id: 'history',
      label: 'Analysis History',
      icon: '📜',
      description: 'Browse past analyses'
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: '⚙️',
      description: 'Configure preferences'
    }
  ];

  return (
    <div className="w-64 bg-black border-r border-green-900 min-h-screen p-4">
      {/* Logo */}
      <div className="mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
            <span className="text-black font-bold text-xl">L</span>
          </div>
          <div>
            <h1 className="text-green-400 font-bold text-lg">LexAI</h1>
            <p className="text-gray-500 text-xs">Legal Document Analysis</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="space-y-2">
        {menuItems.map((item) => (
          <Button
            key={item.id}
            variant={activeTab === item.id ? "default" : "ghost"}
            className="w-full justify-start h-12 px-4 mb-1"
            onClick={() => onTabChange?.(item.id)}
          >
            <div className="flex items-center gap-3">
              <span className="text-lg">{item.icon}</span>
              <div className="text-left">
                <div className="text-white text-sm font-medium">{item.label}</div>
                <div className="text-gray-500 text-xs">{item.description}</div>
              </div>
            </div>
          </Button>
        ))}
      </nav>

      {/* User Section */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="border-t border-green-900 pt-4">
          <Button variant="ghost" className="w-full justify-start">
            <span className="mr-2">👤</span>
            <span className="text-sm">Profile</span>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
