import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, Mic, MoreVertical, ThumbsUp, ThumbsDown, Share, Sparkles, Brain, FileText, Music, User } from 'lucide-react';

const ChatTemplate = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [selectedTool, setSelectedTool] = useState('DeepInnova');
  const [showWelcome, setShowWelcome] = useState(true);
  const [animatedText, setAnimatedText] = useState('');
  const fileInputRef = useRef(null);
  const audioInputRef = useRef(null);
  const inputRef = useRef(null);

  const tools = [
    { name: 'DeepInnova', icon: Brain, message: "How can I assist you today?" },
    { name: 'Website Builder', icon: 'W', message: "Let's build an innovative website!" },
    { name: 'Agent Developer', icon: 'A', message: "Ready to develop a cool AI agent?" },
    { name: 'Image Generator', icon: 'I', message: "Let's create some amazing visuals!" },
    { name: 'Code Generator', icon: '</>',message: "Time to write some groundbreaking code!" },
    { name: 'Video Generator', icon: 'V', message: "Let's bring your ideas to life in video!" },
    { name: 'Email Composer', icon: '@', message: "Craft the perfect email with AI assistance." },
  ];

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    const tool = tools.find(t => t.name === selectedTool);
    if (tool) {
      setAnimatedText('');
      let i = 0;
      const intervalId = setInterval(() => {
        if (i <= tool.message.length) {
          setAnimatedText(tool.message.slice(0, i));
          i++;
        } else {
          clearInterval(intervalId);
        }
      }, 50);
      return () => clearInterval(intervalId);
    }
  }, [selectedTool]);

  const handleSend = () => {
    if (input.trim() || fileInputRef.current.files.length > 0 || audioInputRef.current.files.length > 0) {
      const newMessage = { sender: 'user', type: 'text', content: input };
      if (fileInputRef.current.files.length > 0) {
        newMessage.type = 'file';
        newMessage.fileName = fileInputRef.current.files[0].name;
      } else if (audioInputRef.current.files.length > 0) {
        newMessage.type = 'audio';
        newMessage.fileName = audioInputRef.current.files[0].name;
      }
      setMessages([...messages, newMessage]);
      setInput('');
      setShowWelcome(false);
      setAnimatedText('');
      fileInputRef.current.value = '';
      audioInputRef.current.value = '';
      
      // Simulate AI response
      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, { 
          type: 'text',
          content: "Here's a response from DeepInnova based on your input.",
          sender: 'ai'
        }]);
      }, 1000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    if (e.target.value.trim() !== '') {
      setShowWelcome(false);
      setAnimatedText('');
    } else {
      setShowWelcome(messages.length === 0);
      const tool = tools.find(t => t.name === selectedTool);
      if (tool) {
        setAnimatedText(tool.message);
      }
    }
  };

  const handleFileUpload = () => {
    fileInputRef.current.click();
  };

  const handleAudioUpload = () => {
    audioInputRef.current.click();
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Left Sidebar */}
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
                {typeof tool.icon === 'string' ? tool.icon : <tool.icon size={16} />}
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

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
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
              onClick={handleSend} 
              className="p-2 bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors"
            >
              <Send size={20} />
            </button>
          </div>
          <input type="file" ref={fileInputRef} className="hidden" onChange={handleSend} />
          <input type="file" accept="audio/*" ref={audioInputRef} className="hidden" onChange={handleSend} />
        </div>
      </div>

      {/* Right Sidebar */}
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
    </div>
  );
};

export default ChatTemplate;