// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Interactive Textbook',
  favicon: 'img/favicon.ico',

  // Production URL (Vercel deployment)
  url: 'https://h1-book-q4.vercel.app',
  baseUrl: '/',
  trailingSlash: false,

  // GitHub pages deployment config
  organizationName: 'Syeda-Rohab',
  projectName: 'ai-native-textbook',

  onBrokenLinks: 'warn',

  // Markdown configuration
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Internationalization (i18n) config
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          // Docs route at /docs (homepage at /)
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          // Remove edit links (no external repo for MVP)
          editUrl: undefined,
          // Disable blog features
          showLastUpdateTime: false,
          showLastUpdateAuthor: false,
        },
        blog: false, // Disable blog for textbook-only site
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/social-card.png',

      // Metadata
      metadata: [
        {name: 'keywords', content: 'physical ai, robotics, humanoid robots, ai textbook, machine learning, embodied intelligence'},
        {name: 'author', content: 'Syeda Rohab Ali'},
        {name: 'theme-color', content: '#00b894'},
      ],

      // Head tags for fonts and external resources
      headTags: [
        {
          tagName: 'link',
          attributes: {
            rel: 'preconnect',
            href: 'https://fonts.googleapis.com',
          },
        },
        {
          tagName: 'link',
          attributes: {
            rel: 'preconnect',
            href: 'https://fonts.gstatic.com',
            crossorigin: 'anonymous',
          },
        },
        {
          tagName: 'link',
          attributes: {
            rel: 'stylesheet',
            href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap',
          },
        },
      ],

      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Textbook Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            to: '/',
            label: 'Home',
            position: 'left',
          },
          {
            to: '/chat',
            label: '🤖 AI Chat',
            position: 'left',
          },
          {
            type: 'dropdown',
            label: '📚 Pages',
            position: 'left',
            items: [
              {
                type: 'docSidebar',
                sidebarId: 'textbookSidebar',
                label: '📖 Chapters',
              },
              {
                to: '/dashboard',
                label: '📊 Dashboard',
              },
              {
                to: '/simulations',
                label: '🎮 Simulations',
              },
            ],
          },
          {
            href: 'https://github.com/Syeda-Rohab/H1-Book-Q4',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Home',
                to: '/',
              },
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Chapter 1',
                to: '/docs/chapter-01-physical-ai-intro',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Syeda-Rohab/H1-Book-Q4',
              },
              {
                label: 'Report Issues',
                href: 'https://github.com/Syeda-Rohab/H1-Book-Q4/issues',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI-Native Textbook Project. Written by Syeda Rohab Ali. Built with Docusaurus.`,
      },

      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },

      // Mobile-responsive configuration (constitution: Principle VI)
      docs: {
        sidebar: {
          hideable: true,
          autoCollapseCategories: true,
        },
      },

      // Color mode configuration
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      // Algolia search (future enhancement)
      // algolia: {
      //   appId: 'YOUR_APP_ID',
      //   apiKey: 'YOUR_API_KEY',
      //   indexName: 'YOUR_INDEX_NAME',
      // },

      // Announcement bar (optional)
      announcementBar: {
        id: 'new_textbook',
        content:
          '🎓 New AI-Native Textbook on Physical AI & Humanoid Robotics - Start Learning Now! 🤖',
        backgroundColor: '#2e8555',
        textColor: '#ffffff',
        isCloseable: true,
      },
    }),

  // Plugins
  plugins: [],

  // Custom fields
  customFields: {
    // Constitution metadata
    constitution: {
      version: '1.0.0',
      principles: [
        'AI-Native Design',
        'Speed & Simplicity',
        'Free-Tier Architecture',
        'Grounded RAG Responses',
        'Modular Backend Structure',
        'Mobile-First Design',
        'Content Quality Over Quantity',
        'Observability',
      ],
    },
    // Textbook metadata
    textbook: {
      topic: 'Physical AI & Humanoid Robotics',
      chaptersTotal: 8, // Complete: 8 chapters including Safety/Ethics and Future Trends
      wordsPerChapter: '800-1200',
      readingTimePerChapter: '5-7 minutes',
    },
  },
};

module.exports = config;
