import React from 'react';
import { MoreVertical } from 'lucide-react';
import './RightSidebar.css';

const RightSidebar = () => {
  return (
    <div className="w-64 bg-gray-800 p-4">
      <button className="w-full py-2 bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors mb-4">
        NEW CHAT
      </button>
      <input
        type="text"
        placeholder="Search Here..."
        className="w-full p-2 bg-gray-700 rounded-lg mb-4"
      />
      <div>
        <h3 className="font-semibold mb-2">Today</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span>DeepInnova Intro</span>
            <MoreVertical size={16} />
          </div>
          <div className="flex items-center justify-between">
            <span>Your last Query</span>
            <MoreVertical size={16} />
          </div>
          {/* Add more items as needed */}
        </div>
      </div>
    </div>
  );
};

export default RightSidebar;