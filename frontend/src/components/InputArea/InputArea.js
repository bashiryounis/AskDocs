import React, { useRef } from 'react';
import { Sparkles, FileText, Mic, Send } from 'lucide-react';
import './InputArea.css';

const InputArea = ({ input, setInput, handleSend, setShowWelcome, setAnimatedText, selectedTool, tools }) => {
  const fileInputRef = useRef(null);
  const audioInputRef = useRef(null);
  const inputRef = useRef(null);

  const handleInputChange = (e) => {
    setInput(e.target.value);
    if (e.target.value.trim() !== '') {
      setShowWelcome(false);
      setAnimatedText('');
    } else {
      setShowWelcome(true);
      const tool = tools.find(t => t.name === selectedTool);
      if (tool) {
        setAnimatedText(tool.message);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = () => {
    if (input.trim() || fileInputRef.current.files.length > 0 || audioInputRef.current.files.length > 0) {
      const newMessage = { sender: 'user', type: 'text', content: input };
      if (fileInputRef.current.files.length > 0) {
        newMessage.type = 'file';
        newMessage.fileName = fileInputRef.current.files[0].name;
      } else if (audioInputRef.current.files.length > 0) {
        newMessage.type = 'audio';
        newMessage.fileName = audioInputRef.current.files[0].name;
      }
      handleSend(newMessage);
      fileInputRef.current.value = '';
      audioInputRef.current.value = '';
    }
  };

  const handleFileUpload = () => {
    fileInputRef.current.click();
  };

  const handleAudioUpload = () => {
    audioInputRef.current.click();
  };

  return (
    <div className="p-4 bg-gray-800">
      <div className="flex items-center space-x-2 bg-gray-700 rounded-lg p-2">
        <Sparkles size={20} className="text-gray-400" />
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          className="flex-1 bg-transparent outline-none"
          placeholder="Send a message..."
        />
        <button onClick={handleFileUpload} className="text-gray-400 hover:text-white">
          <FileText size={20} />
        </button>
        <button onClick={handleAudioUpload} className="text-gray-400 hover:text-white">
          <Mic size={20} />
        </button>
        <button 
          onClick={handleSendMessage} 
          className="p-2 bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors"
        >
          <Send size={20} />
        </button>
      </div>
      <input type="file" ref={fileInputRef} className="hidden" onChange={handleSendMessage} />
      <input type="file" accept="audio/*" ref={audioInputRef} className="hidden" onChange={handleSendMessage} />
    </div>
  );
};

export default InputArea;