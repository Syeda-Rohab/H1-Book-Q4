import React, { useState, useEffect, useRef } from 'react';
import Link from '@docusaurus/Link';
import styles from './NavigationIcons.module.css';

interface Chapter {
  id: string;
  title: string;
  link: string;
}

const chapters: Chapter[] = [
  { id: 'intro', title: 'Welcome', link: '/docs/intro' },
  { id: 'ch01', title: 'Chapter 1: Physical AI Intro', link: '/docs/chapter-01-physical-ai-intro' },
  { id: 'ch02', title: 'Chapter 2: Humanoid Robotics', link: '/docs/chapter-02-humanoid-robotics-fundamentals' },
  { id: 'ch03', title: 'Chapter 3: Sensors & Perception', link: '/docs/chapter-03-sensors-perception' },
  { id: 'ch04', title: 'Chapter 4: Actuators & Motion', link: '/docs/chapter-04-actuators-motion' },
  { id: 'ch05', title: 'Chapter 5: AI Robot Control', link: '/docs/chapter-05-ai-robot-control' },
  { id: 'ch06', title: 'Chapter 6: Manipulation', link: '/docs/chapter-06-manipulation-dexterity' },
  { id: 'ch07', title: 'Chapter 7: Safety & Ethics', link: '/docs/chapter-07-safety-ethics' },
  { id: 'ch08', title: 'Chapter 8: Future Trends', link: '/docs/chapter-08-future-trends' },
];

export default function NavigationIcons(): JSX.Element {
  const [showChapters, setShowChapters] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowChapters(false);
      }
    }

    if (showChapters) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('touchstart', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('touchstart', handleClickOutside);
    };
  }, [showChapters]);

  return (
    <div className={styles.navIcons}>
      {/* AI Chat Icon */}
      <Link
        to="/chat"
        className={styles.iconButton}
        aria-label="AI Chat Assistant"
        title="AI Chat"
      >
        <span role="img" aria-label="robot">🤖</span>
      </Link>

      {/* Chapters Icon with Dropdown */}
      <div className={styles.iconWrapper} ref={dropdownRef}>
        <button
          className={styles.iconButton}
          onClick={() => setShowChapters(!showChapters)}
          aria-label="View Chapters"
          aria-expanded={showChapters}
          title="Chapters"
        >
          <span role="img" aria-label="book">📖</span>
        </button>
        {showChapters && (
          <div className={styles.dropdown} role="menu">
            <div className={styles.dropdownHeader}>All Chapters</div>
            <div className={styles.dropdownContent}>
              {chapters.map((chapter) => (
                <Link
                  key={chapter.id}
                  to={chapter.link}
                  className={styles.dropdownItem}
                  onClick={() => setShowChapters(false)}
                  role="menuitem"
                >
                  {chapter.title}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Dashboard Icon */}
      <Link
        to="/dashboard"
        className={styles.iconButton}
        aria-label="Dashboard"
        title="Dashboard"
      >
        <span role="img" aria-label="chart">📊</span>
      </Link>

      {/* Simulations Icon */}
      <Link
        to="/simulations"
        className={styles.iconButton}
        aria-label="Simulations"
        title="Simulations"
      >
        <span role="img" aria-label="game">🎮</span>
      </Link>
    </div>
  );
}
