import React from 'react';
import { User, Brain, ThumbsUp, ThumbsDown, Share, MoreVertical, FileText, Music } from 'lucide-react';
import './ChatWindow.css';

const ChatWindow = ({ messages, showWelcome, animatedText, selectedTool }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 relative">
      <div className="text-2xl font-bold mb-4">{selectedTool}</div>
      {(showWelcome || animatedText) && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-2xl text-gray-400 text-center">
          {animatedText}
        </div>
      )}
      {messages.map((message, index) => (
        <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-xl rounded-lg p-3 flex items-start ${
            message.sender === 'user' ? 'bg-purple-600' : 'bg-gray-700'
          }`}>
            <div className="w-8 h-8 rounded-full mr-3 flex items-center justify-center bg-gray-600">
              {message.sender === 'user' ? <User size={20} /> : <Brain size={20} />}
            </div>
            <div className="flex-1">
              {message.type === 'text' && message.content}
              {message.type === 'file' && <div><FileText size={16} className="inline mr-2" />{message.fileName}</div>}
              {message.type === 'audio' && <div><Music size={16} className="inline mr-2" />{message.fileName}</div>}
              {message.sender === 'ai' && (
                <div className="flex items-center mt-2 space-x-2">
                  <ThumbsUp size={16} />
                  <ThumbsDown size={16} />
                  <Share size={16} />
                  <MoreVertical size={16} />
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;