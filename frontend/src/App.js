import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import ChatWindow from './components/ChatWindow/ChatWindow';
import InputArea from './components/InputArea/InputArea';
import RightSidebar from './components/RightSidebar/RightSidebar';
import { tools } from './utils/constants';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [selectedTool, setSelectedTool] = useState('DeepInnova');
  const [showWelcome, setShowWelcome] = useState(true);
  const [animatedText, setAnimatedText] = useState('');

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

  const handleSend = (newMessage) => {
    setMessages([...messages, newMessage]);
    setInput('');
    setShowWelcome(false);
    setAnimatedText('');
    
    // Simulate AI response
    setTimeout(() => {
      setMessages(prevMessages => [...prevMessages, { 
        type: 'text',
        content: "Here's a response from DeepInnova based on your input.",
        sender: 'ai'
      }]);
    }, 1000);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar 
        tools={tools} 
        selectedTool={selectedTool} 
        setSelectedTool={setSelectedTool}
        setShowWelcome={setShowWelcome}
        setAnimatedText={setAnimatedText}
      />
      <div className="flex-1 flex flex-col">
        <ChatWindow 
          messages={messages} 
          showWelcome={showWelcome} 
          animatedText={animatedText} 
          selectedTool={selectedTool}
        />
        <InputArea 
          input={input} 
          setInput={setInput} 
          handleSend={handleSend}
          setShowWelcome={setShowWelcome}
          setAnimatedText={setAnimatedText}
          selectedTool={selectedTool}
          tools={tools}
        />
      </div>
      <RightSidebar />
    </div>
  );
};

export default App;