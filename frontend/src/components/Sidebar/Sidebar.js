import React from 'react';
import { Brain } from 'lucide-react';
import { tools } from '../../utils/constants';

const Sidebar = ({ selectedTool, setSelectedTool, setShowWelcome, setAnimatedText }) => {
  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col">
      <div className="flex items-center mb-6">
        <div className="w-8 h-8 bg-purple-600 rounded-lg mr-2 flex items-center justify-center">
          <Brain size={24} />
        </div>
        <span className="text-xl font-bold">DeepInnova</span>
      </div>
      {tools.map(tool => (
        <div 
          key={tool.name} 
          className={`mb-2 p-2 rounded-lg cursor-pointer flex items-center justify-between ${selectedTool === tool.name ? 'bg-gray-700' : 'hover:bg-gray-700'}`}
          onClick={() => {
            setSelectedTool(tool.name);
            setShowWelcome(true);
            setAnimatedText('');
          }}
        >
          <div className="flex items-center">
            <span className="w-6 h-6 bg-gray-600 rounded flex items-center justify-center mr-2">
              <tool.icon size={16} />
            </span>
            <span>{tool.name}</span>
          </div>
        </div>
      ))}
      <div className="mt-auto">
        <div className="flex items-center p-2 bg-gray-700 rounded-lg mb-2">
          <img src="/api/placeholder/32/32" alt="User" className="w-8 h-8 rounded-full mr-2" />
          <div>
            <div className="font-semibold">RainbowIT</div>
            <div className="text-sm text-gray-400">adam@gmail.com</div>
          </div>
        </div>
        <button className="w-full py-2 bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors">
          Upgrade To Pro
        </button>
      </div>
    </div>
  );
};

export default Sidebar;