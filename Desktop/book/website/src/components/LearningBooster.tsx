/**
 * LearningBooster React Component (T060)
 */
import React from 'react';
import styles from './LearningBooster.module.css';

interface LearningBoosterProps {
  type: 'analogy' | 'example' | 'explanation';
  content: string;
}

const icons = { analogy: '🔗', example: '💡', explanation: '📖' };
const titles = { analogy: 'Analogy', example: 'Real-World Example', explanation: 'Simplified Explanation' };

export default function LearningBooster({ type, content }: LearningBoosterProps): JSX.Element {
  return (
    <div className={`${styles.booster} ${styles[type]}`} role="complementary" aria-label={`Learning aid: ${titles[type]}`}>
      <div className={styles.header}>
        <span className={styles.icon}>{icons[type]}</span>
        <span className={styles.title}>{titles[type]}</span>
      </div>
      <div className={styles.content}>{content}</div>
    </div>
  );
}
