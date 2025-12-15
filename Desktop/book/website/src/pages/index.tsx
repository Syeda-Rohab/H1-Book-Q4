import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

const FeatureList = [
  {
    title: '🤖 AI-Native Content',
    description: (
      <>
        Every chapter is generated and enhanced by Claude AI, ensuring modern,
        accurate content on Physical AI and Humanoid Robotics.
      </>
    ),
  },
  {
    title: '⚡ Lightning Fast',
    description: (
      <>
        Optimized for speed and simplicity. Read the entire textbook in under
        50 minutes. Perfect for learners on low-end devices.
      </>
    ),
  },
  {
    title: '📱 Mobile-First',
    description: (
      <>
        Fully responsive design that works beautifully on all devices. Learn
        anywhere, anytime, on any screen size.
      </>
    ),
  },
  {
    title: '✨ Interactive Learning',
    description: (
      <>
        Self-assessment quizzes, chapter summaries, and learning boosters help
        you master concepts quickly and effectively.
      </>
    ),
  },
  {
    title: '🎯 Quality Over Quantity',
    description: (
      <>
        Just 6 focused chapters, each 5-7 minutes to read. No fluff, only the
        essential concepts you need to know.
      </>
    ),
  },
  {
    title: '🌍 Free & Open',
    description: (
      <>
        Completely free to access. Built on free-tier infrastructure and open
        source principles. Education for everyone.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <span className={styles.badge}>AI-Powered Education</span>
          <h1 className={styles.heroTitle}>
            Physical AI & <br />
            <span className={styles.gradient}>Humanoid Robotics</span>
          </h1>
          <p className={styles.heroSubtitle}>
            Master the fundamentals of embodied intelligence, humanoid robots, and AI-driven control systems.
            Learn from an AI-native textbook designed for the modern learner.
          </p>
          <div className={styles.buttons}>
            <Link
              className={clsx('button button--primary button--lg', styles.buttonPrimary)}
              to="/docs/intro">
              Start Learning
            </Link>
            <Link
              className={clsx('button button--secondary button--lg', styles.buttonSecondary)}
              to="/docs/chapter-01-physical-ai-intro">
              Read Chapter 1
            </Link>
          </div>
          <div className={styles.stats}>
            <div className={styles.stat}>
              <div className={styles.statNumber}>6</div>
              <div className={styles.statLabel}>Chapters</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>~50</div>
              <div className={styles.statLabel}>Minutes</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>100%</div>
              <div className={styles.statLabel}>Free</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function ChapterOverview() {
  const chapters = [
    {
      number: '01',
      title: 'Introduction to Physical AI',
      description: 'Foundations of embodied intelligence and real-world AI systems',
      link: '/docs/chapter-01-physical-ai-intro',
    },
    {
      number: '02',
      title: 'Humanoid Robotics Fundamentals',
      description: 'Robot anatomy, degrees of freedom, and balance control',
      link: '/docs/chapter-02-humanoid-robotics-fundamentals',
    },
    {
      number: '03',
      title: 'Sensors and Perception',
      description: 'Vision systems, tactile sensors, IMUs, and sensor fusion',
      link: '/docs/chapter-03-sensors-perception',
    },
    {
      number: '04',
      title: 'Actuators and Motion',
      description: 'Motors, hydraulics, and bipedal locomotion systems',
      link: '/docs/chapter-04-actuators-motion',
    },
    {
      number: '05',
      title: 'AI for Robot Control',
      description: 'Reinforcement learning, imitation learning, and sim-to-real transfer',
      link: '/docs/chapter-05-ai-robot-control',
    },
    {
      number: '06',
      title: 'Manipulation and Dexterity',
      description: 'Grasp planning, object manipulation, and dexterous hands',
      link: '/docs/chapter-06-manipulation-dexterity',
    },
  ];

  return (
    <section className={styles.chapters}>
      <div className="container">
        <h2 className={styles.sectionTitle}>What You'll Learn</h2>
        <p className={styles.sectionSubtitle}>
          6 comprehensive chapters covering the essential concepts of Physical AI and Humanoid Robotics
        </p>
        <div className={styles.chapterGrid}>
          {chapters.map((chapter) => (
            <Link
              key={chapter.number}
              to={chapter.link}
              className={styles.chapterCard}>
              <div className={styles.chapterNumber}>Chapter {chapter.number}</div>
              <h3 className={styles.chapterTitle}>{chapter.title}</h3>
              <p className={styles.chapterDescription}>{chapter.description}</p>
              <div className={styles.chapterArrow}>→</div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Learn Physical AI and Humanoid Robotics with an AI-native interactive textbook">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {FeatureList.map((props, idx) => (
                <Feature key={idx} {...props} />
              ))}
            </div>
          </div>
        </section>
        <ChapterOverview />
        <section className={styles.cta}>
          <div className="container">
            <h2>Ready to Start Learning?</h2>
            <p>Dive into the world of Physical AI and Humanoid Robotics today.</p>
            <Link
              className={clsx('button button--primary button--lg', styles.ctaButton)}
              to="/docs/intro">
              Start Reading Now
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
