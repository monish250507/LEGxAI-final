import React, { useState } from 'react';

interface ChatbotWidgetProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({ isOpen, onToggle }) => {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = () => {
    if (message.trim()) {
      // Mock send - replace with actual API call
      console.log('Sending message:', message);
      setMessage('');
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && message.trim()) {
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={onToggle}
        className={`
          fixed bottom-6 right-6 w-14 h-14 bg-green-500 border-2 border-green-400 rounded-full flex items-center justify-center
          hover:bg-green-400 hover:shadow-[0_0_25px_rgba(0,255,136,0.6)] 
          transition-all duration-300 z-50
          ${isOpen ? 'rotate-45' : ''}
        `}
      >
        <span className="text-black font-bold text-xl">
          {isOpen ? '✕' : '💬'}
        </span>
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-black border border-green-500 rounded-2xl w-full max-w-2xl mx-4 h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="border-b border-green-900 p-4 flex items-center justify-between">
              <h3 className="text-green-400 font-bold text-lg">AI Legal Assistant</h3>
              <button 
                onClick={onToggle}
                className="text-gray-400 hover:text-green-400 transition-colors duration-200"
              >
                ✕
              </button>
            </div>
            
            {/* Chat Messages */}
            <div className="flex-1 p-4 overflow-y-auto">
              <div className="space-y-4">
                {/* AI Message */}
                <div className="flex justify-start">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-black font-bold text-sm">AI</span>
                  </div>
                  <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 max-w-[80%]">
                    <p className="text-green-300 text-sm">
                      Hello! I'm your AI legal assistant. I can help you understand any clause in your document, provide offensive and defensive analysis, and answer your legal questions.
                    </p>
                  </div>
                </div>
                
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-sm">U</span>
                  </div>
                  <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 max-w-[80%]">
                    <p className="text-white text-sm">
                      {message}
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Chat Input */}
            <div className="border-t border-green-900 p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onFocus={() => setIsTyping(true)}
                  onBlur={() => setIsTyping(false)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about any clause..."
                  className="flex-1 bg-black border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!message.trim() || isTyping}
                  className="bg-green-500 text-black px-6 py-3 rounded-lg hover:bg-green-400 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;
