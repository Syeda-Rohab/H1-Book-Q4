/**
 * Video Gallery Component
 *
 * Features:
 * - Curated video demonstrations of robotics concepts
 * - Organized by chapter/topic
 * - YouTube embeds with responsive design
 * - Playlist support
 */

import React, { useState } from 'react';
import styles from './VideoGallery.module.css';

interface Video {
  id: string;
  title: string;
  description: string;
  youtubeId: string;
  chapter: string;
  duration: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

// Curated video demonstrations (these are example placeholders - replace with actual videos)
const VIDEOS: Video[] = [
  {
    id: '1',
    title: 'Introduction to Physical AI Systems',
    description: 'Overview of how AI integrates with physical robotics systems',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder - replace with actual video ID
    chapter: 'Introduction',
    duration: '10:23',
    difficulty: 'beginner',
  },
  {
    id: '2',
    title: 'Humanoid Robot Walking Demo',
    description: 'Boston Dynamics Atlas performing bipedal locomotion',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    chapter: 'Humanoid Robotics',
    duration: '5:47',
    difficulty: 'intermediate',
  },
  {
    id: '3',
    title: 'Sensor Fusion in Action',
    description: 'How robots combine multiple sensors for perception',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    chapter: 'Sensors',
    duration: '8:15',
    difficulty: 'advanced',
  },
  {
    id: '4',
    title: 'Robotic Manipulation Techniques',
    description: 'Demonstrations of grasping and manipulation',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    chapter: 'Manipulation',
    duration: '12:30',
    difficulty: 'intermediate',
  },
  {
    id: '5',
    title: 'Reinforcement Learning for Robot Control',
    description: 'How RL enables robots to learn complex behaviors',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    chapter: 'AI Control',
    duration: '15:42',
    difficulty: 'advanced',
  },
  {
    id: '6',
    title: 'Robot Safety Mechanisms',
    description: 'Fail-safe systems and collision avoidance in action',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    chapter: 'Safety',
    duration: '7:28',
    difficulty: 'beginner',
  },
];

const CHAPTERS = ['All', 'Introduction', 'Humanoid Robotics', 'Sensors', 'Manipulation', 'AI Control', 'Safety'];

export default function VideoGallery(): JSX.Element {
  const [selectedChapter, setSelectedChapter] = useState('All');
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);

  const filteredVideos = selectedChapter === 'All'
    ? VIDEOS
    : VIDEOS.filter(v => v.chapter === selectedChapter);

  return (
    <div className={styles.gallery}>
      <div className={styles.header}>
        <h2>Video Demonstrations</h2>
        <p>Learn through visual demonstrations of robotics concepts</p>
      </div>

      <div className={styles.filters}>
        <div className={styles.filterGroup}>
          <label>Filter by Chapter:</label>
          <div className={styles.filterButtons}>
            {CHAPTERS.map(chapter => (
              <button
                key={chapter}
                className={`${styles.filterButton} ${selectedChapter === chapter ? styles.active : ''}`}
                onClick={() => setSelectedChapter(chapter)}
              >
                {chapter}
              </button>
            ))}
          </div>
        </div>
      </div>

      {selectedVideo && (
        <div className={styles.videoPlayer}>
          <div className={styles.playerHeader}>
            <h3>{selectedVideo.title}</h3>
            <button
              className={styles.closeButton}
              onClick={() => setSelectedVideo(null)}
              aria-label="Close video"
            >
              ✕
            </button>
          </div>
          <div className={styles.videoEmbed}>
            <iframe
              src={`https://www.youtube.com/embed/${selectedVideo.youtubeId}`}
              title={selectedVideo.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <div className={styles.videoInfo}>
            <p>{selectedVideo.description}</p>
            <div className={styles.videoMeta}>
              <span className={styles.duration}>⏱️ {selectedVideo.duration}</span>
              <span className={`${styles.difficulty} ${styles[selectedVideo.difficulty]}`}>
                {selectedVideo.difficulty}
              </span>
            </div>
          </div>
        </div>
      )}

      <div className={styles.videoGrid}>
        {filteredVideos.map(video => (
          <div key={video.id} className={styles.videoCard} onClick={() => setSelectedVideo(video)}>
            <div className={styles.thumbnail}>
              <img
                src={`https://img.youtube.com/vi/${video.youtubeId}/mqdefault.jpg`}
                alt={video.title}
              />
              <div className={styles.playButton}>▶</div>
              <div className={styles.duration}>{video.duration}</div>
            </div>
            <div className={styles.cardContent}>
              <h4>{video.title}</h4>
              <p>{video.description}</p>
              <div className={styles.cardMeta}>
                <span className={styles.chapter}>{video.chapter}</span>
                <span className={`${styles.difficulty} ${styles[video.difficulty]}`}>
                  {video.difficulty}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredVideos.length === 0 && (
        <div className={styles.emptyState}>
          <p>No videos found for this chapter.</p>
        </div>
      )}

      <div className={styles.notice}>
        <p>
          <strong>Note:</strong> Video demonstrations include content from leading robotics research labs
          and educational channels. Check back regularly for new additions!
        </p>
      </div>
    </div>
  );
}
