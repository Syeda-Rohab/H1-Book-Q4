/**
 * Personalization Dashboard Component
 *
 * Features:
 * - Progress tracking across chapters
 * - Personalized chapter recommendations
 * - Reading time estimates based on user pace
 * - Quiz performance analytics
 * - Learning preferences
 */

import React, { useState, useEffect } from 'react';
import styles from './PersonalizationDashboard.module.css';

interface ChapterProgress {
  slug: string;
  title: string;
  completed: boolean;
  quizScore?: number;
  timeSpent: number; // in minutes
  lastVisited: Date;
}

interface UserPreferences {
  readingSpeed: 'slow' | 'medium' | 'fast';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  theme: 'light' | 'dark' | 'auto';
  notificationsEnabled: boolean;
}

interface PersonalizationData {
  progress: ChapterProgress[];
  preferences: UserPreferences;
  totalReadingTime: number;
  completedChapters: number;
  averageQuizScore: number;
}

const CHAPTERS = [
  { slug: 'chapter-01-physical-ai-intro', title: 'Introduction to Physical AI', order: 1 },
  { slug: 'chapter-02-humanoid-robotics-fundamentals', title: 'Humanoid Robotics Fundamentals', order: 2 },
  { slug: 'chapter-03-sensors-perception', title: 'Sensors and Perception', order: 3 },
  { slug: 'chapter-04-actuators-motion', title: 'Actuators and Motion', order: 4 },
  { slug: 'chapter-05-ai-robot-control', title: 'AI for Robot Control', order: 5 },
  { slug: 'chapter-06-manipulation-dexterity', title: 'Manipulation and Dexterity', order: 6 },
  { slug: 'chapter-07-safety-ethics', title: 'Safety and Ethics', order: 7 },
  { slug: 'chapter-08-future-trends', title: 'Future Trends', order: 8 },
];

// Load personalization data from localStorage
function loadPersonalizationData(): PersonalizationData {
  // Check if we're in a browser environment
  if (typeof window === 'undefined') {
    // Return default data for SSR
    return getDefaultData();
  }

  const stored = localStorage.getItem('personalization_data');
  if (stored) {
    const data = JSON.parse(stored);
    // Convert date strings back to Date objects
    data.progress = data.progress.map((p: any) => ({
      ...p,
      lastVisited: new Date(p.lastVisited)
    }));
    return data;
  }

  // Default data
  return getDefaultData();
}

// Get default personalization data
function getDefaultData(): PersonalizationData {
  return {
    progress: CHAPTERS.map(ch => ({
      slug: ch.slug,
      title: ch.title,
      completed: false,
      timeSpent: 0,
      lastVisited: new Date(),
    })),
    preferences: {
      readingSpeed: 'medium',
      difficulty: 'beginner',
      theme: 'auto',
      notificationsEnabled: false,
    },
    totalReadingTime: 0,
    completedChapters: 0,
    averageQuizScore: 0,
  };
}

// Save personalization data to localStorage
function savePersonalizationData(data: PersonalizationData): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('personalization_data', JSON.stringify(data));
  }
}

export default function PersonalizationDashboard(): JSX.Element {
  const [data, setData] = useState<PersonalizationData>(loadPersonalizationData());
  const [activeTab, setActiveTab] = useState<'progress' | 'recommendations' | 'preferences'>('progress');

  useEffect(() => {
    savePersonalizationData(data);
  }, [data]);

  const handleMarkComplete = (slug: string) => {
    setData(prev => {
      const newProgress = prev.progress.map(p =>
        p.slug === slug ? { ...p, completed: !p.completed } : p
      );
      const completedCount = newProgress.filter(p => p.completed).length;

      return {
        ...prev,
        progress: newProgress,
        completedChapters: completedCount,
      };
    });
  };

  const handlePreferenceChange = (key: keyof UserPreferences, value: any) => {
    setData(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: value,
      },
    }));
  };

  const getRecommendations = (): ChapterProgress[] => {
    const incomplete = data.progress.filter(p => !p.completed);
    return incomplete.slice(0, 3);
  };

  const getProgressPercentage = (): number => {
    return Math.round((data.completedChapters / CHAPTERS.length) * 100);
  };

  const getEstimatedTimeRemaining = (): number => {
    const avgTimePerChapter = 7; // 7 minutes average
    const speedMultiplier = data.preferences.readingSpeed === 'fast' ? 0.8 :
                           data.preferences.readingSpeed === 'slow' ? 1.2 : 1.0;
    const remaining = CHAPTERS.length - data.completedChapters;
    return Math.round(remaining * avgTimePerChapter * speedMultiplier);
  };

  return (
    <div className={styles.dashboard}>
      <div className={styles.header}>
        <h2>Your Learning Dashboard</h2>
        <p>Track your progress and personalize your learning experience</p>
      </div>

      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'progress' ? styles.active : ''}`}
          onClick={() => setActiveTab('progress')}
        >
          📊 Progress
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'recommendations' ? styles.active : ''}`}
          onClick={() => setActiveTab('recommendations')}
        >
          💡 Recommendations
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'preferences' ? styles.active : ''}`}
          onClick={() => setActiveTab('preferences')}
        >
          ⚙️ Preferences
        </button>
      </div>

      {activeTab === 'progress' && (
        <div className={styles.content}>
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statIcon}>📚</div>
              <div className={styles.statValue}>{data.completedChapters}/{CHAPTERS.length}</div>
              <div className={styles.statLabel}>Chapters Completed</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statIcon}>⏱️</div>
              <div className={styles.statValue}>{getEstimatedTimeRemaining()} min</div>
              <div className={styles.statLabel}>Time Remaining</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statIcon}>🎯</div>
              <div className={styles.statValue}>{getProgressPercentage()}%</div>
              <div className={styles.statLabel}>Overall Progress</div>
            </div>
          </div>

          <div className={styles.progressBar}>
            <div className={styles.progressFill} style={{ width: `${getProgressPercentage()}%` }} />
          </div>

          <div className={styles.chapterList}>
            <h3>Chapter Progress</h3>
            {data.progress.map((chapter) => (
              <div key={chapter.slug} className={styles.chapterItem}>
                <div className={styles.chapterInfo}>
                  <input
                    type="checkbox"
                    checked={chapter.completed}
                    onChange={() => handleMarkComplete(chapter.slug)}
                    className={styles.checkbox}
                  />
                  <div className={styles.chapterDetails}>
                    <h4>{chapter.title}</h4>
                    {chapter.quizScore !== undefined && (
                      <span className={styles.quizScore}>Quiz: {chapter.quizScore}%</span>
                    )}
                  </div>
                </div>
                {chapter.completed && <span className={styles.completedBadge}>✓</span>}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'recommendations' && (
        <div className={styles.content}>
          <h3>Recommended for You</h3>
          <p className={styles.recommendationIntro}>
            Based on your progress and preferences, here are your next chapters:
          </p>
          <div className={styles.recommendationList}>
            {getRecommendations().map((chapter, index) => (
              <div key={chapter.slug} className={styles.recommendationCard}>
                <div className={styles.recommendationNumber}>{index + 1}</div>
                <div className={styles.recommendationContent}>
                  <h4>{chapter.title}</h4>
                  <p>Estimated time: 5-7 minutes</p>
                  <a href={`/docs/${chapter.slug}`} className={styles.startButton}>
                    {chapter.timeSpent > 0 ? 'Continue Reading →' : 'Start Chapter →'}
                  </a>
                </div>
              </div>
            ))}
          </div>

          {data.completedChapters === CHAPTERS.length && (
            <div className={styles.completionMessage}>
              <h3>🎉 Congratulations!</h3>
              <p>You've completed all chapters! Consider retaking quizzes or exploring the AI Chat for deeper understanding.</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'preferences' && (
        <div className={styles.content}>
          <h3>Learning Preferences</h3>

          <div className={styles.preferenceGroup}>
            <label className={styles.preferenceLabel}>Reading Speed</label>
            <div className={styles.radioGroup}>
              {(['slow', 'medium', 'fast'] as const).map((speed) => (
                <label key={speed} className={styles.radioLabel}>
                  <input
                    type="radio"
                    name="readingSpeed"
                    value={speed}
                    checked={data.preferences.readingSpeed === speed}
                    onChange={(e) => handlePreferenceChange('readingSpeed', e.target.value)}
                  />
                  <span>{speed.charAt(0).toUpperCase() + speed.slice(1)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className={styles.preferenceGroup}>
            <label className={styles.preferenceLabel}>Difficulty Level</label>
            <div className={styles.radioGroup}>
              {(['beginner', 'intermediate', 'advanced'] as const).map((level) => (
                <label key={level} className={styles.radioLabel}>
                  <input
                    type="radio"
                    name="difficulty"
                    value={level}
                    checked={data.preferences.difficulty === level}
                    onChange={(e) => handlePreferenceChange('difficulty', e.target.value)}
                  />
                  <span>{level.charAt(0).toUpperCase() + level.slice(1)}</span>
                </label>
              ))}
            </div>
          </div>

          <div className={styles.preferenceGroup}>
            <label className={styles.preferenceLabel}>
              <input
                type="checkbox"
                checked={data.preferences.notificationsEnabled}
                onChange={(e) => handlePreferenceChange('notificationsEnabled', e.target.checked)}
                className={styles.checkbox}
              />
              <span>Enable learning reminders</span>
            </label>
          </div>

          <button className={styles.resetButton} onClick={() => {
            if (typeof window !== 'undefined' && confirm('Are you sure you want to reset all progress and preferences?')) {
              localStorage.removeItem('personalization_data');
              window.location.reload();
            }
          }}>
            Reset All Data
          </button>
        </div>
      )}
    </div>
  );
}
