/**
 * AI Chatbot Component for RAG-based Q&A
 *
 * Features:
 * - Natural language question answering
 * - Context-aware responses from textbook content
 * - Search through chapter content
 * - Interactive chat interface
 * - Mobile-responsive design
 */

import React, { useState, useRef, useEffect } from 'react';
import styles from './AIChatbot.module.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
}

interface ChapterContent {
  title: string;
  slug: string;
  content: string;
  keywords: string[];
}

// Sample chapter data - In production, this would be loaded dynamically
const CHAPTER_DATA: ChapterContent[] = [
  {
    title: 'Introduction to Physical AI',
    slug: 'chapter-01-physical-ai-intro',
    content: 'Physical AI focuses on creating intelligent systems with physical embodiment. Unlike traditional AI, Physical AI systems interact with the physical world through sensors and actuators. Embodied intelligence emerges from the interaction between a physical system and its environment.',
    keywords: ['physical ai', 'embodied ai', 'embodiment', 'intelligence', 'sensors', 'actuators']
  },
  {
    title: 'Humanoid Robotics Fundamentals',
    slug: 'chapter-02-humanoid-robotics-fundamentals',
    content: 'Humanoid robots mimic human anatomy with degrees of freedom, balance control, and bipedal locomotion. They feature torso, arms, legs, and head structures with sophisticated control systems.',
    keywords: ['humanoid', 'robotics', 'anatomy', 'dof', 'balance', 'bipedal']
  },
  {
    title: 'Sensors and Perception',
    slug: 'chapter-03-sensors-perception',
    content: 'Robot perception relies on vision systems, tactile sensors, IMUs, and sensor fusion. Cameras and depth sensors provide visual information, while force sensors enable touch interaction.',
    keywords: ['sensors', 'perception', 'vision', 'tactile', 'imu', 'fusion']
  },
  {
    title: 'Actuators and Motion',
    slug: 'chapter-04-actuators-motion',
    content: 'Actuators power robot movement using motors, hydraulics, and pneumatics. Bipedal locomotion requires sophisticated control for balance and efficiency.',
    keywords: ['actuators', 'motors', 'hydraulics', 'locomotion', 'movement']
  },
  {
    title: 'AI for Robot Control',
    slug: 'chapter-05-ai-robot-control',
    content: 'Modern robot control uses reinforcement learning, imitation learning, and sim-to-real transfer. AI enables robots to learn complex behaviors from demonstrations and simulation.',
    keywords: ['ai', 'reinforcement learning', 'imitation learning', 'sim-to-real', 'control']
  },
  {
    title: 'Manipulation and Dexterity',
    slug: 'chapter-06-manipulation-dexterity',
    content: 'Robot manipulation involves grasp planning, force control, and dexterous hands. Advanced systems can handle delicate objects and perform complex assembly tasks.',
    keywords: ['manipulation', 'dexterity', 'grasping', 'hands', 'assembly']
  },
  {
    title: 'Safety and Ethics',
    slug: 'chapter-07-safety-ethics',
    content: 'Robot safety requires fail-safe mechanisms, harm prevention, and ethical considerations. Privacy, autonomy, and human-robot interaction guidelines ensure responsible deployment.',
    keywords: ['safety', 'ethics', 'privacy', 'human-robot interaction', 'responsible ai']
  },
  {
    title: 'Future Trends',
    slug: 'chapter-08-future-trends',
    content: 'Future robotics trends include VLA models, foundation models, soft robotics, and neuromorphic computing. General-purpose robots and human collaboration are emerging focus areas.',
    keywords: ['vla', 'foundation models', 'future', 'trends', 'soft robotics', 'neuromorphic']
  }
];

// Simple keyword-based search (in production, use proper RAG with embeddings)
function searchContent(query: string): { chapter: ChapterContent; relevance: number }[] {
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(' ').filter(w => w.length > 2);

  const results = CHAPTER_DATA.map(chapter => {
    let relevance = 0;

    // Check keywords
    chapter.keywords.forEach(keyword => {
      if (queryWords.some(word => keyword.includes(word) || word.includes(keyword))) {
        relevance += 3;
      }
    });

    // Check title
    if (chapter.title.toLowerCase().includes(queryLower)) {
      relevance += 5;
    }

    // Check content
    queryWords.forEach(word => {
      if (chapter.content.toLowerCase().includes(word)) {
        relevance += 1;
      }
    });

    return { chapter, relevance };
  }).filter(r => r.relevance > 0);

  return results.sort((a, b) => b.relevance - a.relevance);
}

// Generate response based on search results
function generateResponse(query: string): { text: string; sources: string[] } {
  const results = searchContent(query);

  if (results.length === 0) {
    return {
      text: "I couldn't find specific information about that in the textbook. Could you rephrase your question or ask about topics like Physical AI fundamentals, sensors, actuators, AI control, manipulation, safety, or future trends?",
      sources: []
    };
  }

  const topResults = results.slice(0, 2);
  const sources = topResults.map(r => r.chapter.title);

  // Create contextual response
  let response = `Based on the textbook content:\n\n`;
  response += topResults[0].chapter.content;

  if (topResults.length > 1 && topResults[1].relevance > 2) {
    response += `\n\nAdditionally, ${topResults[1].chapter.content}`;
  }

  response += `\n\nFor more details, check the related chapters in the sidebar.`;

  return { text: response, sources };
}

export default function AIChatbot(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your AI textbook assistant. Ask me anything about Physical AI and Humanoid Robotics!",
      sender: 'bot',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate AI processing delay
    setTimeout(() => {
      const { text, sources } = generateResponse(inputValue);

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text,
        sender: 'bot',
        timestamp: new Date(),
        sources,
      };

      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 800);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestedQuestions = [
    "What is Physical AI?",
    "How do sensors work in robots?",
    "What are the safety concerns in robotics?",
    "Tell me about future trends in AI"
  ];

  const handleSuggestionClick = (question: string) => {
    setInputValue(question);
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatHeader}>
        <div className={styles.headerIcon}>🤖</div>
        <div className={styles.headerText}>
          <h3>AI Textbook Assistant</h3>
          <p>Powered by RAG</p>
        </div>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${styles[message.sender]}`}
          >
            <div className={styles.messageContent}>
              <div className={styles.messageText}>{message.text}</div>
              {message.sources && message.sources.length > 0 && (
                <div className={styles.sources}>
                  <strong>Sources:</strong> {message.sources.join(', ')}
                </div>
              )}
              <div className={styles.timestamp}>
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className={`${styles.message} ${styles.bot}`}>
            <div className={styles.messageContent}>
              <div className={styles.typing}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <div className={styles.suggestions}>
          <p className={styles.suggestionsTitle}>Suggested questions:</p>
          {suggestedQuestions.map((question, index) => (
            <button
              key={index}
              className={styles.suggestionButton}
              onClick={() => handleSuggestionClick(question)}
            >
              {question}
            </button>
          ))}
        </div>
      )}

      <div className={styles.inputContainer}>
        <textarea
          className={styles.input}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the textbook..."
          rows={1}
        />
        <button
          className={styles.sendButton}
          onClick={handleSend}
          disabled={!inputValue.trim() || isTyping}
          aria-label="Send message"
        >
          <span className={styles.sendIcon}>➤</span>
        </button>
      </div>
    </div>
  );
}
