import React from 'react';
import Layout from '@theme/Layout';
import AIChatbot from '@site/src/components/AIChatbot';

export default function ChatPage(): JSX.Element {
  return (
    <Layout
      title="AI Chat Assistant"
      description="Ask questions about Physical AI and Humanoid Robotics"
    >
      <main>
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h1>AI Textbook Assistant</h1>
            <p style={{ fontSize: '1.125rem', color: 'var(--ifm-color-emphasis-700)', maxWidth: '600px', margin: '0 auto' }}>
              Ask me anything about Physical AI, Humanoid Robotics, Sensors, Actuators, AI Control, Safety, Ethics, and Future Trends!
            </p>
          </div>
          <AIChatbot />
        </div>
      </main>
    </Layout>
  );
}
